import pandas as pd
import os

class ArticleRecommender:
    def __init__(self, csv_path='data/articles.csv'):
        self.csv_path = csv_path
        self.articles = self.load_articles()
        
    def load_articles(self):
        if not os.path.exists(self.csv_path):
            # Membuat data default jika file tidak ada
            default_articles = {
                'kategori': ['keluarga', 'depresi', 'kecemasan', 'stress', 'trauma', 'burnout_kerja'],
                'judul': [
                    'Membangun Hubungan Keluarga yang Harmonis',
                    'Memahami dan Mengatasi Gejala Depresi',
                    'Mengelola Kecemasan dalam Kehidupan Sehari-hari',
                    'Teknik Mengatasi Stress yang Efektif',
                    'Pemulihan dari Trauma Psikologis',
                    'Mencegah dan Mengatasi Burnout di Tempat Kerja'
                ],
                'konten': [
                    'Artikel tentang komunikasi sehat dalam keluarga...',
                    'Panduan mengenali dan menangani depresi...',
                    'Strategi praktis mengurangi kecemasan...',
                    'Tips mengelola stress dengan baik...',
                    'Proses penyembuhan dari pengalaman traumatis...',
                    'Cara menjaga keseimbangan kerja dan kehidupan...'
                ],
                'link': [
                    'https://example.com/keluarga',
                    'https://example.com/depresi',
                    'https://example.com/kecemasan',
                    'https://example.com/stress',
                    'https://example.com/trauma',
                    'https://example.com/burnout'
                ],
                'rating': [4.5, 4.8, 4.3, 4.6, 4.7, 4.4]
            }
            df = pd.DataFrame(default_articles)
            # Buat folder data jika belum ada
            os.makedirs('data', exist_ok=True)
            df.to_csv(self.csv_path, index=False)
            return df
        return pd.read_csv(self.csv_path)
    
    def recommend_by_category(self, kategori):
        if kategori not in self.articles['kategori'].values:
            return self.articles.head(3)  # Default: 3 artikel pertama
        
        filtered = self.articles[self.articles['kategori'] == kategori]
        
        if filtered.empty:
            filtered = self.articles.sample(3)
        
        filtered = filtered.sort_values(by='rating', ascending=False)
        
        return filtered.head(3)  # Maksimal 3 artikel
    
    def recommend_by_score(self, kategori, skor):
        """Merekomendasikan artikel berdasarkan kategori dan skor hasil tes"""
        recommendations = []
        
        base_articles = self.recommend_by_category(kategori)
        
        if skor > 70:  
            urgent_articles = self.articles[
                (self.articles['kategori'] == kategori) & 
                (self.articles['rating'] >= 4.5)
            ]
            if not urgent_articles.empty:
                recommendations.append(urgent_articles.iloc[0])
        
        elif skor > 40: 
            medium_articles = self.articles[
                (self.articles['kategori'] == kategori) & 
                (self.articles['rating'] >= 4.0)
            ]
            if not medium_articles.empty:
                recommendations.append(medium_articles.iloc[0])
        
        for _, article in base_articles.iterrows():
            recommendations.append(article)
        
        unique_recommendations = []
        seen_titles = set()
        for article in recommendations:
            if article['judul'] not in seen_titles:
                unique_recommendations.append(article)
                seen_titles.add(article['judul'])
        
        return unique_recommendations[:3]  

def tampilkan_artikel_rekomendasi(jenis_tes=None, skor=None):
    """Fungsi utama untuk menampilkan artikel rekomendasi"""
    from tabulate import tabulate
    
    recommender = ArticleRecommender()
    
    print("\n" + "="*60)
    print("📚 ARTIKEL REKOMENDASI UNTUK ANDA")
    print("="*60)
    
    if jenis_tes and skor:
        print(f"Berdasarkan hasil tes {jenis_tes} dengan skor: {skor}\n")
        articles = recommender.recommend_by_score(jenis_tes, skor)
    elif jenis_tes:
        print(f"Berdasarkan kategori: {jenis_tes}\n")
        articles = recommender.recommend_by_category(jenis_tes)
    else:
        print("Artikel Terpopuler:\n")
        articles = recommender.articles.sort_values(by='rating', ascending=False).head(3)
    
    if articles.empty:
        print("⚠️  Belum ada artikel tersedia untuk kategori ini.")
        return
    
    table_data = []
    for idx, (_, article) in enumerate(articles.iterrows(), 1):
        table_data.append([
            idx,
            article['judul'],
            article['kategori'].capitalize(),
            f"⭐ {article['rating']}/5",
            f"🔗 {article['link']}"
        ])
    
    headers = ["No", "Judul Artikel", "Kategori", "Rating", "Link"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    print("\n" + "-"*60)
    print("Pilihan:")
    print("1. Baca detail artikel")
    print("2. Kembali ke menu utama")
    print("3. Simpan artikel favorit")
    
    pilihan = input("\nPilih opsi (1-3): ").strip()
    
    if pilihan == '1':
        print("\n" + "="*60)
        nomor = input("Masukkan nomor artikel yang ingin dibaca (1-3): ").strip()
        if nomor.isdigit() and 1 <= int(nomor) <= len(articles):
            idx = int(nomor) - 1
            article = articles.iloc[idx]
            print(f"\n📖 {article['judul']}")
            print(f"Kategori: {article['kategori'].capitalize()}")
            print(f"Rating: ⭐ {article['rating']}/5")
            print(f"Link: {article['link']}")
            print("\n📝 Konten:")
            print(article['konten'])
            input("\nTekan Enter untuk kembali...")
    
    elif pilihan == '3':
        print("\n✅ Fitur penyimpanan favorit akan tersedia segera!")
        input("Tekan Enter untuk melanjutkan...")