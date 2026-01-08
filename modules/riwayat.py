import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
