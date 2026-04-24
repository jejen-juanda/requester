import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🔍 Status Check", callback_data='nav_check'),
         InlineKeyboardButton("📖 Review Active", callback_data='nav_review')],
        [InlineKeyboardButton("🗑️ Clear Requests", callback_data='nav_clear')],
        [InlineKeyboardButton("⚙️ Panel Admin", callback_data='nav_admin')]
    ]
    return InlineKeyboardMarkup(keyboard)

def category_menu(action):
    keyboard = [
        [InlineKeyboardButton("📁 Channel Requests", callback_data=f'cat_{action}_channel')],
        [InlineKeyboardButton("👤 User Requests", callback_data=f'cat_{action}_user')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='nav_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def requester_list_menu(action, category):
    keyboard = []
    
    # PERBAIKAN: Nama variabel diubah menjadi folder_map_req agar sesuai dengan pemanggilannya
    folder_map_req = {"channel": "channel-requests", "user": "user-account-requests"}
    folder_map_track = {"channel": "channel-tracking", "user": "user-account-tracking"}

    path_req = f"requests/{folder_map_req[category]}"
    path_track = f"tracking/{folder_map_track[category]}"
    
    all_names = set()
    if os.path.exists(path_req):
        for f in os.listdir(path_req):
            if f.endswith(".request"): all_names.add(os.path.splitext(f)[0])
            
    if action == "check" and os.path.exists(path_track):
        for f in os.listdir(path_track):
            if f.endswith(".track"): all_names.add(os.path.splitext(f)[0])

    for name in sorted(list(all_names)):
        cb_data = f"act_{action}_{category}_{name}"
        keyboard.append([InlineKeyboardButton(f"📄 {name}", callback_data=cb_data[:64])])
    
    if not keyboard:
        keyboard.append([InlineKeyboardButton("❌ Kosong", callback_data='ignore')])
        
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data=f'nav_{action}')])
    return InlineKeyboardMarkup(keyboard)

def back_button(target='nav_main'):
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data=target)]])