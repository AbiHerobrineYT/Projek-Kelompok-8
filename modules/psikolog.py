import pandas as pd
import os
import csv
import datetime
import random


def data_psikolog():
    lokasi_file = os.path.join('data','psikolog.csv')

    data_psikolog = []

    try:
        with open(lokasi_file, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                data_psikolog.append(row)
            
        return data_psikolog
    
    except FileNotFoundError:
        print("Error: File data/psikolog.csv tidak ditemukan!")
        return []



def save_booking_struk(data_booking):
    folder_user = os.path.join('data', data_booking['nama_pasien'])

    os.makedirs(folder_user, exist_ok=True)
    nama_file = f"booking_{data_booking['id_booking']}.txt"
    lokasi_file = os.path.join(folder_user, nama_file)

    with open(lokasi_file, mode='w', encoding='utf-8') as f:
        GARIS = "=" * 60

        f.write(GARIS + "\n")
        f.write("DETAIL BOOKING".center(60))
        f.write(GARIS + "\n")

        struk = (
            f"ID BOOKING      : {data_booking['id_booking']}\n"
            f"TANGGAL DICETAK : {data_booking['tanggal_booking']}\n"
            f"----------------------------------------\n"
            f"PASIEN          : {data_booking['nama_pasien']}\n" 
            f"----------------------------------------\n"
            f"PSIKOLOG        : {data_booking['nama']}\n"
            f"SPESIALIS       : {data_booking['spesialis']}\n"
            f"RATING          : {data_booking['rating']}\n"
            f"----------------------------------------\n"
            f"JADWAL TEMU     : {data_booking['tanggal']}\n"
            f"PUKUL           : {data_booking['jam']} WIB\n"
            f"----------------------------------------\n"
            f"CATATAN KELUHAN :\n"
            f"{data_booking['keluhan']}\n"
        )
        f.write(struk)
        return True, nama_file

def list_psikolog(username_aktif):
    list_psikolog = data_psikolog()

    if not list_psikolog:
        return
    
    print("\n===== DAFTAR REKOMENDASI PSIKOLOG =====")
    print(f"{'No':<4} {'Nama':<25} {'Spesialis':<25} {'Rating':<8} {'Jadwal Tersedia'}")
    print("-" * 90)
    
    for i, p in enumerate(list_psikolog, 1):
        nama = p['nama']
        spesialis = p['spesialis']
        rating = p['rating'] + " ⭐"
        jadwal = p['jadwal_tersedia']
        
        print(f"{i:<4} {nama:<25} {spesialis:<25} {rating:<8} {jadwal}")
    
    print("-" * 90)

    #MILIH DULU MAU BOOKING ATAU KEMBALI KE MENU
    while True: 
        print("\n[1] Lanjut Pilih Psikolog")
        print("[2] Kembali ke Menu Utama")
    
        opsi = input("Tentukan pilihanmu (1/2): ")
        if opsi == '1':
            break 
        elif opsi == '2':
            return
        else:
            print("Pilihan salah! Harap masukkan angka 1 atau 2.")
        
    while True:
        pilihan = int(input(f"Pilih nomor psikolog(1-{len(list_psikolog)}) : "))
        if 1<= pilihan <= len(list_psikolog):
            pilihan_psikolog = list_psikolog[pilihan-1]
            break
        else:
            print(f"Masukkan angka yang valid 1-{len(list_psikolog)}")
    
    print(f"\nKamu memilih : {pilihan_psikolog['nama']}")

    #MASUKIN TANGGAL BOOKING 
    while True:
        tanggal = input(f"Masukkan Tanggal (YYYY-MM-DD) : ")
        try:
            tanggal_obj = datetime.datetime.strptime(tanggal, "%Y-%m-%d").date()
            if tanggal_obj < datetime.date.today():
                print("Maaf tanggal sudah terlewat")
                continue
            break
        except ValueError:
            print("Masukkan tanggal yang valid!")
    
    #MASUKAN JAM BOOKING
    while True:
        jam_booking = input(f"Masukkan jam booking (08.00 - 17.00) : ")
        try:
            jam_input = datetime.datetime.strptime(jam_booking, "%H.%M").time()
            if datetime.time(8,0) <= jam_input <= datetime.time(17,0):
                break
            else:
                print("Maaf, jam operasional hanya 08.00 - 17.00")
        except ValueError:
            print(f"Format salah. Gunakan HH:MM (Contoh: 09:30)")

    keluhan = input("Keluhan Anda : ")

    id_booking = f"B-{random.randint(1000, 9999)}"

    data_booking = {
        'id_booking' : id_booking,
        'nama' : pilihan_psikolog['nama'],
        'spesialis' : pilihan_psikolog['spesialis'],
        'rating' : pilihan_psikolog['rating'],
        'nama_pasien' : username_aktif,
        'tanggal' : tanggal,
        'jam' : jam_booking,
        'keluhan' : keluhan,
        'tanggal_booking' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    status, nama_file_dibuat = save_booking_struk(data_booking)

    if status : 
        print("\n" + "="*50)
        print(f"✅ BOOKING BERHASIL! STRUK TELAH DICETAK.")
        print(f"📄 Nama File: data/psikolog/{nama_file_dibuat}")
        print(f"🆔 ID       : {id_booking}")
        print("="*50)
    else:
        print("\n❌ Terjadi kesalahan sistem saat membuat file.")

def lihat_riwayat_booking(username_aktif):

    folder_user = os.path.join('data', username_aktif)

    if not os.path.exists(folder_user):
        print(f"\n[!] Belum ada riwayat booking untuk user: {username_aktif}")
        return
    
    print(f"\n===== DAFTAR RIWAYAT BOOKING ({username_aktif}) =====")
    files = [f for f in os.listdir(folder_user) if f.endswith('.txt')]
    
    for i, nama_file in enumerate(files, 1):
        print(f"{i}. {nama_file}")
    
    print("-" * 40)
    pilihan = input("Pilih nomor file untuk lihat detail (atau Enter untuk kembali): ")
    
    if pilihan.isdigit():
        idx = int(pilihan) - 1
        if 0 <= idx < len(files):
            file_path = os.path.join(folder_user, files[idx])
            print("\n" + "*" * 50)
            with open(file_path, 'r', encoding='utf-8') as f:
                print(f.read())
            print("*" * 50)
            input("Tekan Enter untuk lanjut...")

    

def menu_psikolog(username_aktif):
    while True:
        print(f"[1] List Psikolog")
        print(f"[2] Lihat Riwayat Booking")
        print(f"[3] Kembali")
        user_input = input("Pilih menu (1-3) : ")
        if user_input == '1':
            list_psikolog(username_aktif)
        elif user_input == '2':
            lihat_riwayat_booking(username_aktif)
        elif user_input == '3':
            return
        else:
            print(f"Masukkan angka yang valid (1-3)")