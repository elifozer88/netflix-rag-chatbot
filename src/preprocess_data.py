import pandas as pd
from pathlib import Path

# Windows ve Linux'te çalışan path
data_dir = Path('data')
input_file = data_dir / 'netflix_titles.csv'
output_file = data_dir / 'cleaned_netflix.csv'

print(f"📍 Çalışan dizin: {Path.cwd()}")
print(f"📂 Dosya aranıyor: {input_file.absolute()}")

# Dosya var mı kontrol et
if not input_file.exists():
    print(f"❌ Dosya bulunamadı: {input_file}")
    print(f"💡 Lütfen netflix_titles.csv dosyasını {data_dir} klasörüne kopyala")
    exit(1)

print(f"✅ Dosya bulundu!")

# Veriyi oku
df = pd.read_csv(input_file)
print(f"✅ CSV yüklendi: {len(df)} satır")

# Gerekli alanları seç ve eksik değerleri kaldır
df = df[['title', 'listed_in', 'description']].dropna()
print(f"✅ Temizlendi: {len(df)} satır (eksik veriler kaldırıldı)")

# Yeni bir kolon oluştur
df['content'] = (
    "Title: " + df['title'] + " | Genre: " + df['listed_in'] + 
    " | Description: " + df['description']
)

# Kaydet
df.to_csv(output_file, index=False)
print(f"✅ Temiz veri kaydedildi: {output_file}")
print(df.head())