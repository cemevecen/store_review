# Mağaza yorumu duygu analizi (bitirme projesi)

Google Play ve App Store yorumlarını çeker; **üç sınıflı** duygu skoru üretir: Olumlu, Olumsuz, İstek/Görüş.

- **Hızlı analiz:** Eski projedeki **heuristic engine** (sarkazm, pivot/ama-but, manipülasyon tuzağı, kritik bug anahtar kelimeleri, çok dilli listeler, rating override) birebir taşındı.
- **Zengin analiz:** `Gemini`, `Groq`, `OpenAI` sırasıyla denenir; tümü başarısızsa otomatik olarak heuristic’e düşülür.

Google İşletme / pazaryeri kodları **bilerek yok**; yalnızca mağaza yorumu akışı.

## Kurulum

```bash
cd "/Users/cemevecen/Desktop/store review"
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # anahtarları düzenle
streamlit run streamlit_app.py
```

## Mimari şema

```text
store review/
├── streamlit_app.py          # Sekmeler, analiz tetikleme, grafik / tablo
├── requirements.txt
├── .env.example
├── README.md
└── store_review/             # Python paketi
    ├── config/
    │   ├── settings.py       # Ortam değişkenlerinden API anahtarları
    │   └── theme.py          # Tek yerde CSS
    ├── core/
    │   ├── heuristic.py      # Rule-based motor (legacy v3.0)
    │   ├── prompts.py        # LLM prompt + JSON ayrıştırma
    │   ├── ai_providers.py # Gemini / Groq / OpenAI + fallback zinciri
    │   └── analyzer.py       # Paralel toplu analiz + dedup
    ├── fetchers/
    │   ├── google_play.py    # Çok kanallı paralel Play çekimi
    │   ├── app_store.py      # 40 ülke RSS paralel
    │   └── file_loader.py    # CSV/XLSX → normalize edilmiş yorum listesi
    └── utils/
        ├── validators.py     # is_valid_comment (geliştirici cevabı vb. filtre)
        └── exporters.py      # CSV / Excel bayt çıktısı
```

## Akış

1. **Veri:** Play package / URL, App Store id / URL, dosya veya yapıştırılan metin.
2. **Havuz:** `dedupe_reviews` + `is_valid_comment` ile temizlenmiş liste.
3. **Analiz:** `analyze_batch` → Hızlı: `heuristic_analysis`; Zengin: `RichAnalyzer` (API zinciri + gerekirse heuristic).

## Notlar

- Zengin analizde güvenlik için varsayılan **500 yorum** kotası vardır (`analyzer.analyze_batch` içinde `max_rich_items`).
- Gemini model varsayılanı `gemini-2.0-flash`; sağlayıcı arayüzünden değiştirebilirsiniz (ör. `models/gemini-2.0-flash` gerektiren kurulumlar için).
