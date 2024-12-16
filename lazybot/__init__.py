
from pyrogram import Client

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, CHANNEL_ID, PORT


class LazyDeveloperBot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    # async def start(self):
    #     await super().start()
    #     usr_bot_me = await self.get_me()
    #     self.uptime = datetime.now()

    #     try:
    #         db_channel = await self.get_chat(CHANNEL_ID)
    #         self.db_channel = db_channel
    #         test = await self.send_message(chat_id = db_channel.id, text = "Test Message")
    #         await test.delete()
    #     except Exception as e:
    #         self.LOGGER(__name__).warning(e)
    #         self.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
    #         self.LOGGER(__name__).info("\nBot Stopped. Join channel https://t.me/LazyDeveloper for support")
    #         sys.exit() #if bot is admin & you are getting admin issue again and again then u can also remove this line of code 

    #     self.set_parse_mode(ParseMode.HTML)
    #     self.LOGGER(__name__).info(f"Bot Running..!\n\n❤ with love  \n ıllıllı🚀🌟 L͙a͙z͙y͙D͙e͙v͙e͙l͙o͙p͙e͙r͙r͙ 🌟🚀ıllıllı")
    #     self.username = usr_bot_me.username
    #     #web-response
    #     app = web.AppRunner(await web_server())
    #     await app.setup()
    #     bind_address = "0.0.0.0"
    #     await web.TCPSite(app, bind_address, PORT).start()

    # async def stop(self, *args):
    #     await super().stop()
    #     self.LOGGER(__name__).info("Bot stopped.")
            

multi_clients = {}
work_loads = {}
lazydeveloperxbot = LazyDeveloperBot()















#     # Credit @LazyDeveloper.
#     # Please Don't remove credit.
#     # Born to make history @LazyDeveloper !

#     # Thank you LazyDeveloper for helping us in this Journey
#     # 🥰  Thank you for giving me credit @LazyDeveloperr  🥰

#     # for any error please contact me -> telegram@LazyDeveloperr or insta @LazyDeveloperr 
# import logging
# import logging.config
# logging.config.fileConfig('logging.conf')
# logging.getLogger().setLevel(logging.INFO)
# logging.getLogger("pyrogram").setLevel(logging.ERROR)
# logging.getLogger("imdbpy").setLevel(logging.ERROR)
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )
# logging.getLogger("aiohttp").setLevel(logging.ERROR)
# logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

# from pyrogram import Client

# from pyrogram import Client
# from configs import Config
# from configs import *


# Bot = Client(
#     name=Config.BOT_USERNAME,
#     in_memory=True,
#     bot_token=Config.BOT_TOKEN,
#     api_id=Config.API_ID,
#     api_hash=Config.API_HASH,
#     sleep_threshold=5,
#     workers=50,
# )
# multi_clients = {}
# work_loads = {}

