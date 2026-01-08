import os
import csv

def menu_artikel(username_aktif):
    
    while True:
        print("================ARTIKEL KESEHATAN MENTAL==============") 
        print(f"Halo {username_aktif}! Apa yang ingin baca hari ini?\n")
        print("[1] Keluarga")
        print("[2] Depresi")
        print("[3] Kecemasan")
        print("[4] Stres") 
        print("[5] Trauma")  
        print("[6] Burnout")
        print("[7] Mood")
        print("[8] Kecanduan")
        print("[9] Kembali")
        print("\n" + "-"*40)

        pilihan = input("\nMasukkan pilihan (1-9): ").strip()

        if pilihan in ['1','2','3','4','5','6','7','8']:
            list_artikel(pilihan,username_aktif)

        elif pilihan == '9':
            return 

        else:
            print("\n⚠️  Pilihan tidak valid.")


def list_artikel(jenis_artikel,username_aktif):
    kategori_artikel = {
        '1' : 'Hubungan',
        '2' : 'Depresi',
        '3' : 'Kecemasan',
        '4' : 'Stres',
        '5' : 'Trauma',
        '6' : 'Burnout',
        '7' : 'Mood',
        '8' : 'Kecanduan'
    }
    
    if jenis_artikel in kategori_artikel:
        jenis_artikel = kategori_artikel[jenis_artikel]

    lokasi_file = os.path.join('data', 'artikel', jenis_artikel, f"artikel_{jenis_artikel}.csv")

    data_artikel = []
    with open(lokasi_file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for item in csv_reader:
            data_artikel.append(item)
    
    
    while True:
        print("\n======== LIST ARTIKEL ========")
        print(f"{'no':<4} {'kategori':<10} {'judul':<50} {'tanggal':<10}")
        print(f"="*90)

        for i,p in enumerate(data_artikel,1):
            kategori = p['kategori']
            judul = p['judul']
            tanggal = p['tanggal']
            print(f"{i:<4} {kategori:<10} {judul:<50} {tanggal:<10}")

        print("=" * 90)
        print('')

        print("Ketik '0' atau tekan Enter kosong untuk kembali ke Menu Kategori.")
        input_user = input(f"Pilih artikel yang ingin dibaca (1-{len(data_artikel)}) : ").strip()

        if not input_user or input_user == '0':
            return
        
        if not input_user.isdigit():
            print("Masukkan angka yang valid.")
            continue

        input_user = int(input_user)

        if not (1 <= input_user <= len(data_artikel)):
            print(f"Artikel yang anda pilih tidak dalam list artikel, mohon pilih (1-{len(data_artikel)}).")
            continue


        id_artikel = data_artikel[input_user-1]['id_artikel']
        lokasi_file_txt = os.path.join('data', 'artikel', jenis_artikel, f"{id_artikel}.txt")
        
        if 1 <= input_user <= len(data_artikel):
            with open(lokasi_file_txt, mode='r', encoding='utf-8') as f:
                print("\n")
                print(f.read())
                print("\n")
                input("Tekan Enter untuk selesai membaca...")