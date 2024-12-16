from pyrogram import filters, enums, Client
from pyrogram.types import Message
# from bot import Bot




@Client.on_message(filters.command("id") & filters.private)
async def showid(client, message):
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        user_id = message.chat.id
        await message.reply_text(
            f"<b>Your User ID Is :</b> <code>{user_id}</code>", 
            quote=True
        )
