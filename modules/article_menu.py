from modules.article_recommender import tampilkan_artikel_rekomendasi

def menu_artikel():
    """Menu utama untuk artikel"""
    print("\n" + "="*60)
    print("📚 RUANG BACA - ARTIKEL KESEHATAN MENTAL")
    print("="*60)
    print("\nPilih kategori artikel:")
    print("1. Keluarga & Hubungan")
    print("2. Depresi")
    print("3. Kecemasan")
    print("4. Stress")
    print("5. Trauma")
    print("6. Burnout Kerja")
    print("7. Artikel Terpopuler")
    print("8. Rekomendasi Berdasarkan Riwayat")
    print("9. Kembali ke Menu Utama")
    
    pilihan = input("\nMasukkan pilihan (1-9): ").strip()
    
    mapping_kategori = {
        '1': 'keluarga',
        '2': 'depresi',
        '3': 'kecemasan',
        '4': 'stress',
        '5': 'trauma',
        '6': 'burnout_kerja',
        '7': None,  # Artikel terpopuler
        '8': None   # Rekomendasi berdasarkan riwayat
    }
    
    if pilihan in ['1', '2', '3', '4', '5', '6']:
        kategori = mapping_kategori[pilihan]
        tampilkan_artikel_rekomendasi(jenis_tes=kategori)
        
    elif pilihan == '7':
        tampilkan_artikel_rekomendasi()  # Artikel terpopuler
        
    elif pilihan == '8':
        # Fitur ini bisa dikembangkan untuk membaca riwayat pengguna
        print("\n🔍 Sistem akan menganalisis riwayat tes Anda...")
        # Di sini bisa ditambahkan logika untuk membaca riwayat dari CSV
        print("Fitur rekomendasi personal akan segera tersedia!")
        
    elif pilihan == '9':
        return 'back'
    
    else:
        print("\n⚠️  Pilihan tidak valid.")
    
    input("\nTekan Enter untuk kembali ke menu artikel...")
    return None