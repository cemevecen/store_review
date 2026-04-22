"""Streamlit görünüm katmanı — açık tema, yüksek kontrast, kart + turuncu CTA (eski arayüz referansı)."""

APP_VERSION = "2026-04-22"

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

/* Sekmeler */
.stTabs [data-baseweb="tab-list"] {
  gap: 4px;
  background: rgba(255,255,255,0.65);
  padding: 6px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 10px;
  color: #334155 !important;
}
.stTabs [aria-selected="true"] {
  background: #fff !important;
  box-shadow: 0 1px 3px rgba(15,23,42,0.08);
}
.stTabs [data-baseweb="tab"] p {
  color: #475569 !important;
  font-weight: 500;
}
.stTabs [aria-selected="true"] p {
  color: #c2410c !important;
  font-weight: 600 !important;
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

/* Başlık kartı (HTML) */
.hero-card {
  background: #ffffff;
  border-radius: 18px;
  padding: 22px 26px 18px;
  box-shadow: 0 4px 24px rgba(15, 23, 42, 0.07);
  border: 1px solid #e2e8f0;
  margin-bottom: 8px;
  text-align: center;
}
.hero-title {
  font-family: 'Poppins', sans-serif;
  font-size: 1.65rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
  letter-spacing: -0.02em;
}
.hero-sub {
  font-family: 'Poppins', sans-serif;
  color: #64748b;
  font-size: 0.95rem;
  margin: 10px 0 0 0;
  line-height: 1.45;
}
.hero-version {
  font-size: 0.78rem;
  color: #94a3b8;
  margin-top: 12px;
}

.fancy-divider {
  height: 1px;
  margin: 20px 0;
  background: linear-gradient(90deg, transparent, #93c5fd, transparent);
}

.analysis-hint {
  background: #e0f2fe;
  border: 1px solid #7dd3fc;
  border-radius: 14px;
  padding: 14px 18px;
  margin: 12px 0 18px;
  color: #0c4a6e;
  font-size: 0.92rem;
  line-height: 1.55;
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
