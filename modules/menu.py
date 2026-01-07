import os

def menu_utama():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
            print("================RUANG TEDUH==============") # Judul aplikasi

            print("Halo! Apa yang ingin kamu lakukan hari ini?\n")

            print("[1] 📝 Mulai Tes Kesehatan Mental")
            print("[2] 📊 Lihat Riwayat Hasil Saya")
            print("[3] 📚 Baca Artikel Kesehatan Mental")
            print("[4] ✅ To-Do List & Self Care")
            print("[5] ℹ️ Tentang Aplikasi (Disclaimer)")
            print("[6] 🚪 Keluar Aplikasi")

            print("\n" + "-"*40)

            pilihan = ['1','2','3','4','5','6']
            user_input = input("Pilih menu (1-6): ")

            if user_input in ['1', '2', '3', '4', '5', '6']:
                return user_input
            else:
                input("Pilihan tidak valid, bro. Tekan Enter untuk coba lagi...")