from modules.menu import menu_utama
from modules.about import tampilkan_tentang_kami
from modules.questionnaire_menu import tampilkan_menu_kuisioner, get_nama_kuisioner


def main():
    while True:
        pilihan = menu_utama()
        
        if pilihan == '1':
            pilihan_kuisioner = tampilkan_menu_kuisioner()
            
            if pilihan_kuisioner == '9':
                continue
            else:
                nama_tes = get_nama_kuisioner(pilihan_kuisioner)
                print(f"\n🧠 Memulai Tes: {nama_tes}")
                print("="*60)
                
                # TODO: Panggil fungsi untuk menjalankan kuisioner sesuai pilihan
                # Nanti akan dipanggil di sini, misalnya:
                # if pilihan_kuisioner == '1':
                #     hasil = tes_keluarga_hubungan()
                # elif pilihan_kuisioner == '2':
                #     hasil = tes_depresi()
                # dst...
                
                print(f"\n[DEBUG] Tes {nama_tes} akan dimulai...")
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