🎬 Netflix RAG Chatbot with Gemini

🧠 Projenin Amacı

Bu proje, Google Gemini API ve RAG (Retrieval-Augmented Generation) mimarisi kullanarak geliştirilmiş bir Netflix içerik öneri chatbotudur.

🌐 Live Demo

Uygulamayı canlı olarak buradan test edebilirsiniz:
https://netflix-rag-chatbot-8dfx6pyfbmoewm76tjmb6c.streamlit.app/

Kullanıcılar doğal dilde “Netflix’te ne izlemeliyim?” gibi sorular sorabilir; sistem, Netflix veri setinden uygun dizi veya film önerilerini doğal dil yanıtlarıyla döndürür.

Proje, yapay zekâ tabanlı metin sorgulama, veri indeksleme ve semantik arama yöntemlerini bir araya getirir.

<img width="2878" height="1579" alt="image" src="https://github.com/user-attachments/assets/8740a750-cc36-4298-9f37-f3ed8b8ed4f6" />


📊 Veri Seti Hakkında

Proje kapsamında kullanılan veri seti:
📦 Netflix Movies and TV Shows Dataset — Kaggle

Veri kümesi içeriği:

Dizi ve filmlerin isimleri

Tür (genre) bilgisi

Yayın yılı

Yönetmen, oyuncular, ülke

İçerik tipi (Movie / TV Show)

Açıklama (description)

Veri seti, Kaggle platformundan doğrudan alınmış olup temizleme veya etiketleme işlemi yapılmadan kullanılmıştır.

⚙️ Kullanılan Yöntemler ve Teknolojiler
🔍 RAG (Retrieval-Augmented Generation) Mimarisi

Bu mimari, büyük dil modeline (Gemini) ek bilgi sağlamak için veri tabanından veya embedding dizininden (örneğin FAISS) veri çekmeyi içerir.

Kullanıcı bir sorgu gönderdiğinde:

Sorgu embedding’e dönüştürülür.

FAISS benzeri bir dizin içinde en yakın içerikler bulunur.

Bulunan içerikler Gemini API’ye prompt olarak gönderilir.

Model, doğal dilde bir yanıt üretir.

🧩 Kullanılan Kütüphaneler

google.generativeai → Gemini API bağlantısı

faiss → Vektör indeksleme

pandas, numpy → Veri işleme

streamlit → Web arayüzü

dotenv → Ortam değişkenleri yönetimi

langchain (isteğe bağlı) → Metin bölme / retrieval

🚀 Kodun Çalışma Kılavuzu
1️⃣ Sanal ortam oluşturma
python -m venv venv

2️⃣ Ortamı aktifleştirme

PowerShell:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate

3️⃣ Gerekli kütüphaneleri yükleme
pip install -r requirements.txt

4️⃣ Ortam değişkenlerini tanımla

Proje kök dizininde .env dosyası oluştur ve Gemini API anahtarını ekle:

GEMINI_API_KEY="YOUR_API_KEY"

5️⃣ Uygulamayı başlat

Streamlit arayüzünü başlatmak için:

streamlit run app.py

🧱 Çözüm Mimarisi
Kullanıcı Sorgusu → Embedding Modeli → FAISS Araması → En Yakın Netflix İçerikleri
     ↓
   Gemini API → Doğal Dil Yanıtı → Web Arayüzü (Streamlit)


Veri katmanı: Netflix verileri (Kaggle)
Retrieval katmanı: FAISS vektör dizini
Generation katmanı: Gemini LLM
Sunum katmanı: Streamlit web UI

💻 Web Arayüzü ve Kullanım

Arayüzde kullanıcıya sade bir sohbet ekranı sunulur:

“Netflix'te ne izlemeliyim?”

“Komedi türünde 5 dizi öner”

“Aksiyon filmi öner”

“Bilim kurgu dizilerinden en popüler hangileri?”

🧩 Chatbot, isteğe göre dizi/film adı, tür veya ülke bazında öneriler getirir.
🧠 Yanıtlar Gemini API’den gelir ve kullanıcıya doğal bir şekilde sunulur.


📈 Elde Edilen Sonuçlar

Chatbot, kullanıcıdan gelen doğal dildeki istekleri doğru şekilde anlamaktadır.

Netflix veri setinden ilgili türde içerikleri getirmektedir.

RAG mimarisi sayesinde doğruluk oranı yüksek ve bağlama uygun öneriler sağlanmıştır.

Gemini API, yanıtları akıcı ve kullanıcı dostu biçimde üretmektedir.

Feedback'lerin ardından yaptığım güncellemeler 28.10.2025

🧩 Kullanıcı Dostu Özellikler ve Yenilikler

Bu Streamlit arayüzü, kullanıcı deneyimini iyileştirmek için bir dizi kullanıcı dostu özellik içeriyor:

Tema Seçimi:

Netflix, Aydınlık, Okyanus ve Gün Batımı gibi farklı renk temalarıyla arayüz kişiselleştirilebilir.

Kullanıcı tercihlerine göre tema değiştirmek anında uygulanır.

Referans İçerik Kontrolü:

Kullanıcı, kaç içerik referans alınacağını slider ile seçebilir (1–10).

Referans içerikler ve detayları, isteğe bağlı olarak gösterilip gizlenebilir.

Detaylı Bilgi ve Metadata:

Referans içeriklerde dizi/film türü, açıklama, yayın yılı ve yaş derecelendirmesi gösterilebilir.

Kullanıcı, sadece özet veya tam detay görünümünü seçebilir.

Gerçek Zamanlı İstatistikler:

Kullanıcının sorduğu soru sayısı ve chatbot tarafından sunulan içerik sayısı anlık olarak gösterilir.

Etkileşimli ve Canlı Geri Bildirim:

Soru gönderildiğinde, yanıt hazırlanırken yapay zekânın çalıştığını gösteren animasyonlu bir ilerleme çubuğu kullanılır.

Yanıt tamamlandığında balon animasyonu ile olumlu geri bildirim sağlanır.

Kontrol Paneli:

Sayfa yenileme ve geçmişi temizleme butonları sayesinde kullanıcı deneyimi tamamen kontrol altında.

Chatbot geçmişi temizlendiğinde istatistikler sıfırlanır ve arayüz tazelenir.

Kolay Okunabilir ve Modern Tasarım:

Butonlar, input alanları ve expanders (açılır içerik kutuları) görsel olarak modern ve okunabilir.

Arka plan, başlıklar, metinler ve kartlar için temaya uygun renkler kullanılarak görsel tutarlılık sağlanmıştır.

Bu geliştirmeler, kullanıcıların doğal dilde sorular sorarken rahat ve etkileşimli bir deneyim yaşamalarını sağlıyor ve yapay zekâ tabanlı içerik öneri sistemlerini daha erişilebilir hale getiriyor.




