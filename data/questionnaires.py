def isianKuesioner():
    pertanyaan = [
        "1. Kesulitan berkonsentrasi?",
        "2. Merasa cemas tanpa alasan?",
        "3. Merasa sedih atau murung?",
        "4. Merasa lelah tanpa aktivitas berat?",
        "5. Kesulitan tidur/kualitas tidur buruk?",
        "6. Tidak percaya diri/meragukan kemampuan?",
        "7. Gugup dalam situasi sosial?",
        "8. Mudah marah atau tersinggung?",
        "9. Kehilangan minat pada aktivitas yang disukai?",
        "10. Sulit mengontrol pikiran negatif?",
        "11. Overthinking berlebihan?",
        "12. Tidak termotivasi menjalani aktivitas?",
        "13. Merasa kesepian meski bersama orang lain?",
        "14. Merasa tekanan hidup terlalu berat?",
        "15. Kesulitan mengambil keputusan?",
        "16. Perubahan selera makan?",
        "17. Merasa panik/jantung berdegup tanpa sebab?",
        "18. Sulit mengontrol emosi?",
        "19. Merasa tidak berharga/menyalahkan diri?",
        "20. Hidup terasa tidak seimbang/terbebani?"
    ]

    print("Jawaban menggunakan skala 1–5:")
    print("1 = Tidak Pernah, 5 = Sangat Sering\n")

    total_skor = 0
    jawaban = []  # untuk simpan skor

    for p in pertanyaan:
        while True:
            skor = int(input(p + " (1-5): "))
            if 1 <= skor <= 5:
                jawaban.append(skor)
                total_skor += skor
                break
            else:
                print("Masukkan angka 1 sampai 5!")

    print("\nTotal Skor Anda:", total_skor)

    # opsional: interpretasi sederhana
    if total_skor <= 40:
        print("Kondisi mental relatif stabil.")
    elif total_skor <= 70:
        print("Ada tanda stres ringan atau sedang.")
    else:
        print("Perlu perhatian lebih, mungkin stres berat.")

    return total_skor, jawaban


# Panggil fungsi
isianKuesioner()
