import sys
import os
import pandas as pd
from modules.menu import menu_utama
from modules.about import tampilkan_tentang_kami
from modules.questionnaire_menu import tampilkan_menu_kuisioner
from modules.questionnaire_engine_csv import jalankan_kuisioner, tampilkan_hasil, riwayat_hasil
from modules.login_register import menu_auth    
from modules.psikolog import list_psikolog,menu_psikolog

def tampilkan_todo_list(username):
    """
    Menampilkan to-do list user dari CSV
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, "data", "to_do", username, "to_do_list.csv")
    
    if not os.path.exists(csv_path):
        print("\n📭 Anda belum memiliki to-do list.")
        print("💡 Selesaikan tes terlebih dahulu untuk mendapatkan rekomendasi aktivitas.")
        return
    
    # Baca CSV
    df = pd.read_csv(csv_path)
    
    if df.empty:
        print("\n📭 To-do list Anda kosong.")
        return
    
    print("\n" + "=" * 70)
    print("📋 TO-DO LIST SAYA".center(70))
    print("=" * 70)
    
    # Tampilkan berdasarkan test_id
    for test_id in df['test_id'].unique():
        test_data = df[df['test_id'] == test_id]
        pending = test_data[test_data['status'] == 'pending']
        
        if not pending.empty:
            print(f"\n🔹 {test_id.upper()}")
            print("-" * 70)
            
            for idx, row in pending.iterrows():
                checkbox = "☐" if row['status'] == 'pending' else "☑"
                print(f"{checkbox} [{row['prioritas']}] {row['aktivitas']}")
                print(f"   Ditambahkan: {row['tanggal']}")
    
    print("=" * 70)

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