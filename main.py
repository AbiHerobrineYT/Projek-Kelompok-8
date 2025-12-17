from modules.menu import menu_utama
from modules.about import tampilkan_tentang_kami
from modules.questionnaire_menu import tampilkan_menu_kuisioner, get_nama_kuisioner
from modules.questionnaire_engine import jalankan_kuisioner, tampilkan_hasil, tampilkan_solusi_lengkap

def main():
    while True:
        pilihan = menu_utama()
        
        if pilihan == '1':
            pilihan_kuisioner = tampilkan_menu_kuisioner()
            
            if pilihan_kuisioner == '9':
                continue
            else:
                mapping_tes = {
                    '1': 'keluarga',
                    '2': 'depresi',
                    '3': 'kecemasan',
                    '4': 'stress',
                    '5': 'trauma',
                    '6': 'burnout',
                    '7': 'mood',
                    '8': 'kecanduan'
                }
                
                jenis_tes = mapping_tes.get(pilihan_kuisioner)
                
                if jenis_tes:
                    # Jalankan kuisioner
                    hasil = jalankan_kuisioner(jenis_tes)
                    
                    if hasil:
                        # Tampilkan hasil SKOR saja
                        tampilkan_hasil(hasil)
                        
                        # Tampilkan solusi lengkap
                        tampilkan_solusi_lengkap(
                            hasil['jenis_tes'], 
                            hasil['analisis']['kategori']
                        )
                        
                        # TODO: Simpan hasil ke storage
                        
                input("\n\n👉 Tekan Enter untuk kembali ke menu utama...")
            
        elif pilihan == '2':
            print("\n📊 Menampilkan Riwayat Hasil...")
            input("\nTekan Enter untuk kembali ke menu...")
            
        elif pilihan == '3':
            print("\n✅ To-Do List & Self Care...")
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