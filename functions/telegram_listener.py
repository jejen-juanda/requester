import os
import logging
from telegram.ext import Updater, CommandHandler
from Globals import token, id, incorrect, null, deleted, empty, cleared, bantuan, admin
from functions.encryption import Encryption as enc

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def telegram_creview(update, context):
    chat_id = update.effective_chat.id
    if str(chat_id) != str(id): return

    args = context.args
    if not args:
        update.message.reply_text(incorrect)
        return

    nickname = " ".join(args)
    try:
        with open(f"requests/channel-requests/{nickname}.request", "rb") as file:
            info = file.read()
        
        text = enc.decrypt(info).decode()
        info = text.split(",")
        pesan_balasan = f"Detail Channel:\n- Nama: {info[0]}\n- Password: {info[1]}\n- Op Password: {info[2]}\n- Topik: {info[3]}"
        update.message.reply_text(pesan_balasan)
    except FileNotFoundError:
        update.message.reply_text(null)

def telegram_ureview(update, context):
    chat_id = update.effective_chat.id
    if str(chat_id) != str(id): return

    args = context.args
    if not args:
        update.message.reply_text(incorrect)
        return

    nickname = " ".join(args)
    try:
        with open(f"requests/user-account-requests/{nickname}.request", "rb") as file:
            info = file.read()
            
        text = enc.decrypt(info).decode()
        info = text.split(",")
        pesan_balasan = f"Detail Akun:\n- Username: {info[0]}\n- Password: {info[1]}\n- Nama: {info[2]}"
        update.message.reply_text(pesan_balasan)
    except FileNotFoundError:
        update.message.reply_text(null)

def telegram_remove(update, context):
    chat_id = update.effective_chat.id
    if str(chat_id) != str(id): return

    args = context.args
    if len(args) < 2:
        update.message.reply_text(incorrect)
        return

    kategori = args[0]
    nickname = " ".join(args[1:])

    if kategori == "channel-requests":
        path_file = f"requests/channel-requests/{nickname}.request"
    elif kategori == "user-account-requests":
        path_file = f"requests/user-account-requests/{nickname}.request"
    else:
        update.message.reply_text(incorrect)
        return

    if os.path.isfile(path_file):
        os.remove(path_file)
        update.message.reply_text(deleted)
    else:
        update.message.reply_text(null)

def telegram_clear(update, context):
    chat_id = update.effective_chat.id
    if str(chat_id) != str(id): return

    args = context.args
    if not args:
        update.message.reply_text(incorrect)
        return

    kategori = args[0]
    if kategori == "channel-requests":
        for file in os.listdir("requests/channel-requests"):
            os.remove(f"requests/channel-requests/{file}")
        update.message.reply_text(cleared)
    elif kategori == "user-account-requests":
        for file in os.listdir("requests/user-account-requests"):
            os.remove(f"requests/user-account-requests/{file}")
        update.message.reply_text(cleared)
    elif kategori == "all":
        for file in os.listdir("requests/channel-requests"):
            os.remove(f"requests/channel-requests/{file}")
        for file in os.listdir("requests/user-account-requests"):
            os.remove(f"requests/user-account-requests/{file}")
        update.message.reply_text(cleared)
    else:
        update.message.reply_text(incorrect)

def telegram_check(update, context):
    chat_id = update.effective_chat.id
    if str(chat_id) != str(id): return

    channels = len(os.listdir("requests/channel-requests"))
    users = len(os.listdir("requests/user-account-requests"))
    update.message.reply_text(f"There are {channels} channel requests, and {users} user requests")

def telegram_see(update, context):
    chat_id = update.effective_chat.id
    if str(chat_id) != str(id): return

    args = context.args
    if not args:
        update.message.reply_text(incorrect)
        return

    kategori = args[0]
    if kategori == "channel-requests":
        filelist = os.listdir("requests/channel-requests")
        if filelist:
            balasan = "\n".join([os.path.splitext(i)[0] for i in filelist])
            update.message.reply_text(balasan)
        else:
            update.message.reply_text(empty)
    elif kategori == "user-account-requests":
        filelist = os.listdir("requests/user-account-requests")
        if filelist:
            balasan = "\n".join([os.path.splitext(i)[0] for i in filelist])
            update.message.reply_text(balasan)
        else:
            update.message.reply_text(empty)
    else:
        update.message.reply_text(incorrect)

def telegram_bantuan(update, context):
    chat_id = update.effective_chat.id
    if str(chat_id) != str(id): return
    
    update.message.reply_text(f"{bantuan}\n\n{admin}")

def mulai_pendengar():
    try:
        logger.info("Memulai inisialisasi bot Telegram (Versi 13) Lengkap...")
        updater = Updater(token, use_context=True)
        dp = updater.dispatcher
        
        dp.add_handler(CommandHandler("creview", telegram_creview))
        dp.add_handler(CommandHandler("ureview", telegram_ureview))
        dp.add_handler(CommandHandler("remove", telegram_remove))
        dp.add_handler(CommandHandler("clear", telegram_clear))
        dp.add_handler(CommandHandler("check", telegram_check))
        dp.add_handler(CommandHandler("see", telegram_see))
        dp.add_handler(CommandHandler("bantuan", telegram_bantuan))
        
        logger.info("Bot Telegram aktif dan siap merespons semua perintah!")
        updater.start_polling()
        
    except Exception as e:
        logger.error(f"GAGAL menjalankan Telegram: {e}")