import os
import csv
from modules.menu import menu_utama
def menu_artikel(username_aktif):
    print("================ARTIKEL KESEHATAN MENTAL==============") # Judul aplikasi
    print(f"Halo {username_aktif}! Apa yang ingin baca hari ini?\n")
    print("[1] Keluarga")
    print("[2] Depresi")
    print("[3] Kecemasan")
    print("[4] Stres") 
    print("[5] Trauma")  
    print("[6] Burnout Kerja")
    print("[7] Kembali")
    print("\n" + "-"*40)

    while True:
        pilihan = input("\nMasukkan pilihan (1-7): ").strip()

        if pilihan in ['1','2','3','4','5','6']:
            list_artikel(pilihan,username_aktif)

        elif pilihan == '7':
            return 

        else:
            print("\n⚠️  Pilihan tidak valid.")


def list_artikel(jenis_artikel,username_aktif):
    kategori_artikel = {
        '1' : 'Hubungan',
        '2' : 'Depresi',
        '3' : 'Kecemasan'
    }
    
    if jenis_artikel in kategori_artikel:
        jenis_artikel = kategori_artikel[jenis_artikel]

    lokasi_file = os.path.join('data', 'artikel', jenis_artikel, f"artikel_{jenis_artikel}.csv")

    data_artikel = []
    with open(lokasi_file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for item in csv_reader:
            data_artikel.append(item)
    
    print("\n======== LIST ARTIKEL ========")
    print(f"{'no':<4} {'kategori':<10} {'judul':<50} {'tanggal':<10}")
    print(f"="*90)

    for i,p in enumerate(data_artikel,1):
        kategori = p['kategori']
        judul = p['judul']
        tanggal = p['tanggal']
        print(f"{i:<4} {kategori:<10} {judul:<50} {tanggal:<10}")

    print("=" * 90)
    

    while True:
        input_user = int(input(f"Pilih artikel yang ingin dibaca (1-{len(data_artikel)})"))

        id_artikel = data_artikel[input_user-1]['id_artikel']
        lokasi_file_txt = os.path.join('data', 'artikel', jenis_artikel, f"{id_artikel}.txt")
        
        if 1 <= input_user <= len(data_artikel):
            with open(lokasi_file_txt, mode='r', encoding='utf-8') as f:
                print(f.read())
                print("\n")
                print("[1] Kembali ke menu artikel")
                print("[2] Kembali ke menu awal")

                while True:
                    input_user = int(input("Pilih opsi : "))
                    if input_user == 1:
                        menu_artikel(username_aktif)
                    elif input_user == 2:
                        menu_utama(username_aktif)
                    else:
                        print("Masukkan Opsi yang valid\n")
        else:
            print()

menu_artikel('Him')