import json
import os
from datetime import datetime

def load_questionnaire(jenis_tes):
    """
    Load data kuisioner dari file JSON
    """
    try:
        file_path = f"data/questionnaires/{jenis_tes}.json"
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"\n❌ Error: File kuisioner '{jenis_tes}.json' tidak ditemukan!")
        return None
    except json.JSONDecodeError:
        print(f"\n❌ Error: File kuisioner '{jenis_tes}.json' memiliki format yang salah!")
        return None


def load_solutions():
    """
    Load semua data solusi dari file JSON
    Returns: dict - semua solusi atau None jika error
    """
    try:
        file_path = "data/solutions/solutions.json"
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"\n❌ Error: File solutions.json tidak ditemukan!")
        return None
    except json.JSONDecodeError:
        print(f"\n❌ Error: File solutions.json memiliki format yang salah!")
        return None


def get_solution(jenis_tes, kategori):
    """
    Mengambil solusi spesifik berdasarkan jenis tes dan kategori
    Args:
        jenis_tes (str) - jenis tes (contoh: 'keluarga', 'burnout')
        kategori (str) - kategori hasil (contoh: 'kritis', 'buruk', 'cukup', 'baik')
    Returns: dict - data solusi atau None
    """
    all_solutions = load_solutions()
    
    if not all_solutions:
        return None
    
    try:
        return all_solutions[jenis_tes][kategori]
    except KeyError:
        print(f"\n❌ Solusi untuk {jenis_tes} - {kategori} tidak ditemukan!")
        return None


def tampilkan_instruksi(data_kuisioner):
    """
    Menampilkan informasi dan instruksi kuisioner
    """
    print("\n" + "="*70)
    print(f"📋 {data_kuisioner['nama']}".center(70))
    print("="*70)
    print(f"\n📖 {data_kuisioner['deskripsi']}")
    print(f"\n💡 Instruksi: {data_kuisioner['instruksi']}")
    
    print("\n📊 Skala Penilaian:")
    for nilai, label in data_kuisioner['skala'].items():
        print(f"   [{nilai}] = {label}")
    
    print("\n" + "-"*70)
    print("⚠️  Jawab dengan jujur untuk hasil yang akurat!")
    print("-"*70)


def jalankan_kuisioner(jenis_tes):
    """
    Menjalankan kuisioner dan mengembalikan hasil
    """
    # Load data kuisioner
    data = load_questionnaire(jenis_tes)
    if not data:
        return None
    
    # Tampilkan instruksi
    tampilkan_instruksi(data)
    
    input("\n👉 Tekan Enter untuk memulai tes...")
    
    # Array untuk menyimpan jawaban
    jawaban = []
    total_skor = 0
    
    # Loop untuk setiap pertanyaan
    for i, pertanyaan in enumerate(data['pertanyaan'], 1):
        print(f"\n{'='*70}")
        print(f"Pertanyaan {i} dari {len(data['pertanyaan'])}")
        print(f"{'='*70}")
        print(f"\n{pertanyaan['teks']}")
        
        # Tampilkan opsi jawaban
        print("\nPilihan:")
        for nilai, label in data['skala'].items():
            print(f"  [{nilai}] {label}")
        
        # Input dan validasi
        while True:
            try:
                user_input = input(f"\nJawaban Anda (1-5): ").strip()
                
                if user_input not in ['1', '2', '3', '4', '5']:
                    print("❌ Input tidak valid! Masukkan angka 1-5.")
                    continue
                
                nilai = int(user_input)
                
                # Handle reverse scoring
                if pertanyaan.get('reverse', False):
                    skor = 6 - nilai
                else:
                    skor = nilai
                
                total_skor += skor
                
                jawaban.append({
                    'pertanyaan_id': pertanyaan['id'],
                    'pertanyaan': pertanyaan['teks'],
                    'jawaban': nilai,
                    'skor': skor
                })
                
                break
                
            except ValueError:
                print("❌ Input tidak valid! Masukkan angka 1-5.")
    
    # Tentukan hasil berdasarkan scoring
    hasil_analisis = analisis_skor(total_skor, data['scoring'])
    
    # Compile hasil lengkap
    hasil = {
        'jenis_tes': jenis_tes,
        'nama_tes': data['nama'],
        'tanggal': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'total_pertanyaan': len(data['pertanyaan']),
        'total_skor': total_skor,
        'skor_maksimal': len(data['pertanyaan']) * 5,
        'jawaban': jawaban,
        'analisis': hasil_analisis
    }
    
    return hasil


def analisis_skor(total_skor, scoring_data):
    """
    Menganalisis skor dan menentukan kategori
    """
    for range_data in scoring_data['ranges']:
        if range_data['min'] <= total_skor <= range_data['max']:
            return {
                'skor': total_skor,
                'level': range_data['level'],
                'kategori': range_data['kategori']
            }
    
    return {
        'skor': total_skor,
        'level': 'Unknown',
        'kategori': 'unknown'
    }


def tampilkan_hasil(hasil):
    """
    Menampilkan hasil kuisioner (HANYA SKOR DAN LEVEL)
    """
    if not hasil:
        return
    
    print("\n\n" + "="*70)
    print("🎯 HASIL TES KESEHATAN MENTAL 🎯".center(70))
    print("="*70)
    
    print(f"\n📋 Jenis Tes: {hasil['nama_tes']}")
    print(f"📅 Tanggal: {hasil['tanggal']}")
    print(f"📊 Total Skor: {hasil['total_skor']} / {hasil['skor_maksimal']}")
    
    print("\n" + "="*70)
    print("📈 ANALISIS HASIL".center(70))
    print("="*70)
    
    analisis = hasil['analisis']
    
    # Load solution untuk mendapatkan emoji
    solution = get_solution(hasil['jenis_tes'], analisis['kategori'])
    
    if solution:
        print(f"\n{solution['emoji']} Tingkat: {solution['level']}")
    else:
        print(f"\n⚪ Tingkat: {analisis['level']}")
    
    print("\n" + "="*70)


def tampilkan_solusi_lengkap(jenis_tes, kategori):
    """
    Menampilkan solusi lengkap: deskripsi, to-do, dan saran
    Args:
        jenis_tes (str) - jenis tes
        kategori (str) - kategori hasil (kritis/buruk/cukup/baik)
    """
    solution = get_solution(jenis_tes, kategori)
    
    if not solution:
        print("\n❌ Solusi tidak ditemukan.")
        return
    
    print("\n" + "="*70)
    print(f"{solution['emoji']} DETAIL HASIL & REKOMENDASI {solution['emoji']}".center(70))
    print("="*70)
    
    # Deskripsi
    print(f"\n📝 DESKRIPSI:")
    print(f"   {solution['deskripsi']}")
    
    # To-Do List
    print(f"\n✅ TO-DO LIST:")
    for i, todo in enumerate(solution['todo'], 1):
        print(f"   {i}. {todo}")
    
    # Saran
    print(f"\n💡 SARAN & REKOMENDASI:")
    for i, saran in enumerate(solution['saran'], 1):
        print(f"   {i}. {saran}")
    
    print("\n" + "="*70)