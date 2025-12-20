import pandas as pd
import os
from datetime import datetime

# =========================
# PATH AMAN
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "questionnaires")


# =========================
# LOAD DATA CSV
# =========================
def load_questionnaire(test_id):
    tests = pd.read_csv(os.path.join(DATA_DIR, "tests.csv"))
    pertanyaan = pd.read_csv(os.path.join(DATA_DIR, "pertanyaan.csv"))
    skala_df = pd.read_csv(os.path.join(DATA_DIR, "skala.csv"))
    skoring = pd.read_csv(os.path.join(DATA_DIR, "skoring.csv"))

    # INFO TES
    info = tests[tests["test_id"] == test_id]
    if info.empty:
        raise ValueError(f"Tes '{test_id}' tidak ditemukan di tests.csv")
    info = info.iloc[0]

    # FILTER DATA
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
# JALANKAN KUISIONER
# =========================
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

    # 🔥 AUTO ENUM OFFSET
    tampil_offset = 1 if min_nilai == 0 else 0

    for i, p in enumerate(data["pertanyaan"], 1):
        print(f"\n{i}. {p['teks']}")

        # Mapping tampilan → nilai asli
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

                # reverse aman semua skala
                skor = (max_nilai - nilai) if is_reverse else nilai

                total_skor += skor
                break
            else:
                print("❌ Input tidak valid")

    hasil = analisis_skor(total_skor, data["skoring"])

    return {
        "test_id": test_id,
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_skor": total_skor,
        "analisis": hasil
    }


# =========================
# ANALISIS SKOR
# =========================
def analisis_skor(total_skor, skoring):
    for r in skoring:
        if r["min"] <= total_skor <= r["max"]:
            return r

    return {
        "level": "Tidak diketahui",
        "kategori": "-",
        "deskripsi": "Hasil tidak dapat ditentukan"
    }


# =========================
# TAMPILKAN HASIL
# =========================
def tampilkan_hasil(hasil):
    print("\n" + "=" * 70)
    print("HASIL TES".center(70))
    print("=" * 70)
    print("Tanggal    :", hasil["tanggal"])
    print("Total Skor :", hasil["total_skor"])
    print("Level      :", hasil["analisis"]["level"])
    print("Deskripsi  :", hasil["analisis"]["deskripsi"])
    print("=" * 70)