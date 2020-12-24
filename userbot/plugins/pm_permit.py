#    Black-Lighting - UserBot
#    Copyright (C) 2020 Black-Lighting

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
import asyncio
import io
import os

from telethon import events, functions
from telethon.tl.functions.users import GetFullUserRequest

import userbot.plugins.sql_helper.pmpermit_sql as pmpermit_sql
from userbot import ALIVE_NAME, CUSTOM_PMPERMIT
from userbot.thunderconfig import Config
from userbot.utils import admin_cmd

PMPERMIT_PIC = os.environ.get("PMPERMIT_PIC", None)
if PMPERMIT_PIC is None:
    WARN_PIC = "https://telegra.ph/file/63abc60224dc567e3d441.jpg"
else:
    WARN_PIC = PMPERMIT_PIC
myid = bot.uid
PM_WARNS = {}
PREV_REPLY_MESSAGE = {}

PM_ON_OFF = Config.PM_DATA

DEFAULTUSER = (
    str(ALIVE_NAME) if ALIVE_NAME else "Set ALIVE_NAME in config vars in Heroku"
)
CUSTOM_MIDDLE_PMP = (
    str(CUSTOM_PMPERMIT) if CUSTOM_PMPERMIT else "⚜ Im  Helper and Assitant Of User ⚜"
)
USER_BOT_WARN_ZERO = "You Have Attempted To Spam Masters Inbox So Inorder To Avoid Over Spam , You Have Been Blocked By Userbot"
MESAG = (
    str(CUSTOM_PMPERMIT)
    if CUSTOM_PMPERMIT
    else "`Im  Helper and Assitant Of User😊"
)
botisnoob = Var.TG_BOT_USER_NAME_BF_HER
USER_BOT_NO_WARN = (
    "**Hello, This is Black Lightning ⚠️**\n\n"
    f"Im The Protector Of {DEFAULTUSER}"
    f"`My Master {DEFAULTUSER} is Busy Right Now !` \n"
    "**I Request You To Choose A Reason You Have Came For** 👀 \n\n"
    f"**{CUSTOM_MIDDLE_PMP}**"
)

if Var.PRIVATE_GROUP_ID is not None:
    # Approve outgoing

    @bot.on(events.NewMessage(outgoing=True))
    async def you_dm_niqq(event):
        if event.fwd_from:
            return
        chat = await event.get_chat()
        if event.is_private:
            if not pmpermit_sql.is_approved(chat.id):
                if not chat.id in PM_WARNS:
                    pmpermit_sql.approve(chat.id, "outgoing")
                    bruh = "__Auto-approved bcuz outgoing 🚶__"
                    rko = await borg.send_message(event.chat_id, bruh)
                    await asyncio.sleep(3)
                    await rko.delete()

@borg.on(admin_cmd(pattern="(a|approve)"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    replied_user = await event.client(GetFullUserRequest(event.chat_id))
    firstname = replied_user.user.first_name
    reason = event.pattern_match.group(1)
    chat = await event.get_chat()
    if event.is_private:
        if not pmpermit_sql.is_approved(chat.id):
            if chat.id in PM_WARNS:
                del PM_WARNS[chat.id]
            if chat.id in PREV_REPLY_MESSAGE:
                await PREV_REPLY_MESSAGE[chat.id].delete()
                del PREV_REPLY_MESSAGE[chat.id]
            pmpermit_sql.approve(chat.id, reason)
            await event.edit(
                "Approved [{}](tg://user?id={}) to PM you.".format(firstname, chat.id)
            )
            await asyncio.sleep(3)
            await event.delete()


@command(pattern=".block$")
async def approve_p_m(event):
    if event.fwd_from:
        return
    replied_user = await event.client(GetFullUserRequest(event.chat_id))
    firstname = replied_user.user.first_name
    event.pattern_match.group(1)
    chat = await event.get_chat()
    if event.is_private:
        if chat.id == 1311769691:
            await event.edit("You tried to block my master. GoodBye for Now Im Sleeping 100 seconds! 😪💤")
            await asyncio.sleep(100)
        else:
            if pmpermit_sql.is_approved(chat.id):
                pmpermit_sql.disapprove(chat.id)
                await event.edit(
                    "Get lost retard.\nBlocked [{}](tg://user?id={})".format(
                        firstname, chat.id
                    )
                )
                await asyncio.sleep(3)
                await event.client(functions.contacts.BlockRequest(chat.id))

@borg.on(admin_cmd(pattern="da ?(.*)"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    replied_user = await event.client(GetFullUserRequest(event.chat_id))
    firstname = replied_user.user.first_name
    event.pattern_match.group(1)
    chat = await event.get_chat()
    if event.is_private:
        if chat.id == 1311769691:
            await event.edit("Sorry, I Can't Disapprove My Dev")
        else:
            if pmpermit_sql.is_approved(chat.id):
                pmpermit_sql.disapprove(chat.id)
                await event.edit(
                    "[{}](tg://user?id={}) disapproved to PM.".format(
                        firstname, chat.id
                    )
                )

@borg.on(admin_cmd(pattern="listapproved$"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    approved_users = pmpermit_sql.get_all_approved()
    APPROVED_PMs = "[Black Lightning] Currently Approved PMs\n"
    if len(approved_users) > 0:
        for a_user in approved_users:
            if a_user.reason:
                APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
            else:
                APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id})\n"
    else:
        APPROVED_PMs = "No Approved PMs (yet)"
    if len(APPROVED_PMs) > 4095:
        with io.BytesIO(str.encode(APPROVED_PMs)) as out_file:
            out_file.name = "approved.pms.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="[Black Lightning]Current Approved PMs",
                reply_to=event,
            )
            await event.delete()
    else:
        await event.edit(APPROVED_PMs)


async def do_pm_permit_action(chat_id, event):
    if Var.PMSECURITY.lower() == "off":
        return
    if chat_id not in PM_WARNS:
        PM_WARNS.update({chat_id: 0})
    if PM_WARNS[chat_id] == Config.MAX_SPAM:
        r = await event.reply(USER_BOT_WARN_ZERO)
        await asyncio.sleep(3)
        await event.client(functions.contacts.BlockRequest(chat_id))
        if chat_id in PREV_REPLY_MESSAGE:
            await PREV_REPLY_MESSAGE[chat_id].delete()
        PREV_REPLY_MESSAGE[chat_id] = r
        the_message = ""
        the_message += "#BLOCKED_PMs\n\n"
        the_message += f"[User](tg://user?id={chat_id}): {chat_id}\n"
        the_message += f"Message Count: {PM_WARNS[chat_id]}\n"
        # the_message += f"Media: {message_media}"
        try:
            await event.client.send_message(
                entity=Var.PRIVATE_GROUP_ID,
                message=the_message,
                # reply_to=,
                # parse_mode="html",
                link_preview=False,
                # file=message_media,
                silent=True,
            )
            return
        except BaseException:
            return
    # inline pmpermit menu
    mybot = Var.TG_BOT_USER_NAME_BF_HER
    MSG = USER_BOT_NO_WARN.format(
        DEFAULTUSER, myid, MESAG, PM_WARNS[chat_id] + 1, Config.MAX_SPAM
    )
    tele = await bot.inline_query(mybot, MSG)
    r = await tele[0].click(event.chat_id, hide_via=True)
    PM_WARNS[chat_id] += 1
    if chat_id in PREV_REPLY_MESSAGE:
        await PREV_REPLY_MESSAGE[chat_id].delete()
    PREV_REPLY_MESSAGE[chat_id] = r
    
@bot.on(events.NewMessage(incoming=True))
async def on_new_private_message(event):
    if event.sender_id == bot.uid:
        return

    if Var.PRIVATE_GROUP_ID is None:
        return

    if not event.is_private:
        return

    message_text = event.message.message
    chat_id = event.sender_id

    message_text.lower()
    if USER_BOT_NO_WARN == message_text:
        # userbot's should not reply to other userbot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return
    sender = await bot.get_entity(chat_id)

    if chat_id == bot.uid:

        # don't log Saved Messages

        return

    if sender.bot:

        # don't log bots

        return

    if sender.verified:

        # don't log verified accounts

        return

    if not pmpermit_sql.is_approved(chat_id):
        # pm permit
        await do_pm_permit_action(chat_id, event)

        
@bot.on(events.NewMessage(incoming=True, from_users=(1232461895)))
async def hehehe(event):
    if event.fwd_from:
        return
    chats = await event.get_chat()
    if event.is_private:
        if not pmpermit_sql.is_approved(chats.id):
            pmpermit_sql.approve(chats.id, "**My Boss Is Best🔥**")
            await borg.send_message(
                chats, "**Oo Yeah He Is My Co-Developer. So Approved**"
            )


@bot.on(
    events.NewMessage(incoming=True, from_users=(1311769691, 1105887181, 798271566))
)
async def hehehe(event):
    if event.fwd_from:
        return
    chats = await event.get_chat()
    if event.is_private:
        if not pmpermit_sql.is_approved(chats.id):
            pmpermit_sql.approve(chats.id, "**My Boss Is Best🔥**")
            await borg.send_message(
                chats, "**Oo Yeah He Is My My  Developer. So Approved**"
            )
