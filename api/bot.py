import telebot
import threading
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7946633204:AAEV88u_QTOv_-GuzB23E7uHcYwFN6BMz8I"
CHANNEL = "@FFlikechannelV"
GROUP = "@FFLIKEGROUPV"
ADMIN_ID = 7727616420

bot = telebot.TeleBot(TOKEN)

# join check
def joined(user_id):
    try:
        ch = bot.get_chat_member(CHANNEL, user_id)
        gp = bot.get_chat_member(GROUP, user_id)

        if ch.status in ["member","administrator","creator"] and gp.status in ["member","administrator","creator"]:
            return True
        else:
            return False
    except:
        return False


@bot.message_handler(commands=['start'])
def start(msg):
    user_id = msg.from_user.id

    if joined(user_id):
        bot.send_message(msg.chat.id,"✅ Verification Successful!")
    else:
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("📢 Join Channel", url="https://t.me/yourchannel")
        )
        markup.add(
            InlineKeyboardButton("👥 Join Group", url="https://t.me/yourgroup")
        )
        markup.add(
            InlineKeyboardButton("✅ Verify", callback_data="verify")
        )

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


# auto promotion
def auto_promo():
    while True:
        try:
            bot.send_message(GROUP,"🔥 Join our channel for updates!")
        except:
            pass
        time.sleep(3600)

threading.Thread(target=auto_promo).start()


# admin panel
@bot.message_handler(commands=['admin'])
def admin(msg):
    if msg.from_user.id == ADMIN_ID:
        bot.send_message(msg.chat.id,
        "⚙️ Admin Panel\n\n/sendpromo - send promotion")


@bot.message_handler(commands=['sendpromo'])
def promo(msg):
    if msg.from_user.id == ADMIN_ID:
        bot.send_message(GROUP,"📢 Admin Promotion Message")


print("Bot Running...")
bot.infinity_polling()
