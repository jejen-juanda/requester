import os
import logging
from classes import handler
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

            elif action == 'approve':
                server_tt = context.bot_data.get('tt_server')                
                if os.path.isfile(path_req):
                    with open(path_req, "rb") as f:
                        info = enc.decrypt(f.read()).decode().split(",")
                    
                    if cat == 'user':
                        server_tt.new_account(username=info[0].strip(), password=info[1].strip(), note=f"By {admin_display_name}")
                        pesan_sukses = f"✅ Akun <b>{nick}</b> BERHASIL dibuat."
                        
                    elif cat == 'channel':
                        c_name = info[0].strip()
                        c_pass = info[1].strip()
                        c_op_pass = info[2].strip()
                        c_topic = info[3].strip()

                        kata_abaikan = ["tidak", "tanpa kata sandi", "none", "-", ""]
                        pwd = "" if c_pass.lower() in kata_abaikan else c_pass
                        op_pwd = "" if c_op_pass.lower() in kata_abaikan else c_op_pass
                        
                        # Radar pencari ID dinamis (Versi Perbaikan)
                        target_parent_id = 1 # Default ke Root
                        target_nama_induk = handler.request("TARGET_CHANNEL") or "User"
                        
                        if hasattr(server_tt, 'channels'):
                            for cinfo in server_tt.channels:
                                # TeamTalk API sering menggunakan 'name', tapi kita cek keduanya untuk keamanan
                                current_name = cinfo.get("name") or cinfo.get("channel") or ""
                                
                                if current_name.strip().lower() == target_nama_induk.strip().lower():
                                    # Mengambil ID channel (biasanya 'chanid' atau 'id')
                                    target_parent_id = cinfo.get("chanid") or cinfo.get("id") or 1
                                    break
                        from Globals import settings
                        server_tt.make_channel(
                            parentid=target_parent_id, 
                            channel_name=c_name, 
                            password=pwd, 
                            oppassword=op_pwd, 
                            topic=c_topic,
                            diskquota=settings["DISK_QUOTA"]
                        )
                        pesan_sukses = f"✅ Channel <b>{nick}</b> BERHASIL dibuat di bawah path '{target_nama_induk}'."
                        
                    save_tracking(cat, nick, "APPROVED", admin_display_name) 
                    os.remove(path_req)
                    
                    query.edit_message_text(pesan_sukses, reply_markup=keyboard.back_button(f'cat_review_{cat}'), parse_mode='HTML')
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
                        pesan = f"📖 <b>Review Channel:</b> {nick}\n- Nama: {info[0]}\n- Pass: {info[1]}\n- Op Pass: {info[2]}\n- Topic: {info[3]}"
                        markup = InlineKeyboardMarkup([
                            [InlineKeyboardButton("✅ Approve", callback_data=f'act_approve_channel_{nick}')],
                            [InlineKeyboardButton("❌ Reject", callback_data=f'act_clear_channel_{nick}')],
                            [InlineKeyboardButton("🔙 Kembali", callback_data=f'cat_review_channel')]
                        ])
                        # -----------------------------
                    query.edit_message_text(pesan, reply_markup=markup, parse_mode='HTML')
                else:
                    query.edit_message_text("❌ Request sudah tidak aktif.", reply_markup=keyboard.back_button(f'cat_review_{cat}'), parse_mode='HTML')
    except Exception as e:
        query.edit_message_text(f"⚠️ <b>BUG TERDETEKSI:</b>\n<code>{str(e)}</code>", parse_mode='HTML')
        logger.error(f"Telegram Bug: {e}")

def telegram_debug_user(update, context):
    if not is_admin(update.effective_chat.id):
        return
        
    server_tt = context.bot_data.get('tt_server')
    args = context.args
    
    if not args:
        update.message.reply_text("Sertakan nickname/username. Contoh: /debug_user jejen")
        return
        
    target = " ".join(args).lower()
    found = False
    
    print("\n" + "="*50)
    print(f"INVESTIGASI FORENSIK USER: {target}")
    print("="*50)
    
    if hasattr(server_tt, 'users'):
        for uinfo in server_tt.users:
            # Kita cek nickname atau username
            nick = uinfo.get("nickname", "").lower()
            uname = uinfo.get("username", "").lower()
            
            if target in nick or target in uname:
                import json
                # Cetak semua properti yang ada di memori
                print(json.dumps(uinfo, indent=4))
                update.message.reply_text(f"✅ Properti user '{uinfo.get('nickname')}' telah dicetak ke terminal!")
                found = True
                break
    
    if not found:
        print(f"User '{target}' tidak ditemukan di memori bot.")
        update.message.reply_text(f"❌ User '{target}' tidak ditemukan (mungkin sedang offline).")
    
    print("="*50 + "\n")

def telegram_debug_channel(update, context):
    if not is_admin(update.effective_chat.id):
        return
        
    server_tt = context.bot_data.get('tt_server')
    target_name = "publik area" # Nama channel yang ingin kita intip
    found = False
    
    print("\n" + "="*50)
    print("HASIL INVESTIGASI FORENSIK CHANNEL")
    print("="*50)
    
    if hasattr(server_tt, 'channels'):
        for cinfo in server_tt.channels:
            # Kita cari channel yang mengandung nama target
            current_name = cinfo.get("name") or cinfo.get("channel") or ""
            if target_name.lower() in current_name.lower():
                import json
                # Mencetak ke terminal VPS dalam format JSON agar rapi
                print(json.dumps(cinfo, indent=4))
                update.message.reply_text(f"✅ Data channel '{current_name}' sudah dicetak ke terminal VPS!")
                found = True
                break
    
    if not found:
        print(f"Gagal menemukan channel dengan nama: {target_name}")
        update.message.reply_text(f"❌ Channel '{target_name}' tidak ditemukan di memori bot.")
    
    print("="*50 + "\n")

def mulai_pendengar(tt_server=None):
    try:
        updater = Updater(token, use_context=True)
        dp = updater.dispatcher
        dp.bot_data['tt_server'] = tt_server         

        dp.add_handler(CommandHandler("debug_user", telegram_debug_user))
        dp.add_handler(CommandHandler("debug_channel", telegram_debug_channel))
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