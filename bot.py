# Bot by @BeastX_Bots


import logging
import asyncio
from telethon import TelegramClient, events, Button
from decouple import config
from telethon.tl.functions.users import GetFullUserRequest

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

# start the bot
print("Starting...")
try:
    apiid = config("APP_ID", cast=int)
    apihash = config("API_HASH")
    bottoken = config("BOT_TOKEN")
    frm = config("FROM_CHANNEL", cast=int)
    tochnl = config("TO_CHANNEL", cast=int)
    beast = TelegramClient('bot', apiid, apihash).start(bot_token=bottoken)
except:
    print("Environment vars are missing! Kindly recheck.")
    print("Bot is quiting...")
    exit()


@beast.on(events.NewMessage(pattern="/start"))
async def _(event):
    sed = await beast(GetFullUserRequest(event.sender_id))
    await event.reply(f"Hi `{sed.user.first_name}`!\n\nI am a channel auto-post bot!! Read /help to know more!\n\nI can be used in only two channels (one user) at a time. Kindly deploy your own bot.\n\n[More bots](https://t.me/BeastX_Bots)..", buttons=[Button.url("Repo", url="https://github.com/msy1717/AutoPostChannel"), Button.url("Dev", url="https://t.me/Godmrunal")], link_preview=False)


@beast.on(events.NewMessage(pattern="/help"))
async def helpp(event):
    await event.reply("**Help**\n\nThis bot will send all new posts in one channel to the other channel. (without forwarded tag)!\nIt can be used only in two channels at a time, so kindly deploy your own bot from [here](https://github.com/msy1717/AutoPostChannel).\n\nAdd me to both the channels and make me an admin in both, and all new messages would be autoposted on the linked channel!!\")

@beast.on(events.NewMessage(incoming=True, chats=frm)) 
async def _(event): 
    if not event.is_private:
        try:
            if event.poll:
                return
            if event.photo:
                photo = event.media.photo
                await beast.send_file(tochnl, photo, caption = event.text, link_preview = False)
            elif event.media:
                try:
                    if event.media.webpage:
                        await beast.send_message(tochnl, event.text, link_preview = False)
                        return
                except:
                    media = event.media.document
                    await beast.send_file(tochnl, media, caption = event.text, link_preview = False)
                    return
            else:
                await beast.send_message(tochnl, event.text, link_preview = False)
        except:
            print("TO_CHANNEL ID is wrong or I can't send messages there (make me admin).")


print("Bot has started.")
print("----------------------------------------------")
print("                @BeastX_Bots                  ")
print("----------------------------------------------")

beast.run_until_disconnected()
