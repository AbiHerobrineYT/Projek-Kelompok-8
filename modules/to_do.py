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
    batch_list = list(batches.groups.keys())
    
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
                # Simpan ke CSV
                df.drop(columns=['batch_id']).to_csv(csv_path, index=False)
                print("\n✅ Aktivitas berhasil ditandai selesai!")
            else:
                df.loc[df_index, 'status'] = 'pending'
                df.drop(columns=['batch_id']).to_csv(csv_path, index=False)
                print("\n↩️ Aktivitas dikembalikan ke pending!")
            
            input("Tekan Enter untuk melanjutkan...")
        
        else:
            print("\n❌ Pilihan tidak valid!")
            input("Tekan Enter untuk melanjutkan...")