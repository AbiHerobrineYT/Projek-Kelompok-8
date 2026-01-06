def menu_utama():
    while True:
            print("================RUANG TEDUH==============") # Judul aplikasi

            print("Halo! Apa yang ingin kamu lakukan hari ini?\n")

            print("[1] 📝 Mulai Tes Kesehatan Mental")
            print("[2] 📊 Lihat Riwayat Hasil Saya")
            print("[3] ✅ To-Do List & Self Care")
            print("[4] 📅 Booking Psikolog") 
            print("[5] 📰 Artikel & Tips Mental Health")  
            print("[6] ℹ️ Tentang Aplikasi (Disclaimer)")
            print("[7] 🚪 Keluar Aplikasi")


            print("\n" + "-"*40)

            pilihan = ['1','2','3','4','5']
            user_input = input("Pilih menu (1-5): ")

            if user_input in ['1', '2', '3', '4', '5']:
                return user_input
            else:
                input("Pilihan tidak valid, bro. Tekan Enter untuk coba lagi...")