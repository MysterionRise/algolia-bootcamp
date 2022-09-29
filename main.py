import asyncio
import logging
import sqlite3

from settings import TOKEN
from telegram import ForceReply, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

DB_NAME = "tickets-{}.db"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued and create db"""
    con = sqlite3.connect(DB_NAME.format(update.message.chat.id))
    con.execute("CREATE TABLE IF NOT EXISTS users (name, score)")
    con.commit()
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued"""
    await update.message.reply_text("Help!")


def process_message(msg):
    if "biletik" in msg:
        words = msg.split(" ")
        pos = words.index("biletik")
        if pos != -1 and pos + 1 < len(words):
            user = words[pos + 1]
            return user
    return None


async def ticket_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Try to parse message and assign ticket respectively"""
    msg = update.message.text
    # chat_id = update.message.chat.id
    user = process_message(msg)

    # TODO need to find if user is part of chat?
    if user is not None and user.startswith("@"):
        con = sqlite3.connect(DB_NAME.format(update.message.chat.id))
        con.execute(
            "INSERT OR IGNORE INTO users (name, score) VALUES ('{}', 0)".format(user)
        )
        con.execute(f"UPDATE users SET score = score + 100 WHERE name='{user}'")
        con.commit()
        await update.message.reply_text(f"Assigned ticket to {user}")
    else:
        await update.message.reply_text("Not identified! Try again!")


def get_top_users(chat_id: int):
    con = sqlite3.connect(DB_NAME.format(chat_id))
    top_users = con.execute("SELECT name, score FROM users ORDER BY score desc")
    return top_users.fetchall()


async def top(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get top users based on the tickets"""
    await update.message.reply_text(get_top_users(update.message.chat.id))


def main() -> None:
    """Start the bot."""
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("top", top))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, ticket_handler)
    )

    application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
