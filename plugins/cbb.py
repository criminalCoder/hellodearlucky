
from pyrogram import Client,filters, enums, __version__
# from bot import Bot
from config import STREAM_LOGS
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio
from urllib.parse import quote_plus
from util.file_properties import get_name, get_hash
from config import *
from html import escape
import hashlib
import hmac

# Define a secret key for hash generation (keep it private!)
SECRET_KEY = "theoneandonlylazydeveloper"  # Replace with a strong, unique key

# def generate_hash(log_msg_id):
#     """
#     Generate a secure hash for a given log message ID.
#     """
#     # Encode the log_msg_id and secret key
#     log_msg_id_bytes = str(log_msg_id).encode()
#     secret_key_bytes = SECRET_KEY.encode()

#     # Create the hash using HMAC with SHA256
#     hash_digest = hmac.new(secret_key_bytes, log_msg_id_bytes, hashlib.sha256).hexdigest()
#     return hash_digest[:10]  # Use the first 10 characters for compactness

# def generate_hash(message_id: int) -> str:
#     """
#     Generate a secure hash from the message ID.
#     """
#     # Convert the message ID to a string and hash it
#     return hashlib.sha256(str(message_id).encode('utf-8')).hexdigest()[:6]  # First 6 characters

def validate_hash(log_msg_id, provided_hash):
    """
    Validate the provided hash against the expected hash for the given log_msg_id.
    """
    # Generate the expected hash for the given log_msg_id
    expected_hash = generate_hash(log_msg_id)

    # Compare the provided hash with the expected hash
    return hmac.compare_digest(expected_hash, provided_hash)


def generate_hash(message_id: int) -> str:
    """
    Generate a secure hash from the message ID.
    """
    # Convert the message ID to a string and hash it
    return hashlib.sha256(str(message_id).encode('utf-8')).hexdigest()[:6]  # First 6 characters


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"○ Owner : <a href='https://t.me/ComanderAK'>۞ٖٖComⱥnᖙer 卂.Ԟ ۞ٖٖ</a>\n○ Dev : <a href='https://t.me/LazyDeveloperr'>❤LazyDeveloperr❤</a>\n○  Updates Channel: <a href='https://t.me/LazyDeveloper'> LazyDeveloper</a> </b>",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                    InlineKeyboardButton("⚡️ ᴄʟᴏsᴇ", callback_data = "close"),
                    InlineKeyboardButton('🍁 ᴘʀᴇᴍɪᴜᴍ', url='https://t.me/ComanderAK')
                    ]
                ]
            )
        )
    
    elif data.startswith("generate_stream_link"):
        # _, fileid = data.split(":")
        print("hit generate_stream_link callback")
        try:
            xo = await query.message.reply_text(f'🔐')
            user_id = query.from_user.id
            username =  query.from_user.mention 
            new_text = query.message.text
            print(f"new text => {new_text}")
            # Directly access the file from the callback query's associated message
            file = getattr(query.message.reply_to_message, query.message.reply_to_message.media.value)
            file_id = file.file_id
            # file_name = quote_plus(file.file_name)

            log_msg = await client.send_cached_media(
                chat_id=STREAM_LOGS, 
                file_id=file_id,
            )

            fileName = {quote_plus(get_name(log_msg))}
            lazy_stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
            lazy_download = f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"

            
            await asyncio.sleep(1)
            await xo.delete()

            await log_msg.reply_text(
                text=f"🍿 ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ  🧩\n\n<blockquote>{new_text}</blockquote>\n<blockquote>⏳Direct Download link:\n{lazy_download}</blockquote>\n<blockquote>📺Watch Online\n{lazy_stream}</blockquote>\n🧩User Id: {user_id} \n👮‍♂️ UserName: {username}",
                quote=True,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("web Download", url=lazy_download),  # we download Link
                                                    InlineKeyboardButton('▶Stream online', url=lazy_stream)]])  # web stream Link
            )
            
            await query.message.edit_text(
                text=f"🍿 ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ 🧩\n\n<blockquote>{new_text}</blockquote>\n<blockquote>⏳Direct Download link:\n{lazy_download}</blockquote>\n<blockquote>📺Watch Online\n{lazy_stream}</blockquote>",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("web Download", url=lazy_download),  # we download Link
                        InlineKeyboardButton('▶Stream online', url=lazy_stream)
                    ],
                    [
                        InlineKeyboardButton("<> Get EMBED code </>", callback_data="get_embed_code")
                    ]
                    ])  # web stream Link
            )
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"☣something went wrong sweetheart\n\n{e}", show_alert=True)
            return 
    
    elif data.startswith("get_embed_code"):
        # _, fileid, = data.split(":")
        # print('Hit me 1')
        try:
            xo = await query.message.reply_text(f'🔐')

            file = getattr(query.message.reply_to_message, query.message.reply_to_message.media.value)
            fileid = file.file_id

            log_msg = await client.send_cached_media(
                chat_id=STREAM_LOGS, 
                file_id=fileid,
            )

            fileName = {quote_plus(get_name(log_msg))}
            # print(f'Hit me 1 {fileName}')
            
            # Generate the embed URL
            lazy_embed = f"{URL}embed/{str(log_msg.id)}?hash={get_hash(log_msg)}"
            print(f'Hit me 1 = {lazy_embed}')
            # Create the HTML embed code
            embed_code = f"""
<div style="position: relative; padding-bottom: 56.25%; height: 0">
    <iframe
        src='{lazy_embed}'
        scrolling="no"
        frameborder="0"
        webkitallowfullscreen
        mozallowfullscreen
        allowfullscreen
        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%">
    </iframe>
</div>
            """
            print(f'Hit me 1 {embed_code}')
            escaped_embed_code = escape(embed_code)  # Escapes special characters
            # Send the embed code to the user
            await asyncio.sleep(1)
            await xo.delete()

            await query.message.reply_text(
                text=f"👩‍💻 Here is your embed code:\n\n<blockquote><code>{escaped_embed_code}</code></blockquote>",
                quote=True,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception as e:
            print(e)
            await query.answer(f"☣ Unable to generate embed code\n\n{e}", show_alert=True)
    
    elif data.startswith("convert_link"):
        try:
            xo = await query.message.reply_text(f'🔐')
            
            original_link = query.message.reply_to_message
            
            # urls = original_link.
             # Check if the user replied to a message

            print(f"{original_link}")

            log_msg = await client.send_message(
                chat_id=STREAM_LOGS, 
                text=f"{original_link.text}",
            )

            await asyncio.sleep(1)
            await xo.delete()
            secure_hash = generate_hash(log_msg.id)
            print(f"generated secure hash ==> {secure_hash}")
            await asyncio.sleep(1)
            target_url = original_link.text
            unique_id = secure_hash
            await log_msg.edit_text(f"{target_url}\n\nunique_id = {unique_id}")
            stream_url = f"{URL}play/{unique_id}/{log_msg.id}"

            await query.message.edit(
                text=f"✅ Your streamable link is ready:\n\n🔗 Watch Now => {stream_url}",
                quote=True,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
            await asyncio.sleep(1)
            await client.send_message(
                    chat_id=STREAM_LOGS,
                    text=f"✅ Converted Link for User:\n🔗 Original: {original_link}\n🌐 Stream: {stream_url}"
                )
            
            await query.answer("✅ Link converted successfully!")
        except Exception as e:
            print(e)
            await query.answer(f"☣ Unable to generate  link\n\n{e}", show_alert=True)

    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

