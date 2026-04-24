import os
import logging
from datetime import datetime
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Globals import token, id, incorrect, null, deleted, empty, cleared, bantuan, admin
from functions.encryption import Encryption as enc
from functions import keyboard 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def is_admin(chat_id):
    return str(chat_id) in str(id)

def save_tracking(category, nickname, status, admin_name):
    """Menyimpan jejak keputusan Admin ke folder tracking dengan enkripsi."""
    folder_map = {"channel": "channel-tracking", "user": "user-account-tracking"}
    path = f"tracking/{folder_map[category]}/{nickname}.track"    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data_text = f"{status},{admin_name},{time_now}"
    encrypted_data = enc.encrypt(data_text.encode())
    
    with open(path, "wb") as f:
        f.write(encrypted_data)

def telegram_creview(update, context):
    if not is_admin(update.effective_chat.id): return
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
        update.message.reply_text(f"Detail Channel:\n- Nama: {info[0]}\n- Password: {info[1]}\n- Op Password: {info[2]}\n- Topik: {info[3]}")
    except FileNotFoundError:
        update.message.reply_text(null)

def telegram_ureview(update, context):
    if not is_admin(update.effective_chat.id): return
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
        update.message.reply_text(f"Detail Akun:\n- Username: {info[0]}\n- Password: {info[1]}\n- Nama: {info[2]}")
    except FileNotFoundError:
        update.message.reply_text(null)

def telegram_remove(update, context):
    if not is_admin(update.effective_chat.id): return
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
    if not is_admin(update.effective_chat.id): return
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
    if not is_admin(update.effective_chat.id): return
    channels = len(os.listdir("requests/channel-requests"))
    users = len(os.listdir("requests/user-account-requests"))
    update.message.reply_text(f"There are {channels} channel requests, and {users} user requests")

def telegram_see(update, context):
    if not is_admin(update.effective_chat.id): return
    args = context.args
    if not args:
        update.message.reply_text(incorrect)
        return
    kategori = args[0]
    if kategori == "channel-requests":
        filelist = os.listdir("requests/channel-requests")
        if filelist:
            update.message.reply_text("\n".join([os.path.splitext(i)[0] for i in filelist]))
        else:
            update.message.reply_text(empty)
    elif kategori == "user-account-requests":
        filelist = os.listdir("requests/user-account-requests")
        if filelist:
            update.message.reply_text("\n".join([os.path.splitext(i)[0] for i in filelist]))
        else:
            update.message.reply_text(empty)
    else:
        update.message.reply_text(incorrect)

def telegram_bantuan(update, context):
    if not is_admin(update.effective_chat.id): return
    update.message.reply_text(f"{bantuan}\n\n{admin}")

def telegram_panel(update, context):
    if not is_admin(update.effective_chat.id): return
    update.message.reply_text("🎛 <b>Panel Kendali Utama</b>", reply_markup=keyboard.main_menu(), parse_mode='HTML')

def button_callback(update, context):
    if not is_admin(update.effective_chat.id): return
    query = update.callback_query
    query.answer()
    data = query.data
    admin_obj = update.effective_user
    admin_display_name = admin_obj.first_name or admin_obj.username or "Admin"

    try:
        if data == 'nav_main':
            query.edit_message_text("🎛 <b>Panel Kendali Utama</b>", reply_markup=keyboard.main_menu(), parse_mode='HTML')
        
        elif data.startswith('nav_'):
            action = data.split('_')[1]
            query.edit_message_text(f"Menu <b>{action.upper()}</b>:", reply_markup=keyboard.category_menu(action), parse_mode='HTML')
            
        elif data.startswith('cat_'):
            _, action, cat = data.split('_')
            query.edit_message_text(f"Daftar <b>{cat.title()}</b> ({action}):", reply_markup=keyboard.requester_list_menu(action, cat), parse_mode='HTML')

        elif data.startswith('act_'):
            _, action, cat, nick = data.split('_', 3)
            folder_map_req = {"channel": "channel-requests", "user": "user-account-requests"}
            folder_map_track = {"channel": "channel-tracking", "user": "user-account-tracking"}
            
            path_req = f"requests/{folder_map_req[cat]}/{nick}.request"
            path_track = f"tracking/{folder_map_track[cat]}/{nick}.track"

            if action == 'check':
                if os.path.exists(path_req):
                    pesan = f"🔍 <b>Status:</b> PENDING\n👤 <b>Requester:</b> {nick}\n\nKeterangan: Belum di-Review oleh siapapun."
                elif os.path.exists(path_track):
                    with open(path_track, "rb") as f:
                        track_raw = enc.decrypt(f.read()).decode().split(",")
                    status, adm, tm = track_raw
                    icon = "✅" if status == "APPROVED" else "❌"
                    pesan = f"{icon} <b>Status:</b> {status}\n👤 <b>Requester:</b> {nick}\n👮 <b>Admin:</b> {adm}\n⏰ <b>Waktu:</b> {tm}"
                else:
                    pesan = "❌ Data tidak ditemukan dalam sistem."
                query.edit_message_text(pesan, reply_markup=keyboard.back_button(f'cat_check_{cat}'), parse_mode='HTML')

            elif action == 'approve' and cat == 'user':
                server_tt = context.bot_data.get('tt_server')                
                if os.path.isfile(path_req):
                    with open(path_req, "rb") as f:
                        info = enc.decrypt(f.read()).decode().split(",")
                    
                    server_tt.new_account(username=info[0], password=info[1], note=f"By {admin_display_name}")
                    save_tracking(cat, nick, "APPROVED", admin_display_name) 
                    os.remove(path_req)
                    
                    query.edit_message_text(f"✅ Akun <b>{nick}</b> BERHASIL dibuat.", reply_markup=keyboard.back_button(f'cat_review_{cat}'), parse_mode='HTML')
                else:
                    query.edit_message_text(f"⚠️ <b>GAGAL:</b> File request untuk {nick} tidak terbaca atau sudah hilang!", reply_markup=keyboard.back_button(f'cat_review_{cat}'), parse_mode='HTML')

            elif action == 'clear': 
                if os.path.isfile(path_req):
                    save_tracking(cat, nick, "REJECTED", admin_display_name) 
                    os.remove(path_req)
                    query.edit_message_text(f"❌ Permintaan <b>{nick}</b> telah DITOLAK.", reply_markup=keyboard.back_button(f'cat_review_{cat}'), parse_mode='HTML')
                else:
                    query.edit_message_text(f"⚠️ <b>GAGAL:</b> File request untuk {nick} tidak terbaca!", reply_markup=keyboard.back_button(f'cat_review_{cat}'), parse_mode='HTML')

            elif action == 'review':
                if os.path.exists(path_req):
                    with open(path_req, "rb") as f:
                        info = enc.decrypt(f.read()).decode().split(",")
                    if cat == "user":
                        pesan = f"📖 <b>Review Akun:</b> {nick}\n- User: {info[0]}\n- Pass: {info[1]}\n- Nama: {info[2]}"
                        markup = InlineKeyboardMarkup([
                            [InlineKeyboardButton("✅ Approve", callback_data=f'act_approve_user_{nick}')],
                            [InlineKeyboardButton("❌ Reject", callback_data=f'act_clear_user_{nick}')],
                            [InlineKeyboardButton("🔙 Kembali", callback_data=f'cat_review_user')]
                        ])
                    else:
                        pesan = f"📖 <b>Review Channel:</b> {nick}\n- Nama: {info[0]}\n- Topic: {info[3]}"
                        markup = InlineKeyboardMarkup([
                            [InlineKeyboardButton("❌ Hapus Request", callback_data=f'act_clear_channel_{nick}')],
                            [InlineKeyboardButton("🔙 Kembali", callback_data=f'cat_review_channel')]
                        ])
                    query.edit_message_text(pesan, reply_markup=markup, parse_mode='HTML')
                else:
                    query.edit_message_text("❌ Request sudah tidak aktif.", reply_markup=keyboard.back_button(f'cat_review_{cat}'), parse_mode='HTML')

    except Exception as e:
        query.edit_message_text(f"⚠️ <b>BUG TERDETEKSI:</b>\n<code>{str(e)}</code>", parse_mode='HTML')
        logger.error(f"Telegram Bug: {e}")

def mulai_pendengar(tt_server=None):
    try:
        updater = Updater(token, use_context=True)
        dp = updater.dispatcher
        dp.bot_data['tt_server'] = tt_server         

        dp.add_handler(CommandHandler("creview", telegram_creview))
        dp.add_handler(CommandHandler("ureview", telegram_ureview))
        dp.add_handler(CommandHandler("remove", telegram_remove))
        dp.add_handler(CommandHandler("clear", telegram_clear))
        dp.add_handler(CommandHandler("check", telegram_check))
        dp.add_handler(CommandHandler("see", telegram_see))
        dp.add_handler(CommandHandler("bantuan", telegram_bantuan))
        
        dp.add_handler(CommandHandler("panel", telegram_panel))
        dp.add_handler(CommandHandler("start", telegram_panel))
        dp.add_handler(CallbackQueryHandler(button_callback))
        
        updater.start_polling()
    except Exception as e:
        logger.error(f"Fatal: {e}")