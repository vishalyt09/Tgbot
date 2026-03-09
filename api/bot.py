import telebot
from http.server import BaseHTTPRequestHandler
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7946633204:AAEV88u_QTOv_-GuzB23E7uHcYwFN6BMz8I"
CHANNEL = "@FFlikechannelV"
GROUP = "@FFLIKEGROUPV"

bot = telebot.TeleBot(TOKEN)

def joined(user_id):
    try:
        ch = bot.get_chat_member(CHANNEL, user_id)
        gp = bot.get_chat_member(GROUP, user_id)
        return ch.status in ["member","administrator","creator"] and gp.status in ["member","administrator","creator"]
    except:
        return False


@bot.message_handler(commands=['start'])
def start(msg):
    if joined(msg.from_user.id):
        bot.send_message(msg.chat.id,"✅ Verification Successful!")
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 Join Channel", url="https://t.me/yourchannel"))
        markup.add(InlineKeyboardButton("👥 Join Group", url="https://t.me/yourgroup"))
        markup.add(InlineKeyboardButton("✅ Verify", callback_data="verify"))

        bot.send_message(
            msg.chat.id,
            "⚠️ पहले Channel और Group join करें फिर Verify दबाएं",
            reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: call.data=="verify")
def verify(call):
    if joined(call.from_user.id):
        bot.edit_message_text(
            "✅ Verification complete!",
            call.message.chat.id,
            call.message.message_id
        )
    else:
        bot.answer_callback_query(call.id,"❌ Channel और Group join करें")


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        update = telebot.types.Update.de_json(body.decode("utf-8"))
        bot.process_new_updates([update])

        self.send_response(200)
        self.end_headers()
