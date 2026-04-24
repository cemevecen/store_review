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
  padding-top: 0.35rem !important;
  padding-bottom: 0.65rem !important;
  padding-left: clamp(0.75rem, 2vw, 1.5rem) !important;
  padding-right: clamp(0.75rem, 2vw, 1.5rem) !important;
  max-width: min(1240px, calc(100vw - 1.5rem)) !important;
  margin-left: auto !important;
  margin-right: auto !important;
}

/* Ana sütun — widget aralıklarını sıkılaştır */
[data-testid="stAppViewContainer"] .main [data-testid="element-container"], [data-testid="stAppScrollToBottomContainer"] [data-testid="element-container"] {
  margin-top: 0 !important;
  margin-bottom: 0.2rem !important;
}
[data-testid="stAppViewContainer"] .main hr, [data-testid="stAppScrollToBottomContainer"] hr {
  margin: 0.25rem 0 !important;
}
[data-testid="stAppViewContainer"] .main .stMarkdown, [data-testid="stAppScrollToBottomContainer"] .stMarkdown {
  margin-bottom: 0.15rem !important;
}
[data-testid="stAppViewContainer"] .main .stRadio, [data-testid="stAppScrollToBottomContainer"] .stRadio {
  margin-bottom: 0.1rem !important;
  padding-bottom: 0 !important;
}
[data-testid="stAppViewContainer"] .main .stButton, [data-testid="stAppScrollToBottomContainer"] .stButton {
  margin-bottom: 0.15rem !important;
}
[data-testid="stAppViewContainer"] .main [data-testid="stMetricContainer"], [data-testid="stAppScrollToBottomContainer"] [data-testid="stMetricContainer"] {
  margin-bottom: 0 !important;
  padding-top: 0.2rem !important;
  padding-bottom: 0.2rem !important;
}
[data-testid="stAppViewContainer"] .main [data-testid="stPlotlyChart"], [data-testid="stAppScrollToBottomContainer"] [data-testid="stPlotlyChart"] {
  margin-top: 0.2rem !important;
  margin-bottom: 0.2rem !important;
}
[data-testid="stAppViewContainer"] .main [data-testid="stColumn"], [data-testid="stAppScrollToBottomContainer"] [data-testid="stColumn"] {
  padding-top: 0 !important;
  padding-bottom: 0 !important;
}
[data-testid="stAppViewContainer"] .main .streamlit-expander, [data-testid="stAppScrollToBottomContainer"] .streamlit-expander {
  margin-top: 0.15rem !important;
  margin-bottom: 0.15rem !important;
}
[data-testid="stAppViewContainer"] .main [data-testid="stCaption"], [data-testid="stAppScrollToBottomContainer"] [data-testid="stCaption"] {
  margin-top: 0.1rem !important;
  margin-bottom: 0.1rem !important;
}
[data-testid="stAppViewContainer"] .main .stProgress, [data-testid="stAppScrollToBottomContainer"] .stProgress {
  margin-top: 0.15rem !important;
  margin-bottom: 0.15rem !important;
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
[data-testid="stAppScrollToBottomContainer"],
[data-testid="stAppViewContainer"] .main .block-container,
[data-testid="stAppScrollToBottomContainer"] [data-testid="stMainBlockContainer"] {
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
  margin-bottom: 6px !important;
  padding: 30px clamp(18px, 4vw, 44px) 20px !important;
  box-sizing: border-box !important;
  min-height: 108px !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 14px !important;
  border: none !important;
  border-radius: 0 0 22px 22px !important;
  border-bottom: 1px solid rgba(0, 0, 0, 0.14) !important;
  box-shadow: 0 10px 32px rgba(48, 8, 16, 0.38) !important;
  overflow: hidden !important;
  /* Bordo / şarap tonları (önceki teal yerine) */
  background: linear-gradient(
    102deg,
    #120608 0%,
    #1f0a0e 18%,
    #3a0f18 40%,
    #5c1524 62%,
    #7a1f30 82%,
    #8f2840 100%
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
  margin-top: 14px !important;
}

.hero-masthead-brand {
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: wrap !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 12px !important;
  min-width: 0 !important;
  width: 100% !important;
  max-width: min(100%, 720px) !important;
  margin-left: auto !important;
  margin-right: auto !important;
  text-align: center !important;
}

.hero-brand-logo {
  width: 48px !important;
  height: 48px !important;
  border-radius: 12px !important;
  object-fit: contain !important;
  flex-shrink: 0 !important;
  background: rgba(255, 255, 255, 0.08) !important;
  box-shadow: 0 2px 14px rgba(0, 0, 0, 0.25) !important;
}

.hero-masthead-brand .hero-title {
  font-family: 'Poppins', sans-serif;
  font-size: clamp(1.1rem, 2.4vw, 1.5rem);
  font-weight: 700;
  color: #ffffff;
  margin: 0 !important;
  letter-spacing: -0.02em;
  text-align: center !important;
  line-height: 1.2;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.35);
}

[data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stHorizontalBlock"],
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stHorizontalBlock"] {
  width: 100% !important;
  align-items: stretch !important;
  min-height: 78px !important;
}

/* Masthead — orta sütun: başlık + pills tam ortada (yatay + dikey) */
[data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(2),
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(2) {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 12px !important;
  text-align: center !important;
  min-height: 78px !important;
}

/* Masthead — st.pills satırı ortada */
[data-testid="stVerticalBlock"].st-key-pg_masthead .st-key-main_data_source_tab,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead .st-key-main_data_source_tab {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  width: 100% !important;
  margin-left: auto !important;
  margin-right: auto !important;
}

/* Masthead — dil seçici (yalnızca bayrak); geniş etiket yok */
[data-testid="stVerticalBlock"].st-key-pg_masthead .st-key-_masthead_lang label,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead .st-key-_masthead_lang label {
  display: none !important;
}
[data-testid="stVerticalBlock"].st-key-pg_masthead .st-key-_masthead_lang [data-baseweb="select"] > div,
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead .st-key-_masthead_lang [data-baseweb="select"] > div {
  border-radius: 12px !important;
  background: rgba(255, 255, 255, 0.95) !important;
  border: 1px solid rgba(255, 255, 255, 0.35) !important;
  box-shadow: none !important;
  min-height: 42px !important;
  min-width: 52px !important;
  font-size: 1.35rem !important;
  line-height: 1 !important;
  justify-content: center !important;
}

/* Masthead: başlık dışındaki markdown kutularında üst margin sıfır (başlık kutusu yukarıda 14px alır) */
[data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stMarkdownContainer"]:not(:has(.hero-masthead-brand)),
[data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stMarkdownContainer"]:not(:has(.hero-masthead-brand)) {
  margin-top: 0 !important;
}

.metric-strip {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 10px 14px;
  margin: 2px 0 4px;
  box-shadow: 0 2px 12px rgba(15,23,42,0.04);
}
.metric-strip-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
  margin-bottom: 2px;
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
  margin: 4px 0 2px;
}
.section-title--tight {
  margin-top: 2px !important;
  margin-bottom: 2px !important;
}

/* Chip'i barındıran row'un dikey hizası: pill satırıyla aynı baseline. */
[data-testid="stHorizontalBlock"]:has(.hero-about-chip-wrap) {
  align-items: center !important;
}
[data-testid="stHorizontalBlock"]:has(.hero-about-chip-wrap) > [data-testid="stColumn"] {
  align-self: center !important;
  display: flex;
  align-items: center;
}
.hero-about-chip-wrap {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
.hero-about-chip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  height: 40px;
  padding: 0 16px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.38);
  color: #ffffff !important;
  background: rgba(255, 255, 255, 0.10);
  text-decoration: none !important;
  font-size: 0.82rem;
  font-weight: 600;
  line-height: 1;
  white-space: nowrap;
  box-sizing: border-box;
  transition: transform 0.12s ease, background 0.16s ease, border-color 0.16s ease;
}
.hero-about-chip:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.65);
  transform: translateY(-1px);
}
.hero-about-chip-dot {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.55);
  font-size: 0.7rem;
  font-weight: 700;
  line-height: 1;
}
.about-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 14px 16px;
  margin: 4px 0 8px;
  box-shadow: 0 2px 12px rgba(15, 23, 42, 0.05);
}
.about-card p {
  margin: 0 0 10px;
  font-size: 0.92rem;
  color: #1e293b;
  line-height: 1.6;
}
.about-card p:last-child {
  margin-bottom: 0;
}
.about-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin: 6px 0 12px;
}
.about-kpi {
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
  padding: 10px 11px;
}
.about-kpi span {
  display: block;
  font-size: 0.72rem;
  color: #64748b;
  margin-bottom: 4px;
  font-weight: 600;
}
.about-kpi strong {
  display: block;
  font-size: 0.82rem;
  color: #0f172a;
  line-height: 1.45;
}
.about-table-wrap {
  margin: 10px 0 0;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: auto;
  background: #ffffff;
}
.about-table {
  width: 100%;
  min-width: 640px;
  border-collapse: collapse;
}
.about-table thead th {
  background: #f8fafc;
  color: #334155;
  font-size: 0.78rem;
  font-weight: 700;
  text-align: left;
  padding: 10px 12px;
  border-bottom: 1px solid #e2e8f0;
}
.about-table tbody td {
  font-size: 0.84rem;
  color: #1e293b;
  padding: 10px 12px;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: top;
}
.about-table tbody tr:last-child td {
  border-bottom: none;
}

/* Yorum kartları — tek sütun, tablo yerine */
.review-card-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 4px 0 4px;
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

/* Analiz sonuçları — nlp-sentiment tarzı üst metrik + özet */
.sr-analysis-page-title {
  font-size: 1.35rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0.35rem 0 0.45rem;
  letter-spacing: -0.02em;
}
.sr-analysis-page-title--sub {
  font-size: 1.05rem;
  color: #1f2937;
  margin: 0.25rem 0 0.55rem;
  padding: 0.4rem 0.75rem;
  background: linear-gradient(135deg, rgba(255,237,213,0.65), rgba(255,255,255,0));
  border-left: 3px solid #fb923c;
  border-radius: 6px;
  display: block;
}
.sr-analysis-metric-row {
  display: flex;
  justify-content: center;
  gap: 0.6rem;
  margin: 0.15rem 0 0.75rem;
  flex-wrap: wrap;
}
.sr-analysis-metric-pill {
  background: #ffffff !important;
  border: 2px solid #ffe4d6 !important;
  border-radius: 100px !important;
  padding: 0.55rem 0.75rem !important;
  text-align: center;
  flex: 1 1 128px;
  max-width: 188px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04) !important;
}
.sr-analysis-metric-value {
  font-size: 1.75rem;
  font-weight: 800;
  line-height: 1.15;
}
.sr-analysis-metric-label {
  font-size: 0.72rem;
  color: #64748b !important;
  font-weight: 600;
  margin-top: 0.15rem;
  text-transform: lowercase !important;
  letter-spacing: 0.02em;
}

/* ---- Mobil / dar ekran (≤768px) — yatay sütunları dikey yığ, taşmayı kes ---- */
@media (max-width: 768px) {
  .block-container {
    padding-left: clamp(0.5rem, 3vw, 1rem) !important;
    padding-right: clamp(0.5rem, 3vw, 1rem) !important;
    max-width: 100% !important;
  }
  [data-testid="stAppViewContainer"] .main [data-testid="stHorizontalBlock"], [data-testid="stAppScrollToBottomContainer"] [data-testid="stHorizontalBlock"] {
    flex-direction: column !important;
    align-items: stretch !important;
    width: 100% !important;
    min-width: 0 !important;
  }
  [data-testid="stAppViewContainer"] .main [data-testid="stHorizontalBlock"] > [data-testid="stColumn"], [data-testid="stAppScrollToBottomContainer"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
  [data-testid="stAppViewContainer"] .main [data-testid="stHorizontalBlock"] > [data-testid="column"], [data-testid="stAppScrollToBottomContainer"] [data-testid="stHorizontalBlock"] > [data-testid="column"] {
    width: 100% !important;
    min-width: 0 !important;
    flex: 1 1 auto !important;
  }
  /* Masthead: yan boşluk sütunlarını gizle, orta blok tam genişlik */
  [data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stHorizontalBlock"],
  [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stHorizontalBlock"] {
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: stretch !important;
  }
  [data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child,
  [data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child,
  [data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child,
  [data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child,
  [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child,
  [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child,
  [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child,
  [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child {
    display: none !important;
  }
  [data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2),
  [data-testid="stVerticalBlock"].st-key-pg_masthead [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2),
  [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2),
  [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) {
    width: 100% !important;
    flex: 1 1 100% !important;
    max-width: 100% !important;
  }
  [data-testid="stVerticalBlock"].st-key-pg_masthead,
  [data-testid="stVerticalBlockBorderWrapper"].st-key-pg_masthead {
    padding: 22px clamp(12px, 4vw, 20px) 16px !important;
    min-height: 0 !important;
  }
  [data-testid="stTabs"] [data-baseweb="tab-list"] {
    flex-wrap: wrap !important;
    gap: 6px !important;
  }
  [data-testid="stTabs"] [data-baseweb="tab"] {
    flex: 1 1 calc(50% - 6px) !important;
    min-height: 44px !important;
    padding: 8px 10px !important;
  }
  [data-testid="stTabs"] [data-baseweb="tab"] p,
  [data-testid="stTabs"] [data-baseweb="tab"] span {
    font-size: 0.8rem !important;
  }
  [data-testid="stAppViewContainer"] .main .stRadio div[role="radiogroup"], [data-testid="stAppScrollToBottomContainer"] .stRadio div[role="radiogroup"] {
    flex-wrap: wrap !important;
    gap: 8px !important;
  }
  [data-testid="stAppViewContainer"] .main .stRadio div[role="radiogroup"] label, [data-testid="stAppScrollToBottomContainer"] .stRadio div[role="radiogroup"] label {
    flex: 1 1 auto !important;
    min-height: 44px !important;
    margin-right: 0 !important;
  }
  .stButton > button {
    min-height: 44px !important;
  }
  .stTextInput input,
  .stNumberInput input,
  textarea {
    font-size: 16px !important;
  }
  [data-testid="stPlotlyChart"],
  div[data-testid="stDataFrame"] {
    max-width: 100% !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch;
  }
  .js-plotly-plot,
  .js-plotly-plot .plotly {
    max-width: 100% !important;
  }
  .metric-strip {
    padding: 12px 14px !important;
  }
  .hero-about-chip-wrap {
    justify-content: center !important;
    margin-top: 6px !important;
  }
  .hero-about-chip {
    height: 34px !important;
    padding: 0 12px !important;
    font-size: 0.78rem !important;
  }
  .about-card {
    padding: 12px 13px !important;
    border-radius: 12px !important;
  }
  .about-card p {
    font-size: 0.89rem !important;
    line-height: 1.55 !important;
  }
  .about-grid {
    grid-template-columns: 1fr !important;
    gap: 8px !important;
  }
  .about-table {
    min-width: 560px !important;
  }
  .about-table thead th,
  .about-table tbody td {
    padding: 9px 10px !important;
  }
  .sr-analysis-page-title {
    font-size: 1.15rem !important;
  }
  .sr-analysis-metric-pill {
    flex: 1 1 calc(50% - 0.5rem) !important;
    max-width: none !important;
  }
  .review-card {
    padding: 12px 14px 14px !important;
  }
  .review-card-head {
    flex-direction: column !important;
    align-items: flex-start !important;
  }
  .review-card-date {
    margin-left: 0 !important;
  }
  /* Inline HTML blokları (analiz özeti) */
  .sr-responsive-row {
    flex-direction: column !important;
    align-items: center !important;
    text-align: center !important;
  }
  .sr-week-dow-strip {
    flex-wrap: wrap !important;
    justify-content: center !important;
  }
  .sr-summary-counts-line {
    flex-direction: column !important;
    align-items: flex-start !important;
    gap: 8px !important;
  }
  /* Yorum sayfalama: anahtar dinamik (ör. main_analiz_review_pager) — sınıf adında _review_pager geçer */
  [data-testid="stVerticalBlock"][class*="_review_pager"] [data-testid="stHorizontalBlock"],
  [data-testid="stVerticalBlockBorderWrapper"][class*="_review_pager"] [data-testid="stHorizontalBlock"] {
    flex-direction: row !important;
    flex-wrap: wrap !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 0.35rem !important;
  }
  [data-testid="stVerticalBlock"][class*="_review_pager"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
  [data-testid="stVerticalBlock"][class*="_review_pager"] [data-testid="stHorizontalBlock"] > [data-testid="column"],
  [data-testid="stVerticalBlockBorderWrapper"][class*="_review_pager"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
  [data-testid="stVerticalBlockBorderWrapper"][class*="_review_pager"] [data-testid="stHorizontalBlock"] > [data-testid="column"] {
    width: auto !important;
    flex: 0 1 auto !important;
    min-width: 0 !important;
  }
}

@media (max-width: 480px) {
  .hero-masthead-brand .hero-title {
    font-size: 1rem !important;
  }
  .hero-brand-logo {
    width: 40px !important;
    height: 40px !important;
  }
}

/*
 * Küçük harf kuralı: arayüzün tamamı (buton, etiket, uyarı vb.).
 * İstisna: mağaza / App Store’dan gelen uygulama adı ve paket satırları, grafikler, kullanıcı giriş alanları, SVG.
 */
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] *,
[data-testid="stSidebar"],
[data-testid="stSidebar"] *,
[data-testid="stDecoration"],
[data-testid="stDecoration"] *,
[data-testid="stToolbar"],
[data-testid="stToolbar"] * {
  text-transform: lowercase !important;
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
[data-testid="stTextArea"] textarea,
textarea,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
[data-testid="stDateInput"] input,
[data-testid="stDateInput"] button {
  text-transform: none !important;
}

.sl-row-title,
.sl-row-id,
.sl-app-banner-title,
.sl-app-banner-meta,
.sl-app-banner-score,
.cmp-selected-summary,
.review-card-app,
.st-key-cmp_review_segment [data-baseweb="segmented-control"],
.st-key-cmp_review_segment [data-baseweb="segmented-control"] button,
[data-testid="stPlotlyChart"],
[data-testid="stPlotlyChart"] *,
[data-testid="stJson"],
[data-testid="stJson"] *,
svg,
svg *,
pre,
code,
kbd,
samp {
  text-transform: none !important;
}
"""
