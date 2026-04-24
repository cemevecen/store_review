# Store review sentiment analysis

---

## English

A Streamlit application for ingesting mobile store reviews, classifying sentiment into three categories (positive, negative, request / neutral opinion), and presenting aggregated results with review-level detail. The scope is consumer store review workflows only.

### What it does

- **Ingest.** Google Play and App Store sources with platform and regional scope toggles (local vs. global, the latter fanning out across an expanded language/country matrix); spreadsheet upload; pasted text with automatic tabular (TSV/CSV) detection; and a side-by-side comparison pipeline that fetches two listed applications in parallel over a selectable time window.
- **Analyse.** Two execution modes: a deterministic rules engine tuned for short, noisy user text, and a deeper model-assisted path when local configuration allows. Depth controls for the model path are revealed only when the richer mode is selected. The rules path requires no remote services.
- **Present.** Dashboard metrics and distributions that mirror 1:1 between the web view and the PDF export: four-metric pill row, triple sentiment distribution, experience score, directional trend, weekly negative-rate strip, a positive/negative/mixed summary block with persona signals, and a monthly rating distribution stacked bar. Comparison runs render this dashboard side by side, one column per application.
- **Export.** CSV, Excel, and a dashboard-style PDF (UTF-8, Turkish glyphs via embedded Noto Sans). The PDF mirrors the on-screen layout, draws all charts natively with FPDF primitives (no headless browser or extra rendering dependency), and automatically splits the report by application when comparison data is present, appending a per-record review listing coloured by dominant sentiment.

### Internationalisation

The UI is driven by a single string catalogue (`store_review/config/i18n.py`) covering nine locales — Turkish (default), English, Spanish, German, French, Arabic, Simplified Chinese, Russian, Portuguese. All user-facing copy, including the analysis dashboard, comparison screen, rating-distribution chart labels, the `/about` page body, and PDF export, resolves through a single `t()` helper.

Language selection lives in the masthead (flag-only dropdown) and persists via session state and a `?lang=<code>` query parameter so that reloads, direct `/about` links, and navigation between pages retain the active locale. Legacy session values (e.g. Turkish date-range labels from earlier releases) are migrated to language-neutral codes on load.

### Progress and responsiveness

Store scans and review-pool fetches emit incremental progress with monotonic guarantees — the bar cannot move backwards. Both Google Play and App Store fetchers emit early-phase progress during the initial, non-fanned-out request so the UI does not stall at 0%. The comparison panel applies the same floor-capped synthetic ramp while concurrent, per-app channels fill in actual counts.

Layouts are mobile-first; dashboards, the split comparison view, and the about page all adapt down to narrow viewports and up to wide desktops without fixed breakpoints leaking into the analysis surface.

### URL surface

- `/` — main analysis entry point.
- `/about` — dedicated about page (developer credit, system description, styled information blocks). Language selection is honoured via `?lang=<code>`.

### Requirements

- Python 3.10+ recommended
- Dependencies listed in `requirements.txt`

### Run locally

For local development, `./run_local.sh` listens on **9517** by default (`STREAMLIT_LOCAL_PORT` overrides). Plain `streamlit run` uses the default port (**8501**), which matches Streamlit Community Cloud health checks — do not commit a repo-wide `[server] port` override if you deploy there.

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
├── pages/
│   └── about.py                  # Dedicated about page (i18n-aware)
├── run_local.sh                  # Local dev helper (default port 9517)
├── requirements.txt
├── .env.example
└── store_review/                 # Installable package
    ├── config/
    │   ├── i18n.py               # 9-locale string catalogue + query-param sync
    │   ├── settings.py
    │   └── theme.py              # CSS system, responsive rules, brand palette
    ├── core/                     # Heuristics, batch analysis, model integration
    ├── data/                     # Lexicon, bundled PDF font (Noto Sans)
    ├── fetchers/
    │   ├── app_discovery.py      # Search and slug resolution helpers
    │   ├── app_store.py          # App Store connector with progress + scope
    │   ├── google_play.py        # Google Play connector with progress + scope
    │   ├── file_loader.py        # Spreadsheet ingestion
    │   └── paste_loader.py       # Clipboard parser (auto-detects TSV/CSV)
    ├── ui/
    │   ├── analysis_results_dashboard.py  # Reusable dashboard (compact/split)
    │   ├── compare_panel.py      # Parallel fetch + side-by-side rendering
    │   ├── masthead.py           # Header / brand, data-source pills, flag language + About
    │   ├── review_cards.py       # 5 + expand pagination, LLM/heuristic aware
    │   └── store_link_panel.py   # Single-app search and fetch panel
    └── utils/
        ├── pdf_export.py         # Dashboard-mirroring PDF (native FPDF charts)
        └── ...                   # Validation and additional export helpers
```

### Behavioural notes

- Review pools are deduplicated and filtered for non-review noise before scoring. Previous search state is reset when a new application is selected, so pools never cross-contaminate.
- The deeper analysis path applies an upper bound on batch size for stability; the fast path processes the full prepared pool within the same pipeline constraints.
- Lexicon and rule weights live in `store_review/data/heuristic_lexicon.json`; restart the app after edits, or clear the in-process lexicon cache from code during development.
- The analysis dashboard is a single reusable component. It accepts `compact`, `key_suffix`, and `section_title` parameters so comparison runs can render two instances side by side without widget key collisions.
- The PDF export is self-contained: charts are drawn with FPDF primitives, no browser or Kaleido dependency. Compare mode is detected from the presence of a multi-valued `Uygulama` column in the analysis rows.

---

## Türkçe

Mağaza yorumlarını toplayan, duygu sınıflandırmasını üç kategoride (olumlu, olumsuz, istek / nötr görüş) üreten ve özet ile satır düzeyinde sonuçları sunan bir Streamlit uygulaması. Kapsam yalnızca tüketici mağaza yorumu akışıdır.

### Ne sunar

- **Toplama.** Platform ve bölge seçicileriyle (yerel / global; global genişletilmiş dil-ülke matrisi üzerinden fan-out) Google Play ve App Store; tablo yükleme; otomatik tablo algılamalı (TSV/CSV) yapıştırma; ve seçili tarih aralığında iki uygulamayı paralel getiren karşılaştırma hattı.
- **Analiz.** İki mod: gürültülü kısa metinlere göre ayarlanmış kural tabanlı motor ve yerel yapılandırma uygun olduğunda devreye giren daha derin model destekli yol. Derinlik kontrolleri yalnızca zengin mod seçildiğinde görünür; kural yolu uzak servis gerektirmez.
- **Sunum.** Web arayüzü ve PDF dışa aktarımı bire bir aynı dashboard'u sunar: dörtlü metrik pill satırı, üçlü duygu dağılımı, genel deneyim skoru, yönlü trend, haftalık negatif-oran şeridi, olumlu/olumsuz/karma özet bloğu (persona sinyalleriyle) ve aylık puan dağılımı stacked bar grafiği. Karşılaştırma akışında iki uygulama yan yana, her biri kendi sütununda işlenir.
- **Dışa aktarım.** CSV, Excel ve dashboard tarzı PDF (UTF-8, Türkçe glifler için gömülü Noto Sans). PDF, ekrandaki düzeni birebir yansıtır, tüm grafikleri FPDF primitifleriyle (ek render motoru gerekmez) yerel olarak çizer, karşılaştırma verisi varsa raporu uygulamalara göre bölüp her kayıt için baskın duyguya göre renklendirilmiş yorum listesi ekler.

### Çok dillilik

Arayüz tek bir metin kataloğundan (`store_review/config/i18n.py`) beslenir; dokuz dil kapsanır — Türkçe (varsayılan), İngilizce, İspanyolca, Almanca, Fransızca, Arapça, Basitleştirilmiş Çince, Rusça, Portekizce. Analiz dashboard'u, karşılaştırma ekranı, puan dağılımı grafiği etiketleri, `/about` sayfası ve PDF dışa aktarımı dahil tüm metinler tek bir `t()` yardımcısı üzerinden çözülür.

Dil seçimi masthead'deki (yalnızca bayrak) dropdown'da yaşar; hem oturum state'i hem de `?lang=<code>` URL parametresi ile kalıcı hale getirilir. Bu sayede yenileme, `/about` bağlantısı veya sayfalar arası gezinti aktif dili korur. Eski oturumlarda kalan değerler (ör. önceki sürümlerden gelen Türkçe tarih etiketleri) yüklemede dil-nötr kodlara migrate edilir.

### İlerleme ve akıcılık

Mağaza taraması ve yorum havuzu çekimi, geri gitmesi engellenmiş (monotonik) bir ilerleme barı ile canlı sinyal gönderir. Google Play ve App Store fetcher'ları, fan-out'tan önceki ilk istek sırasında erken faz ilerlemesi yayar; bar %0'da asılı kalmaz. Karşılaştırma paneli aynı zemin-kaplamalı sentetik rampayı uygular, eş zamanlı uygulama kanalları gerçek sayılarla üzerini yazar.

Yerleşim mobile-first'tür; dashboard'lar, bölünmüş karşılaştırma görünümü ve about sayfası dar ekranlardan geniş masaüstü genişliklerine kadar analiz yüzeyine sızmayan breakpoint'lerle uyum sağlar.

### URL yüzeyi

- `/` — ana analiz giriş noktası.
- `/about` — ayrı about sayfası (geliştirici, sistem açıklaması, biçimlendirilmiş bilgi blokları). Dil seçimi `?lang=<code>` ile taşınır.

### Gereksinimler

- Önerilen: Python 3.10+
- Bağımlılıklar: `requirements.txt`

### Yerelde çalıştırma

Yerelde `./run_local.sh` varsayılan olarak **9517** portunu kullanır (`STREAMLIT_LOCAL_PORT` ile değişir). Düz `streamlit run` varsayılan **8501**; Streamlit Community Cloud da sağlık kontrolü için bunu bekler — Cloud'a deploy ediyorsanız depoda genel `[server] port` yönlendirmesi tutmayın.

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
├── pages/
│   └── about.py                  # /about sayfası (i18n farkında)
├── run_local.sh                  # Yerel çalıştırma (varsayılan port 9517)
├── requirements.txt
├── .env.example
└── store_review/                 # Paket
    ├── config/
    │   ├── i18n.py               # 9 dillik metin kataloğu + query-param senkronu
    │   ├── settings.py
    │   └── theme.py              # CSS sistemi, responsive kurallar, marka paleti
    ├── core/                     # Heuristik, toplu analiz, model katmanı
    ├── data/                     # Kural sözlüğü, PDF fontu (Noto Sans)
    ├── fetchers/
    │   ├── app_discovery.py      # Arama ve slug çözümü
    │   ├── app_store.py          # App Store bağlayıcısı (ilerleme + kapsam)
    │   ├── google_play.py        # Google Play bağlayıcısı (ilerleme + kapsam)
    │   ├── file_loader.py        # Tablo yükleme
    │   └── paste_loader.py       # Yapıştırılan metin ayrıştırıcısı (TSV/CSV)
    ├── ui/
    │   ├── analysis_results_dashboard.py  # Tek/split modda yeniden kullanılabilir dashboard
    │   ├── compare_panel.py      # Paralel çekim + yan yana sunum
    │   ├── masthead.py           # Header / marka, kaynak pill'leri, bayrak dil + Hakkında
    │   ├── review_cards.py       # 5 + genişlet sayfalama, LLM/heuristik uyumlu
    │   └── store_link_panel.py   # Tek uygulama arama ve çekim paneli
    └── utils/
        ├── pdf_export.py         # Dashboard'u birebir yansıtan PDF (yerel FPDF grafikler)
        └── ...                   # Doğrulama ve diğer dışa aktarım yardımcıları
```

### Davranış notları

- Havuz, tekrarlar giderildikten ve geliştirici yanıtı vb. gürültü elendikten sonra skorlanır. Yeni bir uygulama seçildiğinde önceki arama durumu sıfırlanır; havuzlar birbirine karışmaz.
- Derin analiz yolu toplu işlemde üst sınır uygular; hızlı yol aynı boru hattında hazırlanmış tüm satırları işler.
- `store_review/data/heuristic_lexicon.json` dosyası kural verisini taşır; düzenlemeden sonra süreci yeniden başlatın veya geliştirme sırasında önbelleği kod üzerinden temizleyin.
- Analiz dashboard'u tek bir yeniden kullanılabilir bileşendir. `compact`, `key_suffix` ve `section_title` parametreleriyle karşılaştırma modunda iki kopyası widget anahtar çakışması yaşamadan yan yana render edilir.
- PDF dışa aktarımı kendi içinde tamamdır: grafikler FPDF primitifleriyle çizilir, tarayıcı veya Kaleido bağımlılığı yoktur. Karşılaştırma modu, analiz satırlarındaki `Uygulama` kolonunun çok değerli olmasından otomatik algılanır.
