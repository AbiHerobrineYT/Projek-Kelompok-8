import sys
import os
from modules.menu import menu_utama
from modules.about import tampilkan_tentang_kami
from modules.questionnaire_menu import tampilkan_menu_kuisioner
from modules.questionnaire_engine_csv import jalankan_kuisioner, tampilkan_hasil, riwayat_hasil
from modules.login_register import menu_auth


def main():
    while True:
        pilihan = menu_utama()

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
                input("\nTekan Enter untuk kembali ke menu...")

        elif pilihan == '2':
            isi = riwayat_hasil()

            if isi:
                print(f'\n{isi}')

            input("\nTekan Enter untuk kembali ke menu...")

        elif pilihan == '3':
            print("\n📋 To-Do List & Self Care (Coming Soon)")
            input("\nTekan Enter untuk kembali ke menu...")

        elif pilihan == '4':
            tampilkan_tentang_kami()
            input("\nTekan Enter untuk kembali ke menu...")

        elif pilihan == '5':
            print("\nTerima kasih telah menggunakan Ruang Teduh.")
            print("Jaga kesehatan mental Anda.")
            break

        else:
            print("\nPilihan tidak dikenal.")


if __name__ == "__main__":
    if menu_auth():
        main()
