import streamlit as st
from rag_pipeline import RAGPipeline

# Streamlit sayfa ayarları
st.set_page_config(page_title="Netflix RAG Chatbot", layout="wide")
st.title("🎬 Netflix RAG Chatbot")
st.markdown("Netflix içeriklerini sorgulayabilir ve doğal dil yanıt alabilirsiniz.")

# Sidebar ayarları
st.sidebar.title("⚙️ Ayarlar")
top_k = st.sidebar.slider("Kaç içerik referans alınsın?", min_value=1, max_value=10, value=5)
show_references = st.sidebar.checkbox("Referans içerikleri göster?", value=True)

# RAG pipeline'ı başlat (cache'le = sadece 1 kez yükle)
@st.cache_resource
def load_rag():
    return RAGPipeline()

try:
    rag = load_rag()
except Exception as e:
    st.error(f"❌ RAG Pipeline yüklenemedi: {e}")
    st.info("💡 Lütfen şunları kontrol et:")
    st.info("1. faiss_index/netflix_faiss.index dosyası var mı?")
    st.info("2. faiss_index/netflix_metadata.csv dosyası var mı?")
    st.info("3. OPENAI_API_KEY ortam değişkeni ayarlandı mı?")
    st.stop()

# Ana input bölümü
st.subheader("🔍 Soru Sor")
query = st.text_input(
    "Netflix'te ne izlemeli?", 
    placeholder="Örn: Korku filmleri önerir misin?"
)

if query:
    with st.spinner("🤔 Yanıt oluşturuluyor..."):
        try:
            answer = rag.generate_answer(query, top_k=top_k)
            
            st.subheader("✅ Chatbot Yanıtı:")
            st.write(answer)

            # Referans içerikleri göster
            if show_references:
                st.subheader("📚 Referans İçerikler:")
                docs = rag.retrieve(query, top_k=top_k)
                
                for idx, (_, row) in enumerate(docs.iterrows(), 1):
                    with st.expander(f"📺 {idx}. {row['title']}"):
                        st.markdown(f"**Tür:** {row['listed_in']}")
                        st.markdown(f"**Açıklama:** {row['description']}")
        
        except Exception as e:
            st.error(f"❌ Hata oluştu: {e}")
            st.info("💡 OpenAI API Key'in doğru mu? .env dosyasını kontrol et")