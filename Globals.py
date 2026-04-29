settings={
	"HOST": "example.com",
	"TCPPORT": "10333",
	"UDPPORT": "10333",
	"USERNAME": "guest",
	"PASSWORD": "guest",
	"nickname": "TT Request Manager",
	"client": "TeamTalk Request manager",
	"TARGET_CHANNEL": "User",
	"DISK_QUOTA": 136870912,
	"NOTIFICATIONS": "True"
}
bantuan="""bp nama pengguna, kata sandi, nama depan. Mengajukan permintaan untuk akun pengguna yang dapat ditinjau oleh administrator kapan saja.
bc nama channel, kata sandi channel, kata sandi operator channel, topik channel. Mengajukan permintaan untuk proses pembuatan channel yang dapat ditinjau oleh administrator kapan saja."""
admin="""I've noticed that you're an administrator, here are a few useful commands for you.
check, check the amount of requests submitted so far.
see channel-requests, or see user-account-requests. Outputs the names of everyone who have made a request in either the channel-requests or the user-account-requests, respectively.
ureview nickname. Reviews a request file with the specified name in the user-account-requests category, if any.
creview nickname. Reviews a request file with the specified name in the channel-requests category, if any.
remove channel-requests nickname, or remove user-account-requests nickname. Removes a request file with the specified nickname, use remove channel-requests nickname to remove a request with the specified name from the channel-requests category, and remove user-account-requests nickname to remove a request from the user-account-requests category.
clear channel-requests, or clear user-account-requests, or clear all. Clears the specified category of all request files, clear all will clear all the requests in both categories. Please be careful with this command and only use it if you're absolutely sure you have delt with all the requests so as to prevent any data loss.
notifications, toggles the sending of notifications via telegram on/off."""
unrecognized="Perintah tidak dikenali, tulis bantuan untuk informasi lebih lanjut!"
details="Silakan coba lagi, dan isi semua detailnya. Namun, jika Kamu ingin meninggalkan sesuatu yang tidak ditentukan, kata sandi saluran misalnya, cukup ketik tanpa kata sandi, atau tidak."
empty="The specified category is empty of requests."
success="Berhasil! Permintaanmu telah saya catat dan akan ditinjau secepatnya oleh administrator."
syntax="Coba lagi! tolong gunakan tanda koma untuk memisahkan informasi yang dibutuhkan. contoh:. Gaming, tanpa kata sandi, tanpa kata sandi operator, saluran yang didedikasikan untuk semua hal yang berhubungan dengan game. Dalam hal ini, kami menentukan nama saluran, yaitu game, lalu kami menggunakan koma, lalu spasi, untuk beralih ke kata sandi, tanpa kata sandi, koma, spasi, tanpa kata sandi operator, DLL."
exists="Permintaanmu telah dicatat sebelumnya, jika ini adalah kesalahan, tolong hubungi administrator untuk klarifikasi lebih lanjut."
null="The specified name has not been found, please make sure you're spelling it correctly then try again. If otherwise, then there aren't any requests made by the name you have entered."
deleted="The specified request has been removed."
cleared="The command has been executed successfully."
incorrect="Invalid argument, please refer to the help section for more information on how to use this command."
token=""
id=
cnotification=" has just made a channel request."
unotification=" has just made a user-account-request."
notifications=None