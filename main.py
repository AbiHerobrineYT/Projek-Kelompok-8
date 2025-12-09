from modules.menu import menu_utama

def main():
    while True:
        pilihan = menu_utama()
        
        if pilihan == '1':
            print("\n🧠 Memulai Tes Kesehatan Mental...")
            # TODO: panggil fungsi tes kesehatan mental
            # Tambahin kode kesehatan mental disini
            input("\nTekan Enter untuk kembali ke menu...")
            
        elif pilihan == '2':
            print("\n📊 Menampilkan Riwayat Hasil...")
            # TODO: panggil fungsi lihat riwayat
            # Tambahin kode riwayat hasil
            input("\nTekan Enter untuk kembali ke menu...")
            
        elif pilihan == '3':
            print("\n✅ To-Do List & Self Care...")
            # TODO: panggil fungsi to-do list
            # Tambahin kode to do list
            input("\nTekan Enter untuk kembali ke menu...")
            
        elif pilihan == '4':
            print("\n" + "="*40)
            print("ℹ️  TENTANG APLIKASI - DISCLAIMER")
            # Tambahin kode about disini boleh hapus yg bawah
            print("="*40)
            print("\nRuang Teduh adalah aplikasi skrining kesehatan mental.")
            print("Hasil tes ini BUKAN diagnosis medis profesional.")
            print("Jika kamu mengalami masalah serius, segera konsultasi")
            print("dengan psikolog atau psikiater profesional.")
            print("\n⚠️  Aplikasi ini hanya untuk awareness dan screening awal.")
            input("\nTekan Enter untuk kembali ke menu...")
            
        elif pilihan == '5':
            print("\n👋 Terima kasih telah menggunakan Ruang Teduh!")
            print("Jaga kesehatan mentalmu ya! 💚")
            break

if __name__ == "__main__":
    main()