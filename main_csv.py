import sys
import os
from modules.menu import menu_utama
from modules.about import tampilkan_tentang_kami
from modules.questionnaire_menu import tampilkan_menu_kuisioner
from modules.questionnaire_engine_csv import jalankan_kuisioner, tampilkan_hasil, riwayat_hasil
from modules.login_register import menu_auth    
from modules.psikolog import list_psikolog,menu_psikolog
from modules.to_do import tampilkan_todo_list


def main(username_aktif):
    while True:
        pilihan = menu_utama(username_aktif)

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
                '6': 'burnout'
            }

            jenis_tes = mapping_tes.get(pilihan_kuisioner)

            if not jenis_tes:
                print("\nPilihan tidak valid.")
                continue

            hasil = jalankan_kuisioner(jenis_tes, username_aktif)

            if hasil:
                tampilkan_hasil(hasil,username_aktif)
                input("\nTekan Enter untuk kembali ke menu...")

        elif pilihan == '2':
            isi = riwayat_hasil(username_aktif)

            if isi:
                print(f'\n{isi}')

            input("\nTekan Enter untuk kembali ke menu...")

        elif pilihan == '3':
            tampilkan_todo_list(username_aktif)
            input("\nTekan Enter untuk kembali ke menu...")

        elif pilihan == '4':
            menu_psikolog(username_aktif)

        elif pilihan == '5':
            print("[5] 📰 Artikel & Tips Mental Health COMING SOON") 
            input("\nTekan Enter untuk kembali ke menu...")

        elif pilihan == '6':
            tampilkan_tentang_kami()
            input("\nTekan Enter untuk kembali ke menu...")

        elif pilihan == '7':
            print("\nTerima kasih telah menggunakan Ruang Teduh.")
            print("Jaga kesehatan mental Anda.")
            break

        else:
            print("\nPilihan tidak dikenal.")


if __name__ == "__main__":
    user_data = menu_auth()

    if user_data: 
        username_sekarang = user_data['username']

        main(username_sekarang)