import sys
import os
from modules.menu import menu_utama
from modules.about import tampilkan_tentang_kami
from modules.questionnaire_menu import tampilkan_menu_kuisioner
from modules.questionnaire_engine_csv import jalankan_kuisioner, tampilkan_hasil, riwayat_hasil
from modules.login_register import menu_auth
from modules.article_menu import menu_artikel  # Tambah import ini

def main():
    while True:
        pilihan = menu_utama(username_aktif=None)

        if pilihan == '1':
            pilihan_kuisioner = tampilkan_menu_kuisioner()

            if pilihan_kuisioner == '9':
                continue

            mapping_tes = {
                '1': 'keluarga',
                '2': 'depresi',
                '3': 'kecemasan',
                '4': 'stress',
                '5': 'trauma',
                '6': 'burnout_kerja'
            }

            jenis_tes = mapping_tes.get(pilihan_kuisioner)

            if not jenis_tes:
                print("\nPilihan tidak valid.")
                continue

            hasil = jalankan_kuisioner(jenis_tes)

            if hasil:
                tampilkan_hasil(hasil)
                
                # TANYAKAN apakah ingin melihat artikel rekomendasi
                print("\n" + "-"*60)
                lihat_artikel = input("Ingin melihat artikel rekomendasi berdasarkan hasil ini? (y/n): ").strip().lower()
                
                if lihat_artikel == 'y':
                    from modules.article_recommender import tampilkan_artikel_rekomendasi
                    tampilkan_artikel_rekomendasi(jenis_tes=jenis_tes, skor=hasil['skor'])
                
                input("\nTekan Enter untuk kembali ke menu...")

        elif pilihan == '2':
            isi = riwayat_hasil()

            if isi:
                print(f'\n{isi}')

            input("\nTekan Enter untuk kembali ke menu...")

        elif pilihan == '3':  # Menu artikel baru
            while True:
                result = menu_artikel()
                if result == 'back':
                    break

        elif pilihan == '4':
            print("\n📋 To-Do List & Self Care (Coming Soon)")
            input("\nTekan Enter untuk kembali ke menu...")

        elif pilihan == '5':
            tampilkan_tentang_kami()
            input("\nTekan Enter untuk kembali ke menu...")

        elif pilihan == '6':  # Diubah dari '5' ke '6'
            print("\nTerima kasih telah menggunakan Ruang Teduh.")
            print("Jaga kesehatan mental Anda.")
            break

        else:
            print("\nPilihan tidak dikenal.")


if __name__ == "__main__":
    if menu_auth():
        main()