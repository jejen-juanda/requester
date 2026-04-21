import os
from telegram.ext import Updater, CommandHandler
from Globals import token, id, incorrect, null, deleted
from functions.encryption import Encryption as enc

def telegram_creview(update, context):
    # Memastikan hanya Admin yang dapat mengeksekusi perintah
    if str(update.message.chat_id) != str(id):
        return

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
    if str(update.message.chat_id) != str(id):
        return

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
    if str(update.message.chat_id) != str(id):
        return

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

def mulai_pendengar():
    """Fungsi untuk menginisialisasi dan menjalankan thread listener Telegram"""
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("creview", telegram_creview))
    dp.add_handler(CommandHandler("ureview", telegram_ureview))
    dp.add_handler(CommandHandler("remove", telegram_remove))
    
    updater.start_polling()