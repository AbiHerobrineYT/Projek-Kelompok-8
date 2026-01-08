import os
import pandas as pd

def tampilkan_todo_list(username):
    FOLDER_DATA = "data/to_do"
    csv_path = f"{FOLDER_DATA}/{username}/to_do_list.csv"

    
    if not os.path.exists(csv_path):
        print("\n📭 Anda belum memiliki to-do list.")
        print("💡 Selesaikan tes terlebih dahulu untuk mendapatkan rekomendasi aktivitas.")
        return
    
    df = pd.read_csv(csv_path)
    
    if len(df) == 0:
        print("\n📭 To-do list Anda kosong.")
        return


    df['batch_id'] = df['tanggal'] + '_' + df['test_id']
    batch_list = sorted(df['batch_id'].unique(), reverse=True)

    
    if not batch_list:
        print("\n📭 To-do list Anda kosong.")
        return
    
    current_index = 0
    
    while True:        
        batch_id = batch_list[current_index]
        batch_data = df[df['batch_id'] == batch_id].copy()
        batch_data = batch_data.reset_index(drop=True)
        
        print("\n" + "=" * 70)
        print("📋 TO-DO LIST SAYA".center(70))
        print("=" * 70)
        
        baris_pertama = batch_data.iloc[0]

        tanggal = baris_pertama['tanggal']
        test_id = baris_pertama['test_id']

        
        print(f"\n🔹 {test_id.upper()} - {tanggal}")
        print(f"📄 Halaman {current_index + 1} dari {len(batch_list)}")
        print("-" * 70)
        
        for index, data in batch_data.iterrows():

            if data['status'] == 'done':
                checkbox = "☑"
            else:
                checkbox = "☐"

            nomor = index + 1

            prioritas = data['prioritas']
            aktivitas = data['aktivitas']

            print(nomor, ".", checkbox, "[Prioritas", prioritas, "]", aktivitas)

        
        print("\n" + "=" * 70)
        
        print("\n🎯 Pilihan:")
        print("  [1-5] Tandai aktivitas selesai")
        
        if current_index < len(batch_list) - 1:
            print("  [N] Selanjutnya →")
        if current_index > 0:
            print("  [P] Sebelumnya ←")
        
        print("  [0] Kembali ke menu utama")
        print("=" * 70)
        
        pilihan = input("\nPilihan Anda: ").strip().lower()
        
        if pilihan == '0':
            break
        
        elif pilihan == 'n' and current_index < len(batch_list) - 1:
            current_index += 1
        
        elif pilihan == 'p' and current_index > 0:
            current_index -= 1
        
        elif pilihan.isdigit() and 1 <= int(pilihan) <= len(batch_data):
            aktivitas_index = int(pilihan) - 1
            row_data = batch_data.iloc[aktivitas_index]
            
            df_index = df[(df['batch_id'] == batch_id) & 
                         (df['prioritas'] == row_data['prioritas'])].index[0]
            
            status_sekarang = df.loc[df_index, 'status']

            if status_sekarang == 'pending':
                df.loc[df_index, 'status'] = 'done'
                data_simpan = df.drop(columns=['batch_id'])
                data_simpan.to_csv(csv_path, index=False)
                update_progress_hasil(username, batch_id, csv_path)
                print("\n✅ Aktivitas berhasil ditandai selesai!")

            else:
                df.loc[df_index, 'status'] = 'pending'
                df.drop(columns=['batch_id']).to_csv(csv_path, index=False)
                
                update_progress_hasil(username, batch_id, csv_path)
                
                print("\n↩️ Aktivitas dikembalikan ke pending!")
            
            input("Tekan Enter untuk melanjutkan...")
        
        else:
            print("\n❌ Pilihan tidak valid!")
            input("Tekan Enter untuk melanjutkan...")

def update_progress_hasil(username, batch_id, csv_path):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    df = pd.read_csv(csv_path)
    
    df['batch_id'] = df['tanggal'] + '_' + df['test_id']
    
    batch_data = df[df['batch_id'] == batch_id]
    
    total_aktivitas = len(batch_data)
    done_count = len(batch_data[batch_data['status'] == 'done'])
    progress = int((done_count / total_aktivitas) * 100)
    status = "Tuntas" if progress == 100 else "Belum Tuntas"
    
    tanggal_raw = batch_data.iloc[0]['tanggal']
    test_id = batch_data.iloc[0]['test_id']
    
    tanggal_obj = pd.to_datetime(tanggal_raw)
    file_timestamp = tanggal_obj.strftime('%Y%m%d_%H%M%S')
    
    hasil_dir = os.path.join(BASE_DIR, "data", "hasil", username)
    target_file = f"{test_id}_{file_timestamp}.txt"
    filepath = os.path.join(hasil_dir, target_file)
    
    if not os.path.exists(filepath):
        print(f"⚠️ File hasil tidak ditemukan: {target_file}")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    updated_lines = []
    for line in lines:
        if line.startswith("Status     :"):
            updated_lines.append(f"Status     : {status}\n")
        elif line.startswith("Progress   :"):
            updated_lines.append(f"Progress   : {progress}%\n")
        else:
            updated_lines.append(line)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)