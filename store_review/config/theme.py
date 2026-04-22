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

/* Tam genişlik header taşması — Streamlit ana sütunu kırpmasın */
[data-testid="stAppViewContainer"] .main,
[data-testid="stAppViewContainer"] .main .block-container {
  overflow-x: visible !important;
}

/*
 * Masthead — yalnızca .st-key-pg_masthead (+ eski BorderWrapper). :has(.hero-masthead-brand) kullanma:
 * üst stVerticalBlock tüm sayfayı sarınca sayfa içi tüm radyolara da uygulanıyordu.
 */
[data-testid="stVerticalBlock"].st-key-pg_masthead,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead {
  width: 100vw !important;
  min-width: 100vw !important;
  max-width: 100vw !important;
  position: relative !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
  margin-top: -1.25rem !important;
  margin-bottom: 16px !important;
  padding: 14px clamp(18px, 4vw, 44px) 16px !important;
  box-sizing: border-box !important;
  min-height: 88px !important;
  border: none !important;
  border-radius: 0 0 22px 22px !important;
  border-bottom: 1px solid rgba(0, 0, 0, 0.14) !important;
  box-shadow: 0 10px 32px rgba(6, 42, 40, 0.32) !important;
  overflow: hidden !important;
  background: linear-gradient(
    102deg,
    #050f14 0%,
    #0a1f24 18%,
    #0c2e32 40%,
    #115e59 68%,
    #0f766e 88%,
    #14b8a6 100%
  ) !important;
}

[data-testid="stVerticalBlock"].st-key-pg_masthead::after,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead::after {
  content: "" !important;
  position: absolute !important;
  inset: 0 !important;
  pointer-events: none !important;
  border-radius: inherit !important;
  opacity: 0.05 !important;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Cpath fill='%23ffffff' d='M11 5h2v6h6v2h-6v6h-2v-6H5v-2h6z'/%3E%3C/svg%3E") !important;
  background-size: 24px 24px !important;
}

.hero-band-target {
  position: absolute !important;
  width: 1px !important;
  height: 1px !important;
  padding: 0 !important;
  margin: -1px !important;
  overflow: hidden !important;
  clip: rect(0, 0, 0, 0) !important;
  white-space: nowrap !important;
  border: 0 !important;
}

[data-testid="stVerticalBlock"].st-key-pg_masthead div[data-testid="stMarkdownContainer"]:has(.hero-band-target),
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead div[data-testid="stMarkdownContainer"]:has(.hero-band-target) {
  margin-bottom: 0 !important;
}

.hero-masthead-brand {
  display: flex !important;
  align-items: center !important;
  min-width: 0 !important;
}

.hero-masthead-brand .hero-title {
  font-family: 'Poppins', sans-serif;
  font-size: clamp(1.1rem, 2.4vw, 1.5rem);
  font-weight: 700;
  color: #ffffff;
  margin: 0 !important;
  letter-spacing: -0.02em;
  text-align: left !important;
  line-height: 1.2;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.35);
}

[data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stHorizontalBlock"],
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stHorizontalBlock"] {
  width: 100% !important;
  align-items: center !important;
}

[data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:first-child,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:first-child {
  display: flex !important;
  align-items: center !important;
  min-width: 0 !important;
}

[data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:last-child,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:last-child {
  display: flex !important;
  justify-content: flex-end !important;
  align-items: center !important;
  flex-wrap: wrap !important;
  gap: 8px !important;
}

[data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stRadio"],
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stRadio"] {
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-end !important;
  width: 100% !important;
}

[data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stRadioGroup"],
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stRadioGroup"],
[data-testid="stVerticalBlock"].st-key-pg_masthead .stRadio div[role="radiogroup"],
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead .stRadio div[role="radiogroup"] {
  display: inline-flex !important;
  flex-wrap: wrap !important;
  justify-content: flex-end !important;
  align-items: center !important;
  gap: 2px !important;
  margin: 0 !important;
  margin-left: auto !important;
  padding: 6px 8px !important;
  width: auto !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
  background: rgba(0, 0, 0, 0.26) !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  border-radius: 20px !important;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.2) !important;
}

[data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stRadioGroup"] label,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stRadioGroup"] label,
[data-testid="stVerticalBlock"].st-key-pg_masthead .stRadio div[role="radiogroup"] label,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead .stRadio div[role="radiogroup"] label {
  position: relative !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  flex: 0 1 auto !important;
  margin: 0 !important;
  min-height: 40px !important;
  padding: 8px 12px !important;
  border-radius: 14px !important;
  border: none !important;
  background: transparent !important;
  box-shadow: none !important;
  cursor: pointer !important;
  transition: background 0.15s ease, color 0.15s ease, box-shadow 0.15s ease !important;
}

[data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stRadioGroup"] label span,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stRadioGroup"] label span,
[data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stRadioGroup"] label p,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stRadioGroup"] label p,
[data-testid="stVerticalBlock"].st-key-pg_masthead .stRadio div[role="radiogroup"] label span,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead .stRadio div[role="radiogroup"] label span,
[data-testid="stVerticalBlock"].st-key-pg_masthead .stRadio div[role="radiogroup"] label p,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead .stRadio div[role="radiogroup"] label p {
  color: #ffffff !important;
  font-weight: 500 !important;
  font-size: 0.82rem !important;
}

[data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stRadioGroup"] label:hover:not(:has(input:checked)),
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stRadioGroup"] label:hover:not(:has(input:checked)),
[data-testid="stVerticalBlock"].st-key-pg_masthead .stRadio div[role="radiogroup"] label:hover:not(:has(input:checked)),
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead .stRadio div[role="radiogroup"] label:hover:not(:has(input:checked)) {
  background: rgba(255, 255, 255, 0.08) !important;
}

[data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stRadioGroup"] label:has(input:checked),
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stRadioGroup"] label:has(input:checked),
[data-testid="stVerticalBlock"].st-key-pg_masthead .stRadio div[role="radiogroup"] label:has(input:checked),
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead .stRadio div[role="radiogroup"] label:has(input:checked) {
  background: #ffffff !important;
  border-radius: 20px !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.18) !important;
}

[data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stRadioGroup"] label:has(input:checked) span,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stRadioGroup"] label:has(input:checked) span,
[data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stRadioGroup"] label:has(input:checked) p,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stRadioGroup"] label:has(input:checked) p,
[data-testid="stVerticalBlock"].st-key-pg_masthead .stRadio div[role="radiogroup"] label:has(input:checked) span,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead .stRadio div[role="radiogroup"] label:has(input:checked) span,
[data-testid="stVerticalBlock"].st-key-pg_masthead .stRadio div[role="radiogroup"] label:has(input:checked) p,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead .stRadio div[role="radiogroup"] label:has(input:checked) p {
  color: #0b2f2c !important;
  font-weight: 600 !important;
}

[data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stRadioGroup"] label input[type="radio"],
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stRadioGroup"] label input[type="radio"],
[data-testid="stVerticalBlock"].st-key-pg_masthead .stRadio div[role="radiogroup"] label input[type="radio"],
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead .stRadio div[role="radiogroup"] label input[type="radio"] {
  position: absolute !important;
  opacity: 0 !important;
  width: 0 !important;
  height: 0 !important;
  margin: 0 !important;
  pointer-events: none !important;
}

[data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stRadioGroup"] label > input[type="radio"] + div,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stRadioGroup"] label > input[type="radio"] + div,
[data-testid="stVerticalBlock"].st-key-pg_masthead .stRadio div[role="radiogroup"] label > input[type="radio"] + div,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead .stRadio div[role="radiogroup"] label > input[type="radio"] + div {
  display: none !important;
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

/* Yorum kartları — tek sütun, tablo yerine */
.review-card-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin: 14px 0 8px;
}
.review-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 14px 16px 16px;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
}
.review-card-app {
  font-size: 0.78rem;
  font-weight: 600;
  color: #6366f1;
  margin: 0 0 8px 0;
}
.review-card-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  font-size: 0.86rem;
  color: #475569;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f1f5f9;
}
.review-card-head-left {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  font-weight: 600;
  color: #334155;
}
.review-card-no {
  font-variant-numeric: tabular-nums;
}
.review-card-sep {
  color: #cbd5e1;
  font-weight: 400;
  user-select: none;
}
.review-card-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
  flex-shrink: 0;
  box-shadow: 0 0 0 1px rgba(15, 23, 42, 0.06);
}
.review-card-date {
  color: #64748b;
  font-weight: 500;
  font-size: 0.86rem;
  margin-left: auto;
}
.review-card-body {
  font-size: 0.94rem;
  line-height: 1.55;
  color: #1e293b;
  white-space: pre-wrap;
  word-break: break-word;
}
"""
