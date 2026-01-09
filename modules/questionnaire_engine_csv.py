import pandas as pd
import os
from datetime import datetime

# Bikin Folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "questionnaires")
HASIL_DIR = os.path.join(BASE_DIR, "data", "hasil")

if not os.path.exists(HASIL_DIR):
    os.makedirs(HASIL_DIR)


# Load Data CSV
def load_questionnaire(test_id):
    tests = pd.read_csv(os.path.join(DATA_DIR, "tests.csv"))
    pertanyaan = pd.read_csv(os.path.join(DATA_DIR, "pertanyaan.csv"))
    skoring = pd.read_csv(os.path.join(DATA_DIR, "skoring.csv"))

    # Info Tes
    info = tests[tests["test_id"] == test_id]
    if info.empty:
        raise ValueError(f"Tes '{test_id}' tidak ditemukan di tests.csv")
    info = info.iloc[0]

    # Filtering
    pertanyaan = pertanyaan[pertanyaan["test_id"] == test_id]
    skoring = skoring[skoring["test_id"] == test_id]


    return {
        "nama": info["nama"],
        "deskripsi": info["deskripsi"],
        "instruksi": info["instruksi"],
        "pertanyaan": pertanyaan.to_dict("records"),
        "skoring": skoring.to_dict("records")
    }


# =========================
# LOAD TO-DO LIST
# =========================
def load_todo_list(test_id, kategori):
    """
    Memuat aktivitas rekomendasi berdasarkan test_id dan kategori
    """
    
    todo_path = os.path.join(DATA_DIR, "to_do_list.csv")
    if not os.path.exists(todo_path):
        return []
    
    todo_df = pd.read_csv(todo_path)
    
    # Filter berdasarkan tes dan kategori
    aktivitas = todo_df[
        (todo_df["tes"] == test_id) & 
        (todo_df["kategori"] == kategori)
    ].sort_values("prioritas")
    
    return aktivitas.to_dict("records")
    


# Kuisoner
def jalankan_kuisioner(test_id, username):
    data = load_questionnaire(test_id)

    print("\n" + "=" * 70)
    print(data["nama"].center(70))
    print("=" * 70)
    print(data["deskripsi"])
    print("\nInstruksi:", data["instruksi"])

    total_skor = 0

    for i, p in enumerate(data["pertanyaan"], 1):
        print(f"\n{i}. {p['teks']}")

        print("[1] Tidak Pernah")
        print("[2] Jarang")
        print("[3] kadang-kadang")
        print("[4] Sering")

        while True:
            user_input = input("Jawaban (1 - 4) : ").strip()

            if user_input == "":
                print("❌ Jawaban tidak boleh kosong!")
                continue

            if not user_input.isdigit():
                print("❌ Masukkan angka 1 - 4!")
                continue

            jawab = int(user_input)

            if 1 <= jawab <= 4:
                total_skor += jawab
                break
            else:
                print("❌ Pilih angka 1 - 4!")

            


    hasil = analisis_skor(total_skor, data["skoring"])
    
    # Load to-do list berdasarkan kategori hasil
    todo_list = load_todo_list(test_id, hasil["level"])

    # Simpan to-do list ke CSV user jika username tersedia
    if username and todo_list:
        simpan_todo_ke_csv(username, test_id, todo_list)

    jumlah_pertanyaan = len(data["pertanyaan"])
    skor_maks = jumlah_pertanyaan * 4

    hasil_analisis = analisis_skor(total_skor, data["skoring"])

    return {
        "test_id": test_id,
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_skor": total_skor,
        "skor_maks": skor_maks,
        "analisis": hasil,
        "todo_list": todo_list
    }


# Analisis skor
def analisis_skor(total_skor, skoring):
    for r in skoring:
        if r["min"] <= total_skor <= r["max"]:
            return r

    return {
        "level": "Tidak diketahui",
        "kategori": "-",
        "deskripsi": "Hasil tidak dapat ditentukan"
    }


# Menampilkan dan Penyimpanan Hasil
def simpan_hasil_txt(hasil, username_aktif):
    """
    Simpan hasil tes ke file TXT
    """
    filename = f"{hasil['test_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    # Path dengan folder username
    user_hasil_dir = os.path.join(HASIL_DIR, username_aktif)
    if not os.path.exists(user_hasil_dir):
        os.makedirs(user_hasil_dir)
    
    filepath = os.path.join(user_hasil_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        GARIS = "=" * 60

        f.write(GARIS + "\n")
        f.write("HASIL TES".center(60) + "\n")
        f.write(GARIS + "\n")

        f.write(f"User       : {username_aktif}\n")
        f.write(f"Tanggal    : {hasil['tanggal']}\n")
        f.write(f"Test ID    : {hasil['test_id']}\n")
        f.write(f"Total Skor : {hasil['total_skor']} / {hasil['skor_maks']}\n")
        f.write(f"Level      : {hasil['analisis']['level']}\n")
        f.write(f"Kategori   : {hasil['analisis']['kategori']}\n")
        f.write("Deskripsi  :\n")
        f.write(hasil["analisis"]["deskripsi"] + "\n")

        # Tambahkan To-Do List
        if hasil.get("todo_list"):
            f.write(GARIS + "\n")
            f.write("REKOMENDASI AKTIVITAS".center(60) + "\n")
            f.write(GARIS + "\n")
            
            for item in hasil["todo_list"]:
                f.write(f"{item['prioritas']}. {item['aktivitas']}\n")
            
            f.write(GARIS + "\n")
            
            # ← TAMBAHAN BARU: Status dan Progress
            f.write(f"Status     : Belum Tuntas\n")
            f.write(f"Progress   : 0%\n")

        f.write(GARIS + "\n")

    tampilkan_hasil(filepath)


def tampilkan_hasil(filepath):
    #Biar lebih kebayang tinggal print txt yang udah disimpen
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        print(csvfile.read())
        print(" ")
        print(f"\n💾 Hasil disimpan di: {filepath}")


def simpan_todo_ke_csv(username, test_id, todo_list):
    """
    Menyimpan to-do list ke file CSV user
    """
    import csv  # ← Tambah import ini
    
    # Path folder user
    user_todo_dir = os.path.join(BASE_DIR, "data", "to_do", username)
    
    # Buat folder jika belum ada
    if not os.path.exists(user_todo_dir):
        os.makedirs(user_todo_dir)
    
    # Path file CSV
    csv_path = os.path.join(user_todo_dir, "to_do_list.csv")
    
    # Siapkan data
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Cek apakah file sudah ada
    file_exists = os.path.exists(csv_path)
    
    # Tulis ke CSV dengan csv.writer (handle koma otomatis)
    with open(csv_path, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)  # ← Pakai csv.writer
        
        # Header jika file baru
        if not file_exists:
            writer.writerow(["tanggal", "test_id", "prioritas", "aktivitas", "status"])
        
        # Tulis setiap aktivitas
        for item in todo_list:
            writer.writerow([
                timestamp,
                test_id,
                item['prioritas'],
                item['aktivitas'],  # ← Otomatis di-quote jika ada koma
                'pending'
            ])