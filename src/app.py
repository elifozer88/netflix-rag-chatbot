import streamlit as st
from rag_pipeline import RAGPipeline
import time
import pandas as pd

# Sayfa ayarları
st.set_page_config(
    page_title="Netflix RAG Chatbot",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state'de tema sakla
if 'theme' not in st.session_state:
    st.session_state.theme = 'netflix'

# Tema tanımları
themes = {
    'netflix': {
        'name': 'Netflix',
        'bg_primary': '#141414',
        'bg_secondary': '#1f1f1f',
        'accent': '#E50914',
        'text': '#ffffff',
        'text_secondary': '#b3b3b3',
        'card_bg': '#2a2a2a',
        'input_bg': '#333333'
    },
    'light': {
        'name': 'Aydınlık',
        'bg_primary': '#f8f9fa',
        'bg_secondary': '#ffffff',
        'accent': '#0d6efd',
        'text': '#212529',
        'text_secondary': '#6c757d',
        'card_bg': '#ffffff',
        'input_bg': '#f8f9fa'
    },
    'ocean': {
        'name': 'Okyanus',
        'bg_primary': '#0a1929',
        'bg_secondary': '#132f4c',
        'accent': '#00b4d8',
        'text': '#ffffff',
        'text_secondary': '#90caf9',
        'card_bg': '#1e3a5f',
        'input_bg': '#244560'
    },
    'sunset': {
        'name': 'Gün Batımı',
        'bg_primary': '#2d1b1b',
        'bg_secondary': '#3d2626',
        'accent': '#ff6b35',
        'text': '#ffffff',
        'text_secondary': '#ffb4a2',
        'card_bg': '#4a3030',
        'input_bg': '#5a3838'
    }
}

current_theme = themes[st.session_state.theme]

# === CSS STİLLERİ ===
st.markdown(f"""
<style>
    /* Üst boşlukları kaldır ama orta alanı aşağı al */
    header[data-testid="stHeader"] {{
        display: none !important;
    }}
    .block-container {{
        padding-top: 4rem !important;
        margin-top: 0 !important;
        max-width: 1200px !important;
    }}

    /* Arka plan */
    .stApp {{
        background: linear-gradient(135deg, {current_theme['bg_primary']} 0%, {current_theme['bg_secondary']} 100%);
    }}

    /* Başlıklar */
    h1, h2, h3, h4 {{
        color: {current_theme['text']} !important;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {current_theme['bg_secondary']} !important;
    }}
    [data-testid="stSidebar"] * {{
        color: {current_theme['text']} !important;
    }}

    /* Input */
    .stTextInput input {{
        background-color: {current_theme['input_bg']} !important;
        color: {current_theme['text']} !important;
        border: 2px solid {current_theme['accent']} !important;
        border-radius: 12px !important;
        padding: 15px !important;
        font-size: 16px !important;
    }}
    .stTextInput input::placeholder {{
        color: {current_theme['text_secondary']} !important;
    }}

    /* Butonlar */
    .stButton button {{
        background: linear-gradient(90deg, {current_theme['accent']} 0%, {current_theme['accent']}dd 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 30px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        transition: all 0.3s !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }}
    .stButton button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px {current_theme['accent']}66 !important;
    }}

    /* Selectbox (tema seçici) */
    div[data-baseweb="select"] > div {{
        background-color: #000 !important;
        color: #fff !important;
        border: 2px solid {current_theme['accent']} !important;
        border-radius: 10px !important;
        box-shadow: 0 0 8px {current_theme['accent']}33 !important;
    }}
    div[data-baseweb="select"] * {{
        color: #fff !important;
    }}

    /* === REFERANS İÇERİKLERİ === */
    .streamlit-expanderHeader {{
        background: linear-gradient(90deg, {current_theme['card_bg']} 0%, {current_theme['bg_secondary']} 100%) !important;
        color: {current_theme['text']} !important;
        border: 1px solid {current_theme['accent']}44 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 10px 14px !important;
    }}
    .streamlit-expanderContent {{
        background-color: {current_theme['card_bg']} !important;
        color: {current_theme['text']} !important;
        border-left: 3px solid {current_theme['accent']}aa !important;
        border-radius: 0 0 10px 10px !important;
        padding: 15px !important;
    }}
    .streamlit-expanderContent p {{
        color: {current_theme['text']} !important;
        opacity: 0.9 !important;
    }}

    /* Metric */
    [data-testid="stMetricValue"] {{
        color: {current_theme['accent']} !important;
        font-weight: bold !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {current_theme['text_secondary']} !important;
    }}
</style>
""", unsafe_allow_html=True)

# === ANA BAŞLIK ===
st.markdown("# 🎬 Netflix RAG Chatbot")
st.markdown("### Netflix içeriklerini sorgulayabilir ve yapay zeka destekli yanıtlar alabilirsiniz.")

# === SIDEBAR ===
with st.sidebar:
    st.markdown("## ⚙️ Ayarlar & Kontrol Paneli")
    st.markdown("---")
    
    st.markdown("### 🎨 Renk Teması")
    theme_options = {v['name']: k for k, v in themes.items()}
    selected_theme_name = st.selectbox(
        "Tema Seç",
        options=list(theme_options.keys()),
        index=list(theme_options.keys()).index(themes[st.session_state.theme]['name']),
        label_visibility="collapsed"
    )
    if theme_options[selected_theme_name] != st.session_state.theme:
        st.session_state.theme = theme_options[selected_theme_name]
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Referans Ayarları")
    top_k = st.slider("Kaç içerik referans alınsın?", 1, 10, 5)
    st.metric("Seçilen Referans", f"{top_k} içerik")

    st.markdown("---")
    show_references = st.checkbox("📚 Referans içerikleri göster", value=True)
    show_metadata = st.checkbox("🔍 Detaylı bilgi göster", value=True)

    st.markdown("---")
    if 'message_count' not in st.session_state:
        st.session_state.message_count = 0
    st.markdown("### 📈 İstatistikler")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💬 Soru", st.session_state.message_count)
    with col2:
        st.metric("🎬 Film", len(st.session_state.get('last_results', [])) if 'last_results' in st.session_state else 0)
    
    st.markdown("---")
    if st.button("🔄 Sayfayı Yenile", use_container_width=True):
        st.rerun()
    if st.button("🗑️ Geçmişi Temizle", use_container_width=True):
        st.session_state.message_count = 0
        if 'last_results' in st.session_state:
            del st.session_state.last_results
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Netflix RAG Chatbot v2.0**")
    st.markdown("*Powered by Gemini & LangChain*")

# === RAG PIPELINE ===
@st.cache_resource(show_spinner=False)
def load_rag():
    with st.spinner("🔄 Sistem başlatılıyor..."):
        return RAGPipeline()

try:
    rag = load_rag()
    st.success("✅ Sistem hazır! Sorularınızı sorabilirsiniz.", icon="✅")
except Exception as e:
    st.error(f"❌ RAG Pipeline yüklenemedi: {e}")
    st.stop()

# === SORU ALANI ===
st.markdown("### 🔍 Sorunuzu Sorun")
query = st.text_input(
    "Mesajınızı yazın...",
    value=st.session_state.get('query', ''),
    placeholder="Örn: Aksiyon dolu filmler önerir misin?",
    label_visibility="collapsed",
    key="query_input"
)

if query:
    st.session_state.message_count += 1
    st.markdown("---")
    st.markdown("### 💬 Sizin Sorunuz:")
    st.info(query)

    with st.spinner("🤔 Yanıt hazırlanıyor... Yapay zeka analiz ediyor..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        progress_bar.empty()

        try:
            answer = rag.generate_answer(query, top_k=top_k)
            st.markdown("### ✅ Chatbot Yanıtı:")
            st.success(answer)

            if show_references:
                st.markdown("---")
                st.markdown("### 📚 Referans İçerikler:")
                docs = rag.retrieve(query, top_k=top_k)
                st.session_state.last_results = docs

                cols = st.columns(2)
                for idx, (_, row) in enumerate(docs.iterrows(), 1):
                    with cols[(idx - 1) % 2]:
                        with st.expander(f"📺 {idx}. {row['title']}", expanded=False):
                            if show_metadata:
                                st.markdown(f"**🎭 Tür:** {row['listed_in']}")
                                st.markdown(f"**📝 Açıklama:** {row['description']}")
                                if 'release_year' in row and pd.notna(row['release_year']):
                                    st.markdown(f"**📅 Yıl:** {int(row['release_year'])}")
                                if 'rating' in row and pd.notna(row['rating']):
                                    st.markdown(f"**⭐ Yaş:** {row['rating']}")
                            else:
                                st.markdown(f"{row['description'][:100]}...")

            st.balloons()

        except Exception as e:
            st.error(f"❌ Hata oluştu: {e}")

#
