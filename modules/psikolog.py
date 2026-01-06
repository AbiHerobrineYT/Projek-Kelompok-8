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

file_path_booking = os.path.join('data', 'riwayat-booking.csv')
header_booking = ['id_booking','nama','spesialis','rating','tanggal','jam','keluhan','tanggal_booking']

def save_booking_psikolog(data_booking):

    file_exists = os.path.isfile(file_path_booking)
    try:
        with open(file_path_booking, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=header_booking)

            if not file_exists:
                writer.writeheader()

            writer.writerow(data_booking)
            return True

    except Exception as e:
        print("Data booking gagal disimpan")
        return False

def list_psikolog():
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
        'tanggal' : tanggal,
        'jam' : jam_booking,
        'keluhan' : keluhan,
        'tanggal_booking' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    if save_booking_psikolog(data_booking):
        print("\n" + "="*40)
        print(f"✅ BOOKING BERHASIL DISIMPAN!")
        print(f"ID: {id_booking} | Tanggal: {tanggal}")
        print("="*40)
    else:
        print("\n❌ Terjadi kesalahan sistem saat menyimpan.")