<<<<<<< HEAD
import os

def menu_utama():
    os.system('cls' if os.name == 'nt' else 'clear')
=======
def menu_utama(username_aktif):
>>>>>>> 690ed3e87cb9abc82f3d3a0427cabf706e542d92
    while True:
            print("================RUANG TEDUH==============") # Judul aplikasi

            print(f"Halo {username_aktif}! Apa yang ingin kamu lakukan hari ini?\n")

            print("[1] 📝 Mulai Tes Kesehatan Mental")
            print("[2] 📊 Lihat Riwayat Hasil Saya")
<<<<<<< HEAD
            print("[3] 📚 Baca Artikel Kesehatan Mental")
            print("[4] ✅ To-Do List & Self Care")
            print("[5] ℹ️ Tentang Aplikasi (Disclaimer)")
            print("[6] 🚪 Keluar Aplikasi")
=======
            print("[3] ✅ To-Do List & Self Care")
            print("[4] 📅 Booking Psikolog") 
            print("[5] 📰 Artikel & Tips Mental Health")  
            print("[6] ℹ️ Tentang Aplikasi (Disclaimer)")
            print("[7] 🚪 Keluar Aplikasi")

>>>>>>> 690ed3e87cb9abc82f3d3a0427cabf706e542d92

            print("\n" + "-"*40)

            pilihan = ['1','2','3','4','5','6']
            user_input = input("Pilih menu (1-6): ")

            if user_input in ['1', '2', '3', '4', '5', '6']:
                return user_input
            else:
                input("Pilihan tidak valid. Tekan Enter untuk coba lagi...")