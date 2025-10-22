import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from pathlib import Path

# Windows ve Linux'te çalışan path
data_dir = Path('data')
faiss_dir = Path('faiss_index')
input_file = data_dir / 'cleaned_netflix.csv'
index_file = faiss_dir / 'netflix_faiss.index'
metadata_file = faiss_dir / 'netflix_metadata.csv'

# Klasörleri oluştur
faiss_dir.mkdir(exist_ok=True)

# Dosya var mı kontrol et
if not input_file.exists():
    print(f"❌ Dosya bulunamadı: {input_file}")
    print(f"💡 Önce preprocess_data.py'ı çalıştır")
    exit(1)

# Temizlenmiş veriyi yükle
print(f"📖 Veri yükleniyor: {input_file}")
df = pd.read_csv(input_file)
print(f"✅ Yüklendi: {len(df)} satır")

# Embedding modeli indir (ilk kez uzun sürer)
print("🔹 Embedding modeli yükleniyor...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Her content için embedding oluştur
print("🔹 Embedding'ler oluşturuluyor (bu biraz zaman alabilir)...")
embeddings = model.encode(df['content'].tolist(), show_progress_bar=True)

# NumPy array'e çevir
embeddings = np.array(embeddings).astype("float32")
print(f"✅ {len(embeddings)} embedding oluşturuldu")

# FAISS index oluştur
print("🔹 FAISS index oluşturuluyor...")
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Kaydet
print(f"💾 Kaydediliyor...")
faiss.write_index(index, str(index_file))
df.to_csv(metadata_file, index=False)

print("✅ FAISS veritabanı başarıyla kaydedildi!")
print(f"   📁 Index: {index_file}")
print(f"   📁 Metadata: {metadata_file}")
print(f"   📊 Toplam embedding: {len(embeddings)}")
print(f"   🎯 Embedding boyutu: {embeddings.shape[1]}")