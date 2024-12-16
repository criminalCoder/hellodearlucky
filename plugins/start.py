import os, asyncio, humanize
from pyrogram import Client, filters, enums, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait,ChatAdminRequired, UserIsBlocked, InputUserDeactivated
# from bot import Bot
from config import *
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user, add_admin_id, get_admin_ids, remove_admin_id
logger = logging.getLogger(__name__)

neha_delete_time = FILE_AUTO_DELETE
neha = neha_delete_time
file_auto_delete = humanize.naturaldelta(neha)

@Client.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except Exception as e:
            print(f"Error adding user: {e}")
            pass
    
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except IndexError:
            return

        string = await decode(base64_string)
        argument = string.split("-")
        
        ids = []
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
            except Exception as e:
                print(f"Error decoding IDs: {e}")
                return

        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except Exception as e:
                print(f"Error decoding ID: {e}")
                return

        temp_msg = await message.reply("Wait A Sec..")
        try:
            messages = await get_messages(client, ids)
        except Exception as e:
            await message.reply_text("Something Went Wrong..!")
            print(f"Error getting messages: {e}")
            return
        finally:
            await temp_msg.delete()

        lazy_msgs = []  # List to keep track of sent messages

        for msg in messages:
            caption = (CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, 
                                             filename=msg.document.file_name) if bool(CUSTOM_CAPTION) and bool(msg.document)
                       else ("" if not msg.caption else msg.caption.html))
            # print(f"msg ==> {msg}")
            reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None
            # reply_markup = InlineKeyboardMarkup(
            #                 [
            #                 [InlineKeyboardButton("📂Downolad / Stream🍿", callback_data=f'downstreamlink:{msg.document.file_id}')],
            #                 [InlineKeyboardButton("<> Get EMBED code </>", callback_data=f'embedcode:{msg.document.file_id}')]
            #                 ]
            #                 )
            try:
                copied_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, 
                                            reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                lazy_msgs.append(copied_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                copied_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, 
                                            reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                lazy_msgs.append(copied_msg)
            except Exception as e:
                print(f"Failed to send message: {e}")
                pass

        k = await client.send_message(chat_id=message.from_user.id, 
                                      text=f"<b><i>This File is deleting automatically in {file_auto_delete}. Forward in your Saved Messages..!</i></b>")

        # Schedule the file deletion
        asyncio.create_task(delete_files(lazy_msgs, client, k))

        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('⚡️ ᴍᴏᴠɪᴇs', url='https://t.me/LazyDeveloper'),
                    InlineKeyboardButton('🍁 sᴇʀɪᴇs', url='https://telegram.me/LazyDeveloper')
                ],
                [
                    InlineKeyboardButton('🍿.  ᴀɴɪᴍᴇ  .🚀', url='https://telegram.me/LazyDeveloper')
                ]
            ]
        )
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
        return

@Client.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    try:
        invite_link = await client.create_chat_invite_link(int(FORCE_SUB_CHANNEL), creates_join_request=True)
        invite_link2 = await client.create_chat_invite_link(int(FORCE_SUB_CHANNEL2), creates_join_request=True)
    except ChatAdminRequired:
        logger.error("Hey Sona, Ek dfa check kr lo ki auth Channel mei Add hu ya nhi...!")
        return
    buttons = [
        [
            InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=invite_link.invite_link),
            InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=invite_link2.invite_link),
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='ʀᴇʟᴏᴀᴅ',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )

@Client.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Client, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=f"Processing...")
    users = await full_userbase()
    await msg.edit(f"{len(users)} Users Are Using This Bot")

@Client.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Client, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except Exception as e:
                print(f"Failed to send message to {chat_id}: {e}")
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u></b>

<b>Total Users :</b> <code>{total}</code>
<b>Successful :</b> <code>{successful}</code>
<b>Blocked Users :</b> <code>{blocked}</code>
<b>Deleted Accounts :</b> <code>{deleted}</code>
<b>Unsuccessful :</b> <code>{unsuccessful}</code>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(f"Use This Command As A Reply To Any Telegram Message Without Any Spaces.")
        await asyncio.sleep(8)
        await msg.delete()

# Function to handle file deletion
async def delete_files(messages, client, k):
    await asyncio.sleep(FILE_AUTO_DELETE)  # Wait for the duration specified in config.py
    
    for msg in messages:
        try:
            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except Exception as e:
            print(f"The attempt to delete the media {msg.id} was unsuccessful: {e}")

    # Safeguard against k.command being None or having insufficient parts
    command_part = k.command[1] if k.command and len(k.command) > 1 else None

    if command_part:
        button_url = f"https://t.me/{client.username}?start={command_part}"
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ ᴀɢᴀɪɴ!", url=button_url)]
            ]
        )
    else:
        keyboard = None

    # Edit message with the button
    await k.edit_text("<b><i>Your Video / File Is Successfully Deleted ✅</i></b>", reply_markup=keyboard)

# ????????????????????????????????????????????????????????///
@Client.on_message(filters.private & filters.command("add_admin"))
async def set_admin(client, message: Message):
    user_id = message.from_user.id
    lazyid = message.from_user.id
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except Exception as e:
            print(f"Error adding user: {e}")
            pass

    if user_id not in OWNERS:
        return await message.reply("🤚Hello bro, This command is only for owners.")

    if not await verify_user(lazyid):
        return await message.reply("⛔ You are not authorized to use this bot.")

    # Ask the user for the channel ID
    admin_msg = await client.ask(
        user_id, 
        "🧩 Please send the `admin_id` you want to add to admins list:", 
        filters=filters.text
    )

    # Validate the channel ID
    try:
        admin_id = int(admin_msg.text)
    except ValueError:
        return await admin_msg.reply("❌ Invalid Admin ID. Please send a valid Admin ID.")

    # Check if the channel ID is already in the user's list
    adminlists = await get_admin_ids()
    if admin_id in adminlists:
        return await admin_msg.reply(f"🆔 Admin ID {admin_id} is already in your list. Please send another ID.")

    # Add the Admin ID to the user's list using the existing database method

    await add_admin_id(admin_id)

    await admin_msg.reply(f"🧩 Admin ID {admin_id} has been added successfully to Admin list.")

@Client.on_message(filters.private & filters.command("remove_admin"))
async def remove_admin(client, message: Message):
    user_id = message.from_user.id
    lazyid = message.from_user.id
    if not await present_user(user_id):
        try:
            await add_user(user_id)
        except Exception as e:
            print(f"Error adding user: {e}")
            pass

    if user_id not in OWNERS:
        return await message.reply("🤚Hello bro, This command is only for owners.")

    if not await verify_user(lazyid):
        return await message.reply("⛔ You are not authorized to use this bot.")
    
    # Extract the channel_id from the message text
    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply("🆘 Usage: `/remove_admin <admin_id>` to remove from \n\n❌ Please provide a `admin_id` to remove.")

    try:
        admin_id = int(parts[1])
    except ValueError:
        return await message.reply("❌ Invalid Admin ID. Please provide a valid numeric ID.")

        # Check if the channel ID is already in the user's list
    adminlists = await get_admin_ids()
    if admin_id not in adminlists:
        return await message.reply(f"🧩 Admin ID {admin_id} not found in database 👎.\n\n❌ Please send another valid ID to remove.")

    # Remove the channel ID from the user's list using the existing database method
    await remove_admin_id(admin_id)
    
    await message.reply(f"🚮 Admin ID {admin_id} has been removed successfully.")

@Client.on_message(filters.private & filters.command("view_admin_list"))
async def list_admins(client, message: Message):
    user_id = message.from_user.id
    lazyid = message.from_user.id
    
    if not await present_user(user_id):
        try:
            await add_user(user_id)
        except Exception as e:
            print(f"Error adding user: {e}")
            pass

    if user_id not in OWNERS:
        return await message.reply("🤚Hello bro, This command is only for owners.")

    if not await verify_user(lazyid):
        return await message.reply("⛔ You are not authorized to use this bot.")
    
    # Get the list of channel IDs from the database
    admin_ids = await get_admin_ids()

    if not admin_ids:
        return await message.reply("❌ You don't have any Admin IDs saved yet.")

    # Format the list of channel IDs and send it to the user
    admin_list = "\n├🆔 ".join([str(admin_id) for admin_id in admin_ids])
    await message.reply(f"🧩 Your saved Admin IDs:\n├🆔 {admin_list}", parse_mode=enums.ParseMode.HTML)

# ///////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////
async def verify_user(user_id: int):
    LAZYLISTS = await get_admin_ids()
    return user_id in ADMINS or user_id in LAZYLISTS

