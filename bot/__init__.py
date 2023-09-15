from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from functions import Youtube_Extract


class Bot():
    def __init__(self, APPID, APPHASH, BOTTOKEN, Channel_name):
        self.Channel_name = Channel_name
        self.app = Client("youtubt_bot", bot_token=BOTTOKEN,
                          api_id=APPID, api_hash=APPHASH)

        @self.app.on_message(filters.command("start"))
        def start(client, message):
            message.reply_text(
                "Hello! I'm your bot.\nType /start  to get started.\n\nJust Send The Youtube Link and Get Download Link In Video & Audio.", quote=True)

        @self.app.on_message(filters.text)
        def text(client, message):
            text = message.text
            
            message_id = message.id
            chat_id = message.chat.id
            if self.CheckChatMembers(chat_id) == True:
                self.send_info_of_ytlink(text,chat_id,message_id)
            else:  # If chat_id isn't present in the list.
                        self.app.send_message(chat_id, text=f"Hey, **{message.chat.first_name}**\n\nYou haven't Joined Our Developer Channel.\n\nPlease ✅Join to continue The Process", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton("✅ Join", url="https://telegram.me/RaviRCoder"), InlineKeyboardButton(
                                    "Try Again", callback_data=f"JoinedCheckUser")],
                            ]
                        ))

        @self.app.on_callback_query()
        def callback_handle(client, callback_query):
            data = callback_query.data
            chat_id = callback_query.from_user.id
            text = callback_query.message.reply_to_message.text
            message_id = callback_query.message.id
            link_id = callback_query.message.reply_to_message_id
            if data in ["Get_Video", "Get_Audio"]:  # handle Get Requests
                self.app.delete_messages(chat_id, message_ids=message_id)
                self.get_download_link(data, text, chat_id, link_id)
            elif data == "JoinedCheckUser":
                 # If chat_id is present in the list.
                    if self.CheckChatMembers(chat_id=chat_id) == True:
                        self.app.delete_messages(chat_id,message_ids=[message_id])
                        callback_query.answer(text="Checked! You have joined✅")
                        self.send_info_of_ytlink(text,chat_id,link_id)

                    else:  # If chat_id isn't present in the list.
                        callback_query.answer(
                            text="Checked! You haven't joined✅")
            else:
                self.app.send_message(chat_id, text="Wrong Callback Query!")

    # start the bot
    def start(self):
        self.app.run()

    # checks the member is availabe or not in the channel or return True,False
    def CheckChatMembers(self, chat_id):
        members_chat_ids = [
            member.user.id for member in self.app.get_chat_members(self.Channel_name)]
        if chat_id in members_chat_ids:
            return True
        else:
            return False

    def send_info_of_ytlink(self,text,chat_id,message_id):
        youtube_links_text = ["youtu", "youtube"]
        if any(keyword in text for keyword in youtube_links_text):
                
            yt_data = Youtube_Extract(text).get_info()
            c = f"**Title** : {yt_data['Title']} \n**ID** : `{yt_data['Id']}` \n**Channel**: __{yt_data['Channel']}__ \n**Views** : {yt_data['Views']} \n**Length** : {yt_data['Length']} \n\nSelect Option to download!👇"
            try:
                self.app.send_photo(chat_id, photo=yt_data["Thumbnail"], caption=c, reply_to_message_id=message_id, reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Video", callback_data="Get_Video"), InlineKeyboardButton("Audio", callback_data="Get_Audio")]]))
            except:
                self.app.send_message("❌ This isn't Correct YouTube link, Send again❓")
        else:
            self.app.send_message("❌ This isn't a YouTube link, Send again❓")

    def get_download_link(self, query, text, chat_id, link_id):
        if query == "Get_Video":
            yt_data = Youtube_Extract(text).get_video()
            button = InlineKeyboardMarkup([[InlineKeyboardButton(
                label, url=yt_data[label]) for label in list(yt_data.keys())]])
            self.app.delete_messages(chat_id, message_ids=link_id)
            self.app.send_message(
                chat_id, text="Choose an option:", reply_markup=button)
        elif query == "Get_Audio":
            yt_data = Youtube_Extract(text).get_audio()

            keyboard_buttons = [
                [
                    InlineKeyboardButton(
                        label, url=yt_data[label])
                    for label in list(yt_data.keys())[i:i+2]
                ]
                for i in range(0, len(list(yt_data.keys())), 2)
            ]
            button = InlineKeyboardMarkup(keyboard_buttons)

            self.app.send_message(
                chat_id, text="Choose an option:", reply_markup=button)
            self.app.delete_messages(chat_id, message_ids=link_id)
