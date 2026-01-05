# --------------------
# FUNGSI UMUM PROSES INPUT & SKOR
# --------------------
def proses_kuesioner(pertanyaan, jenis):
    print("Skala 1–5 | 1 = Tidak Pernah, 5 = Sangat Sering\n")

    total_skor = 0
    jawaban = []

    for q in pertanyaan:
        while True:
            skor = int(input(q + " (1-5): "))
            if 1 <= skor <= 5:
                jawaban.append(skor)
                total_skor += skor
                break
            else:
                print("Masukkan angka 1–5!")
    print(f"\nTotal Skor {jenis.capitalize()}: {total_skor}")

    # Interpretasi khusus setiap jenis kuesioner
    if jenis == "depresi":
        if total_skor <= 15:
            print("Interpretasi: Depresi sangat rendah / normal.")
        elif total_skor <= 30:
            print("Interpretasi: Depresi ringan.")
        elif total_skor <= 40:
            print("Interpretasi: Depresi sedang.")
        else:
            print("Interpretasi: Depresi berat.")

    elif jenis == "stres":
        if total_skor <= 15:
            print("Interpretasi: Stres rendah.")
        elif total_skor <= 30:
            print("Interpretasi: Stres sedang.")
        elif total_skor <= 40:
            print("Interpretasi: Stres tinggi.")
        else:
            print("Interpretasi: Stres sangat tinggi.")

    elif jenis == "burnout":
        if total_skor <= 15:
            print("Interpretasi: Burnout sangat rendah.")
        elif total_skor <= 30:
            print("Interpretasi: Burnout ringan.")
        elif total_skor <= 40:
            print("Interpretasi: Burnout sedang.")
        else:
            print("Interpretasi: Burnout berat.")

    return total_skor, jawaban
