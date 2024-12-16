# Taken from megadlbot_oss <https://github.com/eyaadh/megadlbot_oss/blob/master/mega/webserver/routes.py>
# Thanks to Eyaadh <https://github.com/eyaadh>
# Credit @LazyDeveloper.
# Please Don't remove credit.
# Born to make history @LazyDeveloper !
# Thank you LazyDeveloper for helping us in this Journey
# 🥰  Thank you for giving me credit @LazyDeveloperr  🥰
# for any error please contact me -> telegram@LazyDeveloperr or insta @LazyDeveloperr 


import re
import math
import logging
import secrets
import time
import mimetypes
from aiohttp import web
from aiohttp.http_exceptions import BadStatusLine
from lazybot import multi_clients, work_loads, lazydeveloperxbot
from server.exceptions import FIleNotFound, InvalidHash
from zzint import StartTime, __version__
from util.custom_dl import ByteStreamer
from util.time_format import get_readable_time
from util.render_template import render_page, render_lazydeveloper
from config import *
from util.file_properties import get_file_ids

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response(
        {
            "server_status": "running",
            "uptime": get_readable_time(time.time() - StartTime),
            "telegram_bot": "@" + lazydeveloperxbot.username,
            "connected_bots": len(multi_clients),
            "loads": dict(
                ("bot" + str(c + 1), l)
                for c, (_, l) in enumerate(
                    sorted(work_loads.items(), key=lambda x: x[1], reverse=True)
                )
            ),
            "version": __version__,
        }
    )

@routes.get(r"/watch/{path:\S+}", allow_head=True)
async def stream_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
        if match:
            secure_hash = match.group(1)
            id = int(match.group(2))
        else:
            id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
            secure_hash = request.rel_url.query.get("hash")
        return web.Response(text=await render_page(id, secure_hash, page_type="req"), content_type='text/html')
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FIleNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        pass
    except Exception as e:
        logging.critical(e.with_traceback(None))
        raise web.HTTPInternalServerError(text=str(e))
    
@routes.get(r"/embed/{path:\S+}", allow_head=True)
async def embed_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
        if match:
            secure_hash = match.group(1)
            id = int(match.group(2))
        else:
            id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
            secure_hash = request.rel_url.query.get("hash")
        return web.Response(text=await render_page(id, secure_hash, page_type="embed"), content_type='text/html')
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FIleNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        pass
    except Exception as e:
        logging.critical(e.with_traceback(None))
        raise web.HTTPInternalServerError(text=str(e))


# @routes.get(r"/play/{path:\S+}", allow_head=True)
# async def play_handler(request: web.Request):
#     """
#     Serve the play page for the provided stream or video URL.
#     """
#     try:
#         path = request.match_info["path"]

#         # Extract hash and ID from the path
#         match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
#         if match:
#             secure_hash = match.group(1)
#             id = int(match.group(2))
#         else:
#             id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
#             secure_hash = request.rel_url.query.get("hash")

#         # Validate the hash (ensure it matches the log_msg_id)
#         if not validate_hash(id, secure_hash):
#             raise web.HTTPForbidden(text="❌ Invalid or expired link.")

#         # Retrieve the URL from the stream logs
#         log_message = await lazydeveloperxbot.get_messages(int(STREAM_LOGS), message_ids=[id])
        
#         if not log_message or not log_message.text.startswith("http"):
#             raise web.HTTPNotFound(text="❌ URL not found or invalid.")

#         # Render the play.html with the retrieved URL
#         video_url = log_message.text.strip()
#         return web.Response(
#             text=await render_lazydeveloper(video_url),
#             content_type="text/html"
#         )

#     except Exception as e:
#         logging.critical(e, exc_info=True)
#         raise web.HTTPInternalServerError(text=f"❌ An error occurred: {str(e)}")


@routes.get(r"/{path:\S+}", allow_head=True)
async def stream_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
        if match:
            secure_hash = match.group(1)
            id = int(match.group(2))
        else:
            id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
            secure_hash = request.rel_url.query.get("hash")
        return await media_streamer(request, id, secure_hash)
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FIleNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        pass
    except Exception as e:
        logging.critical(e.with_traceback(None))
        raise web.HTTPInternalServerError(text=str(e))


@routes.get(r"/play/{unique_id}/{message_id}", allow_head=True)
async def play_handler(request: web.Request):
    """
    Validate the unique_id and serve the play page for the video URL.
    """
    try:
        # Extract unique_id and message_id from the URL
        unique_id = request.match_info["unique_id"]
        message_id = int(request.match_info["message_id"])

        # Retrieve the log message from the Stream Logs
        log_message = await lazydeveloperxbot.get_messages(STREAM_LOGS, message_ids=[message_id])

        # Check if the unique_id exists in the log message
        if not log_message or unique_id not in log_message.text:
            raise web.HTTPForbidden(text="❌ Invalid or expired link. Unique ID not found.")

        # Extract the URL from the log message
        lines = log_message.text.split("\n")
        target_url = lines[0].strip()  # the URL is the first line

        if not target_url.startswith("http"):
            raise web.HTTPNotFound(text="❌ URL not found or invalid.")

        # Render the play.html with the retrieved URL
        return web.Response(
            text=await render_lazydeveloper(target_url),
            content_type="text/html"
        )

    except Exception as e:
        logging.critical(e, exc_info=True)
        raise web.HTTPInternalServerError(text=f"❌ An error occurred: {str(e)}")

# @routes.get(r"/play/{path:\S+}", allow_head=True)
# async def play_handler(request: web.Request):
#     """
#     Serve the play page for the provided stream or video URL.
#     """
#     try:
#         path = request.match_info["path"]

#         # Extract hash and ID from the path
#         match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
#         if match:
#             secure_hash = match.group(1)
#             log_msg_id = int(match.group(2))
#         else:
#             log_msg_id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
#             secure_hash = request.rel_url.query.get("hash")

#         # Validate the hash (ensure it matches the log_msg_id)
#         if not validate_hash(log_msg_id, secure_hash):
#             raise web.HTTPForbidden(text="❌ Invalid or expired link.")

#         # Retrieve the URL from the stream logs
#         log_message = await lazydeveloperxbot.get_messages(int(STREAM_LOGS), message_ids=[log_msg_id])

#         if not log_message or not log_message.text.startswith("http"):
#             raise web.HTTPNotFound(text="❌ URL not found or invalid.")

#         # Render the play.html with the retrieved URL
#         video_url = log_message.text.strip()
#         return web.Response(
#             text=await render_page(video_url, page_type="play"),
#             content_type="text/html"
#         )

#     except Exception as e:
#         logging.critical(e, exc_info=True)
#         raise web.HTTPInternalServerError(text=f"❌ An error occurred: {str(e)}")

# @routes.get(r"/play/{log_msg_id}", allow_head=True)
# async def play_handler(request):
#     """
#     Serve the play page for the converted link.
#     """
#     log_msg_id = request.match_info["log_msg_id"]
#     secure_hash = request.rel_url.query.get("hash")

#     # Validate the hash or retrieve the original link
#     if not validate_hash(log_msg_id, secure_hash):  # Replace with your hash validation logic
#         return web.Response(text="❌ Invalid or expired link.", status=403)

#     # Retrieve the original link from STREAM_LOGS or other storage
#     original_link = user_links.get(int(log_msg_id))  # Replace with your storage logic

#     if not original_link:
#         return web.Response(text="❌ Could not retrieve the video link.", status=404)

#     # Populate the embed.html template with the video link
#     async with aiofiles.open('template/embed.html', mode="r") as template_file:
#         html_content = await template_file.read()

#     # Replace placeholders with dynamic content
#     html = html_content.replace("thefileislazydeveloper", original_link).replace(
#         "thenameislazydeveloper", "Stream Now"
#     )

#     return web.Response(text=html, content_type="text/html")
 
# @routes.get(r"/jwplayer/{url_hash}", allow_head=True)
# async def jwplayer_handler(request):
#     url_hash = request.match_info["url_hash"]

#     # Retrieve the video URL from the in-memory dictionary
#     video_url = client.jwplayer_urls.get(url_hash)
#     if not video_url:
#         return web.Response(text="❌ Invalid or expired link.", status=404)

#     # Load and modify the JWPlayer template
#     async with aiofiles.open("template/jwplayer.html", mode="r") as file:
#         html_content = await file.read()

#     # Replace the placeholder with the actual video URL
#     html_content = html_content.replace("{VIDEO_URL}", video_url)

#     return web.Response(text=html_content, content_type="text/html")


import aiofiles


class_cache = {}

async def media_streamer(request: web.Request, id: int, secure_hash: str):
    range_header = request.headers.get("Range", 0)
    
    index = min(work_loads, key=work_loads.get)
    faster_client = multi_clients[index]
    
    if MULTI_CLIENT:
        logging.info(f"Client {index} is now serving {request.remote}")

    if faster_client in class_cache:
        tg_connect = class_cache[faster_client]
        logging.debug(f"Using cached ByteStreamer object for client {index}")
    else:
        logging.debug(f"Creating new ByteStreamer object for client {index}")
        tg_connect = ByteStreamer(faster_client)
        class_cache[faster_client] = tg_connect
    logging.debug("before calling get_file_properties")
    file_id = await tg_connect.get_file_properties(id)
    logging.debug("after calling get_file_properties")
    
    if file_id.unique_id[:6] != secure_hash:
        logging.debug(f"Invalid hash for message with ID {id}")
        raise InvalidHash
    
    file_size = file_id.file_size

    if range_header:
        from_bytes, until_bytes = range_header.replace("bytes=", "").split("-")
        from_bytes = int(from_bytes)
        until_bytes = int(until_bytes) if until_bytes else file_size - 1
    else:
        from_bytes = request.http_range.start or 0
        until_bytes = (request.http_range.stop or file_size) - 1

    if (until_bytes > file_size) or (from_bytes < 0) or (until_bytes < from_bytes):
        return web.Response(
            status=416,
            body="416: Range not satisfiable",
            headers={"Content-Range": f"bytes */{file_size}"},
        )

    chunk_size = 1024 * 1024
    until_bytes = min(until_bytes, file_size - 1)

    offset = from_bytes - (from_bytes % chunk_size)
    first_part_cut = from_bytes - offset
    last_part_cut = until_bytes % chunk_size + 1

    req_length = until_bytes - from_bytes + 1
    part_count = math.ceil(until_bytes / chunk_size) - math.floor(offset / chunk_size)
    body = tg_connect.yield_file(
        file_id, index, offset, first_part_cut, last_part_cut, part_count, chunk_size
    )

    mime_type = file_id.mime_type
    file_name = file_id.file_name
    disposition = "attachment"

    if mime_type:
        if not file_name:
            try:
                file_name = f"{secrets.token_hex(2)}.{mime_type.split('/')[1]}"
            except (IndexError, AttributeError):
                file_name = f"{secrets.token_hex(2)}.unknown"
    else:
        if file_name:
            mime_type = mimetypes.guess_type(file_id.file_name)
        else:
            mime_type = "application/octet-stream"
            file_name = f"{secrets.token_hex(2)}.unknown"

    return web.Response(
        status=206 if range_header else 200,
        body=body,
        headers={
            "Content-Type": f"{mime_type}",
            "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
            "Content-Length": str(req_length),
            "Content-Disposition": f'{disposition}; filename="{file_name}"',
            "Accept-Ranges": "bytes",
        },
    )
