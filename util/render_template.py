# Credit @LazyDeveloper.
# Please Don't remove credit.
# Born to make history @LazyDeveloper !
# Thank you LazyDeveloper for helping us in this Journey
# 🥰  Thank you for giving me credit @LazyDeveloperr  🥰
# for any error please contact me -> telegram@LazyDeveloperr or insta @LazyDeveloperr 
# rip paid developers 🤣 - >> No need to buy paid source code while @LazyDeveloperr is here 😍😍
from config import *
from lazybot import lazydeveloperxbot
from util.human_readable import humanbytes
from util.file_properties import get_file_ids
from server.exceptions import InvalidHash
import urllib.parse
import aiofiles
import logging
import aiohttp

# to render cricket links
async def render_lazydeveloper(video_url):
    """
    Render an HTML page for the given video URL and page type.
    """
    # Load the play.html template
    async with aiofiles.open("template/lazyplaycricks.html", mode="r") as r:
        html_content = await r.read()

    # Replace placeholders in the HTML template
    heading = "Powered by LazyDeveloper"
    print(f"📺Here is video url ==> {video_url}")
    html = html_content.replace("thenameislazydeveloper", heading).replace("thefileislazydeveloper", video_url)

    return html

# to render online video 
async def render_page(id, secure_hash, page_type,):
    file_data=await get_file_ids(lazydeveloperxbot, int(STREAM_LOGS), int(id))
    if file_data.unique_id[:6] != secure_hash:
        logging.debug(f'link hash: {secure_hash} - {file_data.unique_id[:6]}')
        logging.debug(f"Invalid hash for message with - ID {id}")
        raise InvalidHash
    
    lazydevelopersrc = urllib.parse.urljoin(URL, f'{secure_hash}{str(id)}')
    if str(file_data.mime_type.split('/')[0].strip()) == 'video':
        if page_type=="req":
            async with aiofiles.open('template/req.html') as r:
                heading = 'Watch {}'.format(file_data.file_name)
                tag = file_data.mime_type.split('/')[0].strip()
                html = (await r.read()).replace('tag', tag) % (heading, file_data.file_name, lazydevelopersrc)
        
        if page_type=="embed":
            async with aiofiles.open('template/embed.html') as r:
                heading = 'Watch {}'.format(file_data.file_name)
                tag = file_data.mime_type.split('/')[0].strip()
                html = (await r.read()).replace('thenameislazydeveloper', heading).replace('thefileislazydeveloper', lazydevelopersrc)

    elif str(file_data.mime_type.split('/')[0].strip()) == 'audio':
        if page_type=="req":
            async with aiofiles.open('template/req.html') as r:
                heading = 'Listen {}'.format(file_data.file_name)
                tag = file_data.mime_type.split('/')[0].strip()
                html = (await r.read()).replace('tag', tag) % (heading, file_data.file_name, lazydevelopersrc)
        if page_type=="embed":
            async with aiofiles.open('template/embed.html') as r:
                heading = 'Listen {}'.format(file_data.file_name)
                tag = file_data.mime_type.split('/')[0].strip()
                html = (await r.read()).replace('thenameislazydeveloper', heading).replace('thefileislazydeveloper', lazydevelopersrc)
    else:
        async with aiofiles.open('template/dl.html') as r:
            async with aiohttp.ClientSession() as s:
                async with s.get(lazydevelopersrc) as u:
                    heading = 'Download {}'.format(file_data.file_name)
                    file_size = humanbytes(int(u.headers.get('Content-Length')))
                    html = (await r.read()) % (heading, file_data.file_name, lazydevelopersrc, file_size)
    return html
