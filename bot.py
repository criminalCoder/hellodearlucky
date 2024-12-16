from aiohttp import web
from plugins import web_server

from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime

import asyncio
from pyrogram import idle
from lazybot import lazydeveloperxbot

from util.keepalive import ping_server
from lazybot.clients import initialize_clients

from config import *

import logging
import logging.config

PORT = "8080"
lazydeveloperxbot.start()
loop = asyncio.get_event_loop()

lazydeveloperxbot.LOGGER = LOGGER

async def lazyDeveloperStartBOT():
    print('\n')
    print('|==> Powered by - The one & Only LAZYDEVELOPER <==||')
    print('//// Initalizing Telegram Bot  ')
    usr_bot_me = await lazydeveloperxbot.get_me()
    lazydeveloperxbot.uptime = datetime.now()
    await initialize_clients()
    print('//// Processing basic inits....  ')
    print('================================  ')
    print('================================  ')

    try:
        db_channel = await lazydeveloperxbot.get_chat(CHANNEL_ID)
        lazydeveloperxbot.db_channel = db_channel
        test = await lazydeveloperxbot.send_message(chat_id = db_channel.id, text = "Test Message")
        await test.delete()
    except Exception as e:
        lazydeveloperxbot.LOGGER(__name__).warning(e)
        lazydeveloperxbot.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
        lazydeveloperxbot.LOGGER(__name__).info("\nBot Stopped. Join channel https://t.me/LazyDeveloper for support")
        # sys.exit() #if bot is admin & you are getting admin issue again and again then u can also remove this line of code 

    lazydeveloperxbot.set_parse_mode(ParseMode.HTML)
    print("[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[❤]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]")
    print("[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[❤]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]")
    print("[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[❤]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]")
    print(f"[||==> ❤ with love  llı🎉 L͙a͙z͙y͙D͙e͙v͙e͙l͙o͙p͙e͙r͙r͙ 🍿ıll with love ❤ <==||]")
    print("[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[❤]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]")
    print("[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[❤]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]")
    print("[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[❤]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]")
    lazydeveloperxbot.username = usr_bot_me.username
    #web-response
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    await idle()

if __name__ == '__main__':
    try:
        loop.run_until_complete(lazyDeveloperStartBOT())
        logging.info('=================================================================================')
        logging.info('=================================================================================')
        logging.info('-----------------------[x 🌎 x ==> Service running in Lazy Mode <== x 🧩 x]-----------------------')
        logging.info('=================================================================================')
        logging.info('=================================================================================')
    except KeyboardInterrupt:
        logging.info('-----------------------😜 Service Stopped Sweetheart 😝-----------------------')
