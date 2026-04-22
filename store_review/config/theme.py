"""Single place for Streamlit custom CSS (Poppins + light blue + indigo)."""

APP_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif !important;
}

.stApp {
    background: linear-gradient(180deg, #F0F9FF 0%, #EEF2FF 100%);
}

.block-container {
    padding-top: 1.2rem;
    max-width: 960px;
}

div[data-testid="stMetricValue"] {
    font-size: 1.35rem;
    font-weight: 700;
}

.metric-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 16px 18px;
    box-shadow: 8px 8px 16px #D1D9E6, -8px -8px 16px #FFFFFF;
    border: 1px solid rgba(129, 140, 248, 0.25);
}

.fancy-divider {
    height: 2px;
    margin: 18px 0;
    border-radius: 2px;
    background: linear-gradient(90deg, transparent, #818CF8, transparent);
}

.header-title {
    font-size: 1.65rem;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 4px;
}

.header-sub {
    color: #64748B;
    font-size: 0.95rem;
}
"""
