def kuesioner_depresi():
    pertanyaan = [
        "1. Merasa sedih berkepanjangan?",
        "2. Kehilangan minat pada aktivitas yang biasanya disukai?",
        "3. Merasa tidak berharga atau menyalahkan diri sendiri?",
        "4. Mengalami perubahan pola tidur (terlalu banyak atau sedikit)?",
        "5. Perubahan selera makan?",
        "6. Merasa kelelahan hampir setiap hari?",
        "7. Merasa sulit untuk berkonsentrasi?",
        "8. Merasa harapan untuk masa depan menurun?",
        "9. Merasa ingin menarik diri dari orang lain?",
        "10. Merasa hidup tidak bermakna?"
    ]

    print("\n=== KUESIONER DEPRESI ===")
    return proses_kuesioner(pertanyaan, "depresi")


def kuesioner_stres():
    pertanyaan = [
        "1. Merasa tegang atau gelisah?",
        "2. Merasa mudah marah tanpa alasan jelas?",
        "3. Merasa sulit mengontrol kecemasan?",
        "4. Sulit menenangkan diri setelah marah atau cemas?",
        "5. Merasa kewalahan oleh tugas sehari-hari?",
        "6. Merasa sulit tidur karena pikiran berlebih?",
        "7. Merasa detak jantung meningkat saat tegang?",
        "8. Merasa sulit fokus karena tekanan?",
        "9. Merasa takut membuat kesalahan kecil?",
        "10. Merasa tubuh terasa kaku atau pegal karena tegang?"
    ]

    print("\n=== KUESIONER STRES ===")
    return proses_kuesioner(pertanyaan, "stres")


def kuesioner_burnout():
    pertanyaan = [
        "1. Merasa lelah secara fisik maupun mental?",
        "2. Kehilangan motivasi untuk bekerja atau belajar?",
        "3. Merasa tidak berdaya menghadapi tugas?",
        "4. Merasa tidak puas dengan hasil kerja Anda?",
        "5. Merasa sulit memulai aktivitas?",
        "6. Merasa jenuh atau bosan berat?",
        "7. Merasa sinis terhadap pekerjaan/tugas?",
        "8. Merasa sulit memulihkan energi meski beristirahat?",
        "9. Merasa ingin menghindari tugas secara emosional?",
        "10. Merasa produktivitas Anda menurun?"
    ]

    print("\n=== KUESIONER BURNOUT ===")
    return proses_kuesioner(pertanyaan, "burnout")


# --------------------
# FUNGSI MEMILIH TES
# --------------------
def pilih_tes():
    print("\n=== PILIH JENIS TES ===")
    print("1. Depresi")
    print("2. Stres")
    print("3. Burnout")

    pilihan = input("Masukkan pilihan (1/2/3): ")

    if pilihan == "1":
        return kuesioner_depresi()
    elif pilihan == "2":
        return kuesioner_stres()
    elif pilihan == "3":
        return kuesioner_burnout()
    else:
        print("Pilihan tidak valid.")
