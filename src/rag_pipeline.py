import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import os
from pathlib import Path
from dotenv import load_dotenv

# .env dosyasından ortam değişkenlerini yükle
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini'yi yapılandır
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
else:
    raise ValueError("GEMINI_API_KEY bulunamadı! .env dosyasını kontrol et.")

class RAGPipeline:
    def __init__(self, index_path="faiss_index/netflix_faiss.index", 
                 metadata_path="faiss_index/netflix_metadata.csv",
                 model_name="sentence-transformers/all-MiniLM-L6-v2"):
        """
        RAG pipeline'ı başlat
        - FAISS indexini yükle
        - Metadata CSV'sini yükle
        - Embedding modelini yükle
        """
        # Path'leri pathlib ile düzelt (Windows uyumlu)
        index_path = Path(index_path)
        metadata_path = Path(metadata_path)
        
        if not index_path.exists():
            raise FileNotFoundError(f"FAISS index bulunamadı: {index_path}")
        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata dosyası bulunamadı: {metadata_path}")
        
        self.index = faiss.read_index(str(index_path))
        self.df = pd.read_csv(metadata_path)
        self.embedding_model = SentenceTransformer(model_name)
        print("✅ RAG Pipeline başlatıldı (Gemini ile)")

    def retrieve(self, query, top_k=5):
        """
        Sorguyu al ve FAISS ile en yakın top_k içeriği getir
        """
        # Sorguyu embedding'e çevir
        query_embedding = self.embedding_model.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")
        
        # FAISS'te arama yap
        distances, indices = self.index.search(query_embedding, top_k)
        
        # Sonuçları döndür
        results = self.df.iloc[indices[0]]
        return results

    def generate_answer(self, query, top_k=5):
        """
        1. Retrieval: En yakın içerikleri bul
        2. Augmentation: Context olarak düzenle
        3. Generation: Gemini ile yanıt oluştur
        """
        # Retrieval
        docs = self.retrieve(query, top_k)
        
        # Context oluştur
        context_text = "\n\n".join([
            f"Başlık: {row['title']}\nTür: {row['listed_in']}\nAçıklama: {row['description']}" 
            for _, row in docs.iterrows()
        ])

        # Prompt hazırla
        prompt = f"""Soru: {query}

Aşağıdaki Netflix içerikleri veriliyor:
{context_text}

Yukarıdaki bilgileri kullanarak soruyu Türkçe olarak cevapla. Yanıtında hangi film/dizileri referans aldığını belirt. Kısa ve öz cevap ver."""

        # Gemini'den yanıt al
        response = model.generate_content(prompt)
        
        return response.text