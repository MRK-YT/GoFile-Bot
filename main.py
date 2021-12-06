# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/GoFile-Bot/blob/main/LICENSE

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from gofile import uploadFile


Bot = Client(
    "GoFile-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


@Bot.on_message(filters.private & filters.command("start"))
async def start(bot, update):
    await update.reply_text(
        text=f"Hello {update.from_user.mention},  I Can Generate Telegram File To Streaming Link And Direct Download Link.\n\nMade By @hb4all\n For More @HB4All_Bot",
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_message(filters.private & filters.media)
async def media_filter(bot, update):
    try:
        message = await update.reply_text(
            text="`Processing...`",
            quote=True,
            disable_web_page_preview=True
        )
        media = await update.download()
        await message.edit_text(
            text="`Downloading...`",
            disable_web_page_preview=True
        )
        response = uploadFile(media)
        await message.edit_text(
            text="`Uploading...`",
            disable_web_page_preview=True
        )
        try:
            os.remove(media)
        except:
            pass
    except Exception as error:
        await update.reply_text(
            text=f"Error :- <code>{error}</code>",
            quote=True,
            disable_web_page_preview=True
        )
        return
    text = f"**File Name:** `{response['fileName']}`" + "\n"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Watch", url=response['downloadPage']),
                InlineKeyboardButton(text="Download", url=response['directLink'])
            ],
            [
                InlineKeyboardButton(text="💥HB4All💥", url="https://t.me/HB4All")
            ]
        ]
    )
    await message.edit_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


Bot.run()
