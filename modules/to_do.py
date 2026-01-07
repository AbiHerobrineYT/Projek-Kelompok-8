import os
import pandas as pd

def tampilkan_todo_list(username):
    """
    Menampilkan to-do list user dari CSV dengan navigasi dan checklist interaktif
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(BASE_DIR, "data", "to_do", username, "to_do_list.csv")
    
    if not os.path.exists(csv_path):
        print("\n📭 Anda belum memiliki to-do list.")
        print("💡 Selesaikan tes terlebih dahulu untuk mendapatkan rekomendasi aktivitas.")
        return
    
    # Baca CSV
    df = pd.read_csv(csv_path)
    
    if df.empty:
        print("\n📭 To-do list Anda kosong.")
        return
    
    # Kelompokkan berdasarkan tanggal + test_id (setiap batch tes)
    df['batch_id'] = df['tanggal'] + '_' + df['test_id']
    batches = df.groupby('batch_id')
    batch_list = sorted(batches.groups.keys(), reverse=True)  # ← Tambah sorted + reverse
    
    if not batch_list:
        print("\n📭 To-do list Anda kosong.")
        return
    
    # Mulai dari batch terbaru
    current_index = 0
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
        
        batch_id = batch_list[current_index]
        batch_data = df[df['batch_id'] == batch_id].copy()
        batch_data = batch_data.reset_index(drop=True)
        
        # Tampilkan header
        print("\n" + "=" * 70)
        print("📋 TO-DO LIST SAYA".center(70))
        print("=" * 70)
        
        # Info batch
        tanggal = batch_data.iloc[0]['tanggal']
        test_id = batch_data.iloc[0]['test_id']
        
        print(f"\n🔹 {test_id.upper()} - {tanggal}")
        print(f"📄 Halaman {current_index + 1} dari {len(batch_list)}")
        print("-" * 70)
        
        # Tampilkan aktivitas dengan nomor
        for idx, row in batch_data.iterrows():
            checkbox = "☑" if row['status'] == 'done' else "☐"
            print(f"{idx + 1}. {checkbox} [Prioritas {row['prioritas']}] {row['aktivitas']}")
        
        print("\n" + "=" * 70)
        
        # Menu navigasi
        print("\n🎯 Pilihan:")
        print("  [1-5] Tandai aktivitas selesai")
        
        if current_index < len(batch_list) - 1:
            print("  [N] Selanjutnya →")
        if current_index > 0:
            print("  [P] Sebelumnya ←")
        
        print("  [0] Kembali ke menu utama")
        print("=" * 70)
        
        pilihan = input("\nPilihan Anda: ").strip().lower()
        
        # Proses pilihan
        if pilihan == '0':
            break
        
        elif pilihan == 'n' and current_index < len(batch_list) - 1:
            current_index += 1
        
        elif pilihan == 'p' and current_index > 0:
            current_index -= 1
        
        elif pilihan.isdigit() and 1 <= int(pilihan) <= len(batch_data):
            # Tandai aktivitas selesai
            aktivitas_index = int(pilihan) - 1
            row_data = batch_data.iloc[aktivitas_index]
            
            # Update status di dataframe asli
            df_index = df[(df['batch_id'] == batch_id) & 
                         (df['prioritas'] == row_data['prioritas'])].index[0]
            
            if df.loc[df_index, 'status'] == 'pending':
                df.loc[df_index, 'status'] = 'done'
                df.drop(columns=['batch_id']).to_csv(csv_path, index=False)
                
                # ← TAMBAHAN: Update progress di file hasil
                update_progress_hasil(username, batch_id, csv_path)
                
                print("\n✅ Aktivitas berhasil ditandai selesai!")
            else:
                df.loc[df_index, 'status'] = 'pending'
                df.drop(columns=['batch_id']).to_csv(csv_path, index=False)
                
                # ← TAMBAHAN: Update progress di file hasil
                update_progress_hasil(username, batch_id, csv_path)
                
                print("\n↩️ Aktivitas dikembalikan ke pending!")
            
            input("Tekan Enter untuk melanjutkan...")
        
        else:
            print("\n❌ Pilihan tidak valid!")
            input("Tekan Enter untuk melanjutkan...")

def update_progress_hasil(username, batch_id, csv_path):
    """
    Update status dan progress di file hasil TXT berdasarkan checklist
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Baca CSV untuk hitung progress
    df = pd.read_csv(csv_path)
    
    # ← TAMBAH LAGI batch_id karena sudah di-drop saat save
    df['batch_id'] = df['tanggal'] + '_' + df['test_id']
    
    batch_data = df[df['batch_id'] == batch_id]
    
    total_aktivitas = len(batch_data)
    done_count = len(batch_data[batch_data['status'] == 'done'])
    progress = int((done_count / total_aktivitas) * 100)
    status = "Tuntas" if progress == 100 else "Belum Tuntas"
    
    # Ambil info untuk cari file hasil
    tanggal_raw = batch_data.iloc[0]['tanggal']  # Format: "2026-01-07 20:30:12"
    test_id = batch_data.iloc[0]['test_id']
    
    # Parse tanggal untuk format filename
    tanggal_obj = pd.to_datetime(tanggal_raw)
    file_timestamp = tanggal_obj.strftime('%Y%m%d_%H%M%S')
    
    # Cari file hasil
    hasil_dir = os.path.join(BASE_DIR, "data", "hasil", username)
    target_file = f"{test_id}_{file_timestamp}.txt"
    filepath = os.path.join(hasil_dir, target_file)
    
    if not os.path.exists(filepath):
        print(f"⚠️ File hasil tidak ditemukan: {target_file}")
        return
    
    # Baca file
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Update baris Status dan Progress
    updated_lines = []
    for line in lines:
        if line.startswith("Status     :"):
            updated_lines.append(f"Status     : {status}\n")
        elif line.startswith("Progress   :"):
            updated_lines.append(f"Progress   : {progress}%\n")
        else:
            updated_lines.append(line)
    
    # Tulis ulang file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)