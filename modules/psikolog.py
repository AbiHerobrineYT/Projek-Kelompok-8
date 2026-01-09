import pandas as pd
import os
import csv
import datetime
import random

lokasi_file = os.path.join('data','psikolog.csv')

def data_psikolog():

    data_psikolog = []

    with open(lokasi_file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data_psikolog.append(row)
        
    return data_psikolog


def save_booking_struk(data_booking):
    folder_user = os.path.join('data',
                               'Booking',
                                data_booking['nama_pasien'])

    os.makedirs(folder_user, exist_ok=True)
    nama_file = f"booking_{data_booking['id_booking']}.txt"
    lokasi_file = os.path.join(folder_user, nama_file)

    with open(lokasi_file, mode='w', encoding='utf-8') as f:
        GARIS = "=" * 50

        f.write(GARIS + "\n")
        f.write("DETAIL BOOKING".center(50) + "\n")
        f.write(GARIS + "\n")

        struk = (
            f"ID BOOKING      : B_{data_booking['id_booking']}\n"
            f"TANGGAL DICETAK : {data_booking['tanggal_booking']}\n"
            f"----------------------------------------\n"
            f"PASIEN          : {data_booking['nama_pasien']}\n" 
            f"----------------------------------------\n"
            f"PSIKOLOG        : {data_booking['nama']}\n"
            f"SPESIALIS       : {data_booking['spesialis']}\n"
            f"----------------------------------------\n"
            f"JADWAL TEMU     : {data_booking['tanggal']}\n"
            f"PUKUL           : {data_booking['jam']} WIB\n"
            f"----------------------------------------\n"
            f"CATATAN KELUHAN :\n"
            f"{data_booking['keluhan']}\n"
            f"----------------------------------------\n"
            f"Detail mengenai teknis pelaksanaan sesi dan\n"
            f"informasi administrasi telah kami kirimkan ke\n"
            f"alamat email terdaftar:\n\n"
            f"{data_booking['email_pasien']}\n\n"
            f"Mohon periksa kotak masuk (Inbox) atau folder\n"
            f"Spam Anda untuk mendapatkan panduan lebih\n"
            f"lanjut dari Psikolog terkait.\n"
        )
        f.write(struk)
        return nama_file

def list_psikolog(username_aktif, email_user):
    list_psikolog = data_psikolog()

    if not list_psikolog:
        return
    
    print("\n================== DAFTAR REKOMENDASI PSIKOLOG ==================")
    print(f"{'No':<4} {'Nama':<35} {'Spesialis':<25}")
    print("=" * 65)
    
    for i, p in enumerate(list_psikolog, 1):
        nama = p['nama']
        spesialis = p['spesialis']
        
        print(f"{i:<4} {nama:<35} {spesialis:<25}")
    
    print("=" * 65)
        
    while True:
        pilihan = input(f"Pilih nomor psikolog (1-{len(list_psikolog)}) atau '0 untuk kembali: ")
        #mengatasi error saat user klik enter doang
        if pilihan == '':
            return
        
        pilihan = int(pilihan)
        if pilihan == 0:
            return
        elif pilihan in [1,2,3,4]:
            pilihan_psikolog = list_psikolog[pilihan - 1]
            break
        else:
            print(f"Masukkan angka yang valid 1-{len(list_psikolog)}")
    
    print(f"\nKamu memilih : {pilihan_psikolog['nama']}")
    booking_psikolog(username_aktif, email_user, pilihan_psikolog)

def booking_psikolog(username_aktif, email_user, pilihan_psikolog):
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
            print(f"Format salah. Gunakan HH.MM (Contoh: 09.30)")

    keluhan = input("Keluhan Anda : ")

    folder_user = os.path.join('data', username_aktif)

    os.makedirs(folder_user, exist_ok=True)
    
    nomor_urut = len(os.listdir(folder_user)) + 1
    
    id_booking = str(nomor_urut)

    data_booking = {
        'id_booking' : id_booking,
        'nama' : pilihan_psikolog['nama'],
        'spesialis' : pilihan_psikolog['spesialis'],
        'nama_pasien' : username_aktif,
        'email_pasien' : email_user,
        'tanggal' : tanggal,
        'jam' : jam_booking,
        'keluhan' : keluhan,
        'tanggal_booking' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    nama_file = save_booking_struk(data_booking)

    print("\n" + "="*50)
    print(f"✅ BOOKING BERHASIL! STRUK TELAH DICETAK.")
    print(f"📄 Lokasi File: data/Booking/{username_aktif}/{nama_file}")
    print(f"🆔 ID       : {id_booking}")
    print("="*50)
    

def lihat_riwayat_booking(username_aktif):
    folder_user = os.path.join('data', 'Booking', username_aktif)

    if not os.path.exists(folder_user):
        print(f"\n[!] Belum ada riwayat booking untuk user: {username_aktif}")
        return
    
    print(f"\n===== DAFTAR RIWAYAT BOOKING ({username_aktif}) =====")
    files = [f for f in os.listdir(folder_user) if f.endswith('.txt')]
    
    for i, nama_file in enumerate(files, 1):
        print(f"{i}. {nama_file}")
    
    while True:
         opsi = input("Pilih nomor (atau Enter untuk kembali): ")   
         print(" ")
         if not opsi:
             return 
        
         if opsi.isdigit() and 1 <= int(opsi) <= len(files):
             nama_file = files[int(opsi) - 1]
             path_lengkap = os.path.join(folder_user, nama_file) 

             with open(path_lengkap, 'r', encoding='utf-8') as f:
                 print(f.read())
             print("="*40)

             input("\nTekan Enter lanjut...")
         else:
             print("❌ Masukkan nomor yang valid!")

def menu_psikolog(username_aktif, email_user):
    while True:
        print(f"[1] List Psikolog")
        print(f"[2] Lihat Riwayat Booking")
        print(f"[3] Kembali")
        user_input = input("Pilih menu (1-3) : ")
        if user_input == '1':
            list_psikolog(username_aktif, email_user)
        elif user_input == '2':
            lihat_riwayat_booking(username_aktif)
        elif user_input == '3':
            return
        else:
            print(f"Masukkan angka yang valid (1-3)")