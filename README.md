# Mağaza yorumu duygu analizi (bitirme projesi)

Google Play ve App Store yorumlarını çeker; **üç sınıflı** duygu skoru üretir: Olumlu, Olumsuz, İstek/Görüş.

- **Hızlı analiz:** Eski projedeki **heuristic engine** (sarkazm, pivot/ama-but, manipülasyon tuzağı, kritik bug anahtar kelimeleri, çok dilli listeler, rating override) birebir taşındı.
- **Zengin analiz:** `Gemini`, `Groq`, `OpenAI` sırasıyla denenir; tümü başarısızsa otomatik olarak heuristic’e düşülür.

Google İşletme / pazaryeri kodları **bilerek yok**; yalnızca mağaza yorumu akışı.

**Neden repoda `.env` yok?** API anahtarları asla Git’e eklenmemeli; bu yüzden sadece **`.env.example`** var. Projeyi klonladıktan sonra kendi bilgisayarında `cp .env.example .env` ile `.env` oluşturup anahtarlarını bu dosyaya yazıyorsun (`.gitignore` içinde `.env` zaten yok sayılıyor).

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
    ├── data/
    │   └── heuristic_lexicon.json  # Tüm kelime/liste/pivot/sarkazm verisi (düzenlenebilir)
    ├── core/
    │   ├── heuristic.py      # Rule-based motor (mantık; veri → JSON)
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

- **Heuristic verisi:** `store_review/data/heuristic_lexicon.json` dosyasında toplanır (manipülasyon kalıpları, tam eşleşme kısa metinler, sarkazm, NEG/POS/NEU listeleri, kritik bug, pivot ifadeleri). Bu dosyayı düzenledikten sonra Streamlit sürecini yeniden başlatman yeterli (`_lexicon` önbelleği). Geliştirme sırasında `from store_review.core.heuristic import reload_heuristic_lexicon` ile önbelleği temizleyebilirsin.
- Zengin analizde güvenlik için varsayılan **500 yorum** kotası vardır (`analyzer.analyze_batch` içinde `max_rich_items`).
- Gemini model varsayılanı `gemini-2.0-flash`; sağlayıcı arayüzünden değiştirebilirsiniz (ör. `models/gemini-2.0-flash` gerektiren kurulumlar için).
