# Store review sentiment analysis

---

## English

A Streamlit application for ingesting mobile store reviews, classifying sentiment into three categories (positive, negative, request / neutral opinion), and presenting aggregated results with optional review-level detail. The scope is consumer store review workflows only.

### What it does

- **Ingest:** Google Play and App Store sources, uploaded spreadsheets, pasted plain text, or side‑by‑side comparison of two listed applications over a selectable time window.
- **Analyse:** Two modes—a deterministic rules engine tuned for short, noisy user text, and a deeper model‑assisted path when local configuration allows. The rules path requires no remote services.
- **Deliver:** Dashboard metrics, distribution views, and paginated review cards; exports to CSV, Excel, and PDF (UTF‑8, Turkish glyphs via embedded Noto Sans).

### Requirements

- Python 3.10+ recommended  
- Dependencies listed in `requirements.txt`

### Run locally

For local development, `./run_local.sh` listens on **9517** by default (`STREAMLIT_LOCAL_PORT` overrides). Plain `streamlit run` uses the default port (**8501**), which matches Streamlit Community Cloud health checks—do not commit a repo-wide `[server] port` override if you deploy there.

```bash
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env         # optional: only if you use the deeper analysis path
./run_local.sh               # http://127.0.0.1:9517/
# or: streamlit run streamlit_app.py
```

Repository configuration uses a local environment file that is not versioned. Use the shipped template and keep secrets out of version control.

### Repository layout

```text
├── streamlit_app.py              # Application shell and analysis orchestration
├── run_local.sh                  # Local dev helper (default port 9517)
├── requirements.txt
├── .env.example
└── store_review/                 # Installable package
    ├── config/                   # Runtime settings and presentation layer (CSS)
    ├── core/                     # Heuristics, batch analysis, model integration
    ├── data/                     # Lexicon, bundled PDF font (Noto Sans)
    ├── fetchers/                 # Store connectors, discovery helpers, file ingestion
    ├── ui/                       # Dashboards, store and comparison panels, review UI
    └── utils/                    # Validation and export helpers
```

### Behavioural notes

- Review pools are deduplicated and filtered for non‑review noise before scoring.
- The deeper analysis path applies an upper bound on batch size for stability; the fast path processes the full prepared pool within the same pipeline constraints.
- Lexicon and rule weights live in `store_review/data/heuristic_lexicon.json`; restart the app after edits, or clear the in‑process lexicon cache from code during development.

---

## Türkçe

Mağaza yorumlarını toplayan, duygu sınıflandırmasını üç kategoride (olumlu, olumsuz, istek / nötr görüş) üreten ve özet ile satır düzeyinde sonuçları sunan bir Streamlit uygulaması. Kapsam yalnızca tüketici mağaza yorumu akışıdır.

### Ne sunar

- **Toplama:** Google Play ve App Store, yüklenen tablolar, yapıştırılan metin veya seçilebilir tarih aralığında iki uygulamanın karşılaştırmalı işlenmesi.
- **Analiz:** Gürültülü kısa metinlere göre ayarlanmış kural tabanlı motor ile, yerel yapılandırma uygun olduğunda devreye giren daha derin model destekli yol. Kural yolu uzak servis gerektirmez.
- **Sunum:** Özet göstergeleri, dağılım görünümleri ve sayfalanmış yorum kartları; CSV, Excel ve PDF dışa aktarımı (UTF‑8, Türkçe glifler için gömülü Noto Sans).

### Gereksinimler

- Önerilen: Python 3.10+  
- Bağımlılıklar: `requirements.txt`

### Yerelde çalıştırma

Yerelde `./run_local.sh` varsayılan olarak **9517** portunu kullanır (`STREAMLIT_LOCAL_PORT` ile değişir). Düz `streamlit run` varsayılan **8501**; Streamlit Community Cloud da sağlık kontrolü için bunu bekler—Cloud’a deploy ediyorsanız depoda genel `[server] port` yönlendirmesi tutmayın.

```bash
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env         # isteğe bağlı: yalnızca derin analiz yolunu kullanacaksanız
./run_local.sh               # http://127.0.0.1:9517/
# veya: streamlit run streamlit_app.py
```

Ortam dosyası sürüm kontrolüne alınmaz; şablona kopyalayarak gizli değerleri yalnızca yerelde tutun.

### Dizin yapısı

```text
├── streamlit_app.py              # Uygulama gövdesi ve analiz akışı
├── run_local.sh                  # Yerel çalıştırma (varsayılan port 9517)
├── requirements.txt
├── .env.example
└── store_review/                 # Paket
    ├── config/                   # Ayarlar ve arayüz stilleri (CSS)
    ├── core/                     # Heuristik, toplu analiz, model katmanı
    ├── data/                     # Kural sözlüğü, PDF fontu (Noto Sans)
    ├── fetchers/                 # Mağaza bağlantıları, keşif, dosya yükleme
    ├── ui/                       # Özet panelleri, mağaza ve karşılaştırma, yorumlar
    └── utils/                    # Doğrulama ve dışa aktarım
```

### Davranış notları

- Havuz, tekrarlar giderildikten ve geliştirici yanıtı vb. gürültü elendikten sonra skorlanır.
- Derin analiz yolu toplu işlemde üst sınır uygular; hızlı yol aynı boru hattında hazırlanmış tüm satırları işler.
- `store_review/data/heuristic_lexicon.json` dosyası kural verisini taşır; düzenlemeden sonra süreci yeniden başlatın veya geliştirme sırasında önbelleği kod üzerinden temizleyin.
