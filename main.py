from modules.menu import menu_utama
from modules.about import tampilkan_tentang_kami


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
            tampilkan_tentang_kami()
            input("\nTekan Enter untuk kembali ke menu...")
            
        elif pilihan == '5':
            print("\n👋 Terima kasih telah menggunakan Ruang Teduh!")
            print("Jaga kesehatan mentalmu ya! 💚")
            break

if __name__ == "__main__":
    main()