def scoring(kuisoner):
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

