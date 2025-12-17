def tampilkan_menu_kuisioner():
    """
    Menampilkan menu pilihan jenis kuisioner kesehatan mental
    Returns: string pilihan user ('1'-'9')
    """
    while True:
        print("\n" + "="*60)
        print("🧠 PILIH JENIS TES KESEHATAN MENTAL 🧠".center(60))
        print("="*60)
        
        print("\nSilakan pilih area yang ingin kamu evaluasi:\n")
        
        print("[1] 👨‍👩‍👧‍👦 Keluarga & Hubungan")
        print("    Evaluasi kualitas hubungan dengan keluarga dan orang terdekat")
        
        print("\n[2] 😔 Depresi")
        print("    Deteksi gejala depresi dan tingkat keparahannya")
        
        print("\n[3] 😰 Kecemasan")
        print("    Ukur tingkat kecemasan dan gangguan anxiety")
        
        print("\n[4] 😫 Stres")
        print("    Evaluasi tingkat stres yang kamu alami")
        
        print("\n[5] 💔 Trauma")
        print("    Identifikasi dampak trauma dan PTSD")
        
        print("\n[6] 🔥 Burnout")
        print("    Ukur tingkat kelelahan fisik, mental, dan emosional")
        
        print("\n[7] 🎭 Gangguan Mood")
        print("    Deteksi perubahan mood dan bipolar tendencies")
        
        print("\n[8] 🚬 Kecanduan")
        print("    Evaluasi potensi kecanduan (substansi, perilaku, dll)")
        
        print("\n[9] 🔙 Kembali ke Menu Utama")
        
        print("\n" + "-"*60)
        
        user_input = input("Pilih tes (1-9): ").strip()
        
        if user_input in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return user_input
        else:
            print("\n❌ Pilihan tidak valid!")
            input("Tekan Enter untuk coba lagi...")


def get_nama_kuisioner(pilihan):
    """
    Mendapatkan nama lengkap kuisioner berdasarkan pilihan
    Args: pilihan (string) - pilihan user ('1'-'8')
    Returns: string nama kuisioner
    """
    nama_kuisioner = {
        '1': 'Keluarga & Hubungan',
        '2': 'Depresi',
        '3': 'Kecemasan',
        '4': 'Stres',
        '5': 'Trauma',
        '6': 'Burnout',
        '7': 'Gangguan Mood',
        '8': 'Kecanduan'
    }
    return nama_kuisioner.get(pilihan, 'Unknown')