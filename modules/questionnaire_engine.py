import json
import os
from datetime import datetime

def load_questionnaire(jenis_tes):
    """
    Load data kuisioner dari file JSON
    Args: jenis_tes (str) - nama file tanpa .json (contoh: 'keluarga', 'stress')
    Returns: dict - data kuisioner atau None jika error
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
    Args: jenis_tes (str) - jenis kuisioner
    Returns: dict - hasil kuisioner dengan skor dan jawaban
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
                
                # Handle reverse scoring (untuk pertanyaan negatif)
                if pertanyaan.get('reverse', False):
                    skor = 6 - nilai  # Reverse: 1->5, 2->4, 3->3, 4->2, 5->1
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
    Args: 
        total_skor (int) - total skor yang didapat
        scoring_data (dict) - data scoring dari JSON
    Returns: dict - hasil analisis
    """
    for range_data in scoring_data['ranges']:
        if range_data['min'] <= total_skor <= range_data['max']:
            return {
                'skor': total_skor,
                'level': range_data['level'],
                'kategori': range_data['kategori'],
                'deskripsi': range_data['deskripsi']
            }
    
    # Jika tidak ada range yang cocok (seharusnya tidak terjadi)
    return {
        'skor': total_skor,
        'level': 'Unknown',
        'kategori': 'unknown',
        'deskripsi': 'Hasil tidak dapat ditentukan.'
    }


def tampilkan_hasil(hasil):
    """
    Menampilkan hasil kuisioner dengan format yang menarik
    Args: hasil (dict) - hasil dari jalankan_kuisioner()
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
    
    # Icon berdasarkan kategori
    icon_kategori = {
        'kritis': '🔴',
        'perlu_perhatian': '🟠',
        'moderat': '🟡',
        'baik': '🟢',
        'sangat_baik': '💚'
    }
    
    icon = icon_kategori.get(analisis['kategori'], '⚪')
    
    print(f"\n{icon} Tingkat: {analisis['level']}")
    print(f"\n📝 Interpretasi:")
    print(f"   {analisis['deskripsi']}")
    
    print("\n" + "="*70)
    
    # Rekomendasi berdasarkan kategori
    # Ini masih perlu disesuaiin buat setiap jenis tes
    if analisis['kategori'] in ['kritis', 'perlu_perhatian']:
        print("\n⚠️  REKOMENDASI PENTING:")
        print("   • Pertimbangkan untuk konsultasi dengan psikolog atau konselor")
        print("   • Bicarakan dengan orang yang Anda percaya")
        print("   • Jangan ragu mencari bantuan profesional")
    elif analisis['kategori'] == 'moderat':
        print("\n💡 SARAN:")
        print("   • Tingkatkan komunikasi dengan pasangan/keluarga")
        print("   • Luangkan quality time bersama")
        print("   • Diskusikan harapan dan kebutuhan masing-masing")
    else:
        print("\n✨ TETAP JAGA KUALITAS HUBUNGAN:")
        print("   • Pertahankan komunikasi yang terbuka")
        print("   • Terus saling mendukung dan menghargai")
        print("   • Rayakan momen-momen kecil bersama")
    
    print("\n" + "="*70)