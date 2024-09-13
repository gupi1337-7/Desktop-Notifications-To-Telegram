import time
import asyncio
from pywinauto import Desktop
from telegram import Bot
from telegram.error import TelegramError
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder



def get_credentials():
    token = input("Enter your Telegram Bot Token: ")
    chat_id = input("Enter your Telegram User ID: ")
    return token, chat_id



async def send_telegram_message(application, chat_id, message):
    try:
        await application.bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)
        print("Message successfully sent")
        return True
    except TelegramError as e:
        print(f"Error when sending a message: {e}")

        await asyncio.sleep(1)
        try:
            await application.bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)
            print("Message sent successfully after retrying")
            return True
        except TelegramError as e:
            print(f"A second attempt to send the message failed: {e}")
            return False



async def monitor_notifications(application, chat_id):
    print("I'm starting to monitor system notifications...")
    last_notification_time = 0

    while True:
        current_time = time.time()


        if current_time - last_notification_time < 30:
            await asyncio.sleep(1)
            continue


        windows = Desktop(backend="uia").windows()

        for window in windows:
            window_text = window.window_text()


            if 'notification' in window.window_text().lower() or "Новое уведомление" in window_text:
                message = f"<b>NEW MESSAGE?</b>\n{window_text}"
                success = await send_telegram_message(application, chat_id, message)
                if success:
                    last_notification_time = current_time
                    print(f"Waiting 30 seconds before the next notification...")
                    break

        await asyncio.sleep(1)


async def main():
    token, chat_id = get_credentials()
    application = ApplicationBuilder().token(token).build()

    try:
        await monitor_notifications(application, chat_id)
    finally:
        await application.shutdown()


if __name__ == "__main__":
    asyncio.run(main())