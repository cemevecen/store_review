"""Streamlit görünüm katmanı — açık tema, yüksek kontrast, kart + turuncu CTA."""

APP_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* Font: yalnızca uygulama gövdesi — [class*="css"] kullanma (Streamlit widget'larını bozuyor) */
.stApp {
  font-family: 'Poppins', 'Source Sans Pro', sans-serif;
  background: linear-gradient(180deg, #dbeafe 0%, #eff6ff 45%, #f8fafc 100%) !important;
  color: #0f172a;
}

/* Streamlit 1.33+ kök metin */
.stApp span, .stApp p, .stApp label {
  color: inherit;
}

.block-container {
  padding-top: 1.25rem;
  padding-bottom: 2rem;
  max-width: 820px;
}

/* Widget etiketleri — beyaz yazı / soluk yazı sorununu gider */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label span,
.stWidget > label span {
  color: #0f172a !important;
  font-weight: 500 !important;
}

/* Veri kaynağı — sekme şeridi (segmented / tek vurgu) */
[data-testid="stTabs"] {
  margin-top: 2px;
}
[data-testid="stTabs"] [data-baseweb="tab-list"] {
  display: flex !important;
  width: 100% !important;
  flex-wrap: nowrap !important;
  gap: 8px !important;
  background: linear-gradient(180deg, #eef2f7 0%, #e2e8f0 100%) !important;
  padding: 8px !important;
  border-radius: 16px !important;
  border: 1px solid #d0d9e6 !important;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.75);
}
[data-testid="stTabs"] [data-baseweb="tab"] {
  flex: 1 1 0 !important;
  min-height: 48px !important;
  margin: 0 !important;
  padding: 10px 12px !important;
  border-radius: 12px !important;
  border: 1px solid transparent !important;
  border-bottom: none !important;
  background: transparent !important;
  box-shadow: none !important;
  transition: background 0.16s ease, border-color 0.16s ease, box-shadow 0.16s ease;
}
[data-testid="stTabs"] [data-baseweb="tab"]:hover {
  background: rgba(255, 255, 255, 0.55) !important;
}
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {
  background: #ffffff !important;
  border: 1px solid #a5b4fc !important;
  box-shadow: 0 2px 10px rgba(99, 102, 241, 0.14), 0 1px 2px rgba(15, 23, 42, 0.05) !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] p,
[data-testid="stTabs"] [data-baseweb="tab"] span {
  color: #64748b !important;
  font-weight: 500 !important;
  font-size: 0.88rem !important;
  line-height: 1.35 !important;
  text-align: center !important;
}
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] p,
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] span {
  color: #4338ca !important;
  font-weight: 600 !important;
}
/* BaseWeb seçili sekme alt çizgisi — kart vurgusu yeterli */
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
  visibility: hidden !important;
  height: 0 !important;
  min-height: 0 !important;
}
[data-testid="stTabs"] [data-baseweb="tab-panel"] {
  padding-top: 1.15rem !important;
}

/* Giriş alanları — açık kutu, koyu metin */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div,
textarea {
  background-color: #ffffff !important;
  color: #0f172a !important;
  border: 1px solid #cbd5e1 !important;
  border-radius: 10px !important;
}

/* İpucu metni — gerçek girişle karışmasın diye belirgin şekilde silik */
.stTextInput input::placeholder,
.stTextInput input::-webkit-input-placeholder,
textarea::placeholder,
textarea::-webkit-input-placeholder {
  color: #94a3b8 !important;
  opacity: 0.38 !important;
  font-weight: 400 !important;
}

.stRadio div[role="radiogroup"] label {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 8px 14px;
  margin-right: 8px;
}
.stRadio div[role="radiogroup"] label span {
  color: #0f172a !important;
}

/* Metrik */
[data-testid="stMetricValue"] {
  color: #0f172a !important;
  font-size: 1.5rem;
  font-weight: 700;
}
[data-testid="stMetricLabel"] {
  color: #475569 !important;
}

/* Butonlar */
.stButton > button {
  border-radius: 12px !important;
  font-weight: 600 !important;
}
.stButton > button[kind="primary"] {
  background: linear-gradient(180deg, #fb923c, #ea580c) !important;
  color: #ffffff !important;
  border: none !important;
  box-shadow: 0 4px 14px rgba(234, 88, 12, 0.35);
}
.stButton > button[kind="primary"]:hover {
  border: none !important;
  color: #fff !important;
}
.stButton > button[kind="secondary"] {
  background: #1e293b !important;
  color: #f8fafc !important;
  border: none !important;
}

/* File uploader */
[data-testid="stFileUploader"] section {
  background: #ffffff !important;
  border: 1px dashed #94a3b8 !important;
  border-radius: 12px !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #f1f5f9, #e2e8f0) !important;
  border-right: 1px solid #cbd5e1;
}
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
  color: #1e293b !important;
}

/* Divider / expander / dataframe başlıkları */
hr {
  border-color: #cbd5e1 !important;
}
.streamlit-expanderHeader {
  color: #0f172a !important;
}

/* Dataframe */
div[data-testid="stDataFrame"] {
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
}

/* Üst header — viewport genişliği + pastel (indigo / gök / şeftali) */
[data-testid="stVerticalBlockBorderWrapper"]:has(.hero-title) {
  width: 100vw !important;
  max-width: 100vw !important;
  margin-left: calc(50% - 50vw) !important;
  margin-right: calc(50% - 50vw) !important;
  margin-top: -1.25rem !important;
  margin-bottom: 14px !important;
  padding: calc(1.25rem + 8px) clamp(16px, 4vw, 40px) 18px !important;
  box-sizing: border-box !important;
  background: linear-gradient(
    125deg,
    #eef2ff 0%,
    #e0f2fe 44%,
    #fff7ed 100%
  ) !important;
  border: none !important;
  border-bottom: 1px solid rgba(99, 102, 241, 0.25) !important;
  border-radius: 0 !important;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.7), 0 10px 32px rgba(79, 70, 229, 0.09) !important;
}

.hero-title {
  font-family: 'Poppins', sans-serif;
  font-size: 1.65rem;
  font-weight: 700;
  color: #312e81;
  margin: 0 0 12px 0;
  letter-spacing: -0.02em;
  text-align: center;
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.55);
}

[data-testid="stVerticalBlockBorderWrapper"]:has(.hero-title) [data-baseweb="radio"] > div {
  justify-content: center !important;
  flex-wrap: wrap !important;
  gap: 8px !important;
}

/* Header içi radyo — pastel zeminde */
[data-testid="stVerticalBlockBorderWrapper"]:has(.hero-title) .stRadio div[role="radiogroup"] label {
  background: rgba(255, 255, 255, 0.88) !important;
  border: 1px solid rgba(129, 140, 248, 0.38) !important;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.hero-title) .stRadio div[role="radiogroup"] label span {
  color: #3730a3 !important;
  font-weight: 500 !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.hero-title)
  .stRadio
  div[role="radiogroup"]
  label:has(input:checked) {
  background: #ffffff !important;
  border-color: #a5b4fc !important;
  box-shadow: 0 2px 12px rgba(99, 102, 241, 0.2);
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.hero-title)
  .stRadio
  div[role="radiogroup"]
  label:has(input:checked)
  span {
  color: #4338ca !important;
  font-weight: 600 !important;
}

.fancy-divider {
  height: 1px;
  margin: 20px 0;
  background: linear-gradient(90deg, transparent, #93c5fd, transparent);
}

.metric-strip {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 16px 20px;
  margin: 12px 0;
  box-shadow: 0 2px 12px rgba(15,23,42,0.04);
}
.metric-strip-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
  margin-bottom: 4px;
}
.metric-strip-value {
  font-size: 1.85rem;
  font-weight: 700;
  color: #0f172a;
}

.section-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: #0f172a;
  margin: 18px 0 8px;
}
"""
