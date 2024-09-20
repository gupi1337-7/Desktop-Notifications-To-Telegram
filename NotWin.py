import time
import asyncio
import requests
import os
import re
from pywinauto import Desktop
from telegram.error import TelegramError
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder
from mss import mss
from PIL import Image


def get_credentials():
    token = input("Enter your Telegram Bot Token: ")
    chat_id = input("Enter your Telegram User ID: ")
    return token, chat_id


OCR_API_KEY = 'OCR_API_KEY'



def take_screenshot(filename="screenshot.png"):

    if os.path.exists(filename):
        os.remove(filename)

    with mss() as sct:
        monitor = sct.monitors[1]
        monitor_width = monitor['width']
        monitor_height = monitor['height']


        left = monitor_width - 500
        top = monitor_height - 500



        screenshot = sct.grab({'left': left, 'top': top, 'width': 500, 'height': 500})


        img = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
        img.save(filename)


def ocr_space_file(filename, api_key=OCR_API_KEY, language='eng'):
    payload = {
        'isOverlayRequired': False,
        'apikey': api_key,
        'language': language,
    }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload)
    return r.json()


async def send_telegram_message(application, chat_id, message):
    try:
        await application.bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)
        print("Message successfully sent")
        return True
    except TelegramError as e:
        print(f"Error when sending a message: {e}")
        return False


async def monitor_notifications(application, chat_id, api_key):
    print("Starting to monitor system notifications..")
    last_notification_time = 0
    last_screenshot_sent = False

    while True:
        current_time = time.time()

        if current_time - last_notification_time < 300:
            await asyncio.sleep(1)
            continue

        windows = Desktop(backend="uia").windows()
        for window in windows:
            window_text = window.window_text()

            if ('notification' in window_text.lower() or "Новое уведомление" in window_text):
                print(f"Found Notification: {window_text}")

                screenshot_filename = "screenshot.png"
                take_screenshot(screenshot_filename)

                try:
                    ocr_result = ocr_space_file(screenshot_filename, api_key=api_key)
                    text_detected = ocr_result.get('ParsedResults', [{}])[0].get('ParsedText', '').lower()
                    print(f"Found text: {text_detected}")


                    recipient_name = None
                    recipient_match = re.search(r"(\w+)(?:,|\s-)\s*(new letters|new chat invite)", text_detected, re.IGNORECASE)
                    if recipient_match:
                        recipient_name = recipient_match.group(1).capitalize()

                    if "letters" in text_detected:
                        match = re.search(r"new letters:\s*(\d+)", text_detected)
                        if match:
                            letter_count = match.group(1)
                            message = f"<b>{recipient_name + ' ' if recipient_name else ''}Retrieved {letter_count} new letters</b>"
                            await send_telegram_message(application, chat_id, message)
                        else:
                            message = f"{recipient_name + ' ' if recipient_name else ''}New letters have been received"
                            await send_telegram_message(application, chat_id, message)

                    elif "chat" in text_detected:
                        invites = re.findall(r"(\w+(?:\s+\w+)?)\s*[-–]\s*(?:'?d|id)[:•.]\s*(\d+)", text_detected, re.IGNORECASE)
                        if invites:
                            message = f"<b>{recipient_name + ' ' if recipient_name else ''}New chat invitations:</b>\n\n"
                            for name, id in invites:
                                name = ' '.join(word.capitalize() for word in name.split())
                                message += f"{name} - ID: {id}\n"
                            await send_telegram_message(application, chat_id, message)
                        else:
                            message = f"<b>{recipient_name + ' ' if recipient_name else ''}New chat invitation received</b>"
                            await send_telegram_message(application, chat_id, message)

                    elif "chat" in text_detected:
                        message = f"<b>{recipient_name + ' ' if recipient_name else ''}Chat Invitation</b>."
                        await send_telegram_message(application, chat_id, message)

                    elif "letters" in text_detected:
                        message = f"<b>{recipient_name + ' ' if recipient_name else ''}New Letter received.</b>"
                        await send_telegram_message(application, chat_id, message)

                except Exception as e:
                    print(f"Error during screenshot processing: {e}")
                    message = "New notification received (error while processing screenshot)"
                    await send_telegram_message(application, chat_id, message)

                last_notification_time = current_time
                last_screenshot_sent = True
                print("Message sent, waiting 300 seconds....")
                break

        await asyncio.sleep(1)
        last_screenshot_sent = False


async def main():
    TOKEN, CHAT_ID = get_credentials()
    application = ApplicationBuilder().token(TOKEN).build()

    try:
        await monitor_notifications(application, CHAT_ID, OCR_API_KEY)
    finally:
        await application.shutdown()

if __name__ == "__main__":
    asyncio.run(main())