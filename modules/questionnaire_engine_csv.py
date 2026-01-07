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
    skala_df = pd.read_csv(os.path.join(DATA_DIR, "skala.csv"))
    skoring = pd.read_csv(os.path.join(DATA_DIR, "skoring.csv"))

    # Info Tes
    info = tests[tests["test_id"] == test_id]
    if info.empty:
        raise ValueError(f"Tes '{test_id}' tidak ditemukan di tests.csv")
    info = info.iloc[0]

    # Filtering
    pertanyaan = pertanyaan[pertanyaan["test_id"] == test_id]
    skoring = skoring[skoring["test_id"] == test_id]
    skala_df = skala_df[skala_df["test_id"] == test_id]

    if skala_df.empty:
        raise ValueError(f"Skala untuk tes '{test_id}' tidak ditemukan di skala.csv")

    skala_dict = dict(zip(skala_df["value"], skala_df["label"]))

    return {
        "nama": info["nama"],
        "deskripsi": info["deskripsi"],
        "instruksi": info["instruksi"],
        "pertanyaan": pertanyaan.to_dict("records"),
        "skala": skala_dict,
        "skoring": skoring.to_dict("records")
    }


# =========================
# LOAD TO-DO LIST
# =========================
def load_todo_list(test_id, kategori):
    """
    Memuat aktivitas rekomendasi berdasarkan test_id dan kategori
    """
    try:
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
    
    except Exception as e:
        print(f"⚠️ Gagal memuat to-do list: {e}")
        return []


# Kuisoner
def jalankan_kuisioner(test_id):
    data = load_questionnaire(test_id)

    print("\n" + "=" * 70)
    print(data["nama"].center(70))
    print("=" * 70)
    print(data["deskripsi"])
    print("\nInstruksi:", data["instruksi"])

    total_skor = 0

    skala_keys = sorted(data["skala"].keys())
    min_nilai = skala_keys[0]
    max_nilai = skala_keys[-1]

    tampil_offset = 1 if min_nilai == 0 else 0

    for i, p in enumerate(data["pertanyaan"], 1):
        print(f"\n{i}. {p['teks']}")

        pilihan_map = {}

        for idx, nilai in enumerate(skala_keys, start=1):
            tampil = idx if tampil_offset else nilai
            pilihan_map[str(tampil)] = nilai
            print(f"  [{tampil}] {data['skala'][nilai]}")

        while True:
            jawab = input(
                f"Jawaban ({min(pilihan_map)} - {max(pilihan_map)}): "
            ).strip()

            if jawab in pilihan_map:
                nilai = pilihan_map[jawab]

                is_reverse = str(p["reverse"]).lower() == "true"

                # Reverse semua skala
                skor = (max_nilai - nilai) if is_reverse else nilai

                total_skor += skor
                break
            else:
                print("❌ Input tidak valid")

    hasil = analisis_skor(total_skor, data["skoring"])
    
    # Load to-do list berdasarkan kategori hasil
    todo_list = load_todo_list(test_id, hasil["level"])

    jumlah_pertanyaan = len(data["pertanyaan"])
    skor_maks = jumlah_pertanyaan * max_nilai

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
    folder_user = os.path.join(BASE_DIR, "data", "hasil", username_aktif)
    
    if not os.path.exists(folder_user):
        os.makedirs(folder_user)

    filename = f"{hasil['test_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(folder_user, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        GARIS = "=" * 60

        f.write(GARIS + "\n")
        f.write("HASIL TES".center(60))
        f.write(GARIS + "\n")

        f.write(f"User       : {username_aktif}\n")
        f.write(f"Tanggal    : {hasil['tanggal']}\n")
        f.write(f"Test ID    : {hasil['test_id']}\n")
        f.write(f"Total Skor : {hasil['total_skor']} / {hasil['skor_maks']}\n")
        f.write(f"Level      : {hasil['analisis']['level']}\n")
        f.write(f"Kategori   : {hasil['analisis'].get('kategori', '-')}\n")
        f.write("Deskripsi  :\n")
        f.write(f"{hasil['analisis']['deskripsi']}\n")

        # Tambahkan To-Do List
        if hasil.get("todo_list"):
            f.write("\n" + GARIS + "\n")
            f.write("REKOMENDASI AKTIVITAS".center(60) + "\n")
            f.write(GARIS + "\n")
            
            for item in hasil["todo_list"]:
                f.write(f"{item['prioritas']}. {item['aktivitas']}\n")

        f.write(GARIS + "\n")

    return filepath


def tampilkan_hasil(hasil, username_aktif, simpan=True):
    print("\n" + "=" * 60)
    print("HASIL TES".center(60))
    print("=" * 60)
    print(f"Tanggal    : {hasil['tanggal']}")
    print(f"Total Skor : {hasil['total_skor']} / {hasil['skor_maks']}")
    print(f"Level      : {hasil['analisis']['level']}")
    print(f"Kategori   : {hasil['analisis']['kategori']}")
    print("Deskripsi  :")
    print(hasil['analisis']['deskripsi'])
    print("=" * 60)
    
    # Tampilkan To-Do List
    if hasil.get("todo_list"):
        print("\n" + "=" * 60)
        print("📋 REKOMENDASI AKTIVITAS".center(60))
        print("=" * 60)
        
        for item in hasil["todo_list"]:
            print(f"{item['prioritas']}. {item['aktivitas']}")
        
        print("=" * 60)

    if simpan:
        path = simpan_hasil_txt(hasil,username_aktif)
        print(f"\n💾 Hasil disimpan di: {path}")

def riwayat_hasil(username_aktif):
    """
    Menampilkan daftar file hasil dan mengembalikan isi file yang dipilih
    """
    folder_user = os.path.join(BASE_DIR, "data", "hasil", username_aktif)
    if not os.path.exists(folder_user) or not os.listdir(folder_user):
        print(f"\n📭 Belum ada riwayat hasil untuk user: {username_aktif}")
        return None

    files = sorted(
        [f for f in os.listdir(folder_user) if f.endswith(".txt")],
        reverse=True
    )

    if not files:
        print("\n📭 Belum ada riwayat hasil.")
        return None

    print(f"\n📊 RIWAYAT HASIL TES : {username_aktif}")
    print("=" * 50)

    ringkasan_list = []

    for i, file in enumerate(files, 1):
        filepath = os.path.join(folder_user, file)
        data = baca_ringkasan_hasil(filepath)

        ringkasan_list.append(filepath)

        print(f"\n[{i}] {data.get('test_id', '-')}"
              f" | {data.get('tanggal', '-')[:16]}")

        print(f"   Skor  : {data.get('total_skor', '-')}")
        print(f"   Level : {data.get('level', '-')}")

    print("\n[0] Kembali")
    print("=" * 60)

    while True:
        pilih = input("Pilih nomor hasil: ").strip()

        if pilih == "0":
            return None

        if pilih.isdigit() and 1 <= int(pilih) <= len(ringkasan_list):
            with open(ringkasan_list[int(pilih) - 1], "r", encoding="utf-8") as f:
                return f.read()

        print("❌ Pilihan tidak valid")

def baca_ringkasan_hasil(filepath):
    ringkasan = {}

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if ":" not in line:
                continue

            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()

            if key == "tanggal":
                ringkasan["tanggal"] = value
            elif key == "test id":
                ringkasan["test_id"] = value
            elif key == "total skor":
                ringkasan["total_skor"] = value
            elif key == "level":
                ringkasan["level"] = value

    return ringkasan

