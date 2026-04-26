# Mağaza yorumu duygu analizi

Mobil uygulama mağazalarından gelen kullanıcı yorumlarını toplayıp, **olumlu / olumsuz / istek–nötr** üçlü sınıflandırma ve özet göstergelerle sunan bir **Streamlit** uygulamasıdır. Amaç; geliştirici veya ürün ekibinin yorumları hızlıca anlaması ve gerektiğinde tablo veya PDF olarak paylaşmasıdır.

**English:** A Streamlit app that pulls mobile store reviews, classifies sentiment into three buckets, and shows a compact dashboard with CSV, Excel, and PDF export. Fast mode runs locally without an API; optional “rich” mode can call a configured LLM provider.

---

## Bu proje ne yapar?

1. **Veri alır** — Google Play ve App Store üzerinden arama veya mağaza bağlantısı; isteğe bağlı yerel veya daha geniş (çok dil–ülke) kapsam; ayrıca tablo dosyası veya panodan yapıştırılan metin (CSV/TSV algısı).
2. **İşler** — **Hızlı:** kural ve sözlük tabanlı analiz, internette ek bir “analiz servisi” gerektirmez. **Zengin:** açıkça seçildiğinde, sizin tanımladığınız API anahtarıyla desteklenen model çağrısı (isteğe bağlı).
3. **Gösterir** — Özet metrikler, dağılımlar, trend ve örnek yorum listesi; iki uygulamayı yan yana karşılaştırma modu.
4. **Dışa verir** — Sonuç tablosu için CSV ve Excel; ekrandaki özet düzenine yakın PDF.

Kapsam, tüketici mağaza yorumlarıdır; başka metin türleri için tasarlanmamıştır.

---

## Kimler kullanır?

Ürün sahibi, geliştirici veya destek ekibi: sürüm notu sonrası tepkiyi, yıldız dağılımını ve yorum metnindeki duyguyu tek ekranda görmek isteyenler.

---

## Diller

Arayüz ve dışa aktarılan metinler **birden çok dilde** sunulabilir (Türkçe varsayılan; diğer diller uygulama içi katalogdan). Dil seçimi oturumda ve isteğe bağlı olarak adres çubuğundaki `?lang=` parametresiyle hatırlanabilir.

---

## Gizlilik ve güvenlik (özet)

- **Depoya API anahtarı veya kişisel veri koymayın.** Örnek dosya `.env.example` yalnızca *hangi değişken isimlerinin* kullanıldığını gösterir; değerleri siz yerelde veya barındırıcı “secrets” alanında doldurursunuz.
- **Hızlı analiz:** Yorum metni uygulamanın çalıştığı ortamda işlenir; zengin mod için tanımlanmamışsa harici modele gönderilmez.
- **Zengin analiz:** Yorum metni, sizin yapılandırdığınız sağlayıcının kurallarına tabi olmak üzere ilgili API’ye gider. Bu modu açmadan önce kendi kurum politikanızı ve sağlayıcı koşullarını gözden geçirmeniz gerekir.
- Mağaza araması ve çekme, herkese açık mağaza sayfalarına benzer isteklerle yapılır; bu README içinde özel token, iç ağ adresi veya kişisel hesap bilgisi paylaşılmaz.

---

## Çalıştırma (yerel)

**Gereksinim:** Python 3.10 veya üzeri önerilir. Bağımlılıklar `requirements.txt` içindedir.

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Zengin analizi deneyecekseniz, proje kökünde `.env` oluşturup `.env.example` ile aynı isimlerde anahtarları tanımlayın; dosyayı **asla** git’e eklemeyin.

Yerel geliştirme için `run_local.sh` varsayılan olarak özel bir port kullanır; dağıtımda Streamlit’in beklediği varsayılan portu kendi yapılandırmanızla hizalayın. Doğrudan:

```bash
streamlit run streamlit_app.py
```

---

## Dağıtım notu

Streamlit Community Cloud gibi ortamlarda uygulama genelde `streamlit_app.py` girişi ve repodaki `requirements.txt` ile çalışır. API anahtarları **yalnızca** barındırıcının gizli alanında (ör. Streamlit Secrets) tutulmalıdır; depoda düz metin olarak bulunmamalıdır.

---

## Sayfa yapısı

- Ana akış: kök URL (`/`).
- Bilgi sayfası: `pages/about.py` üzerinden `/about` (içerik ve dil seçimi uygulama mantığına bağlıdır).

---

## Depo yapısı (özet)

```text
streamlit_app.py          # Giriş noktası, akış ve sayfa bileşimi
pages/about.py            # Hakkında sayfası
run_local.sh              # İsteğe bağlı yerel çalıştırma betiği
requirements.txt
.env.example              # Yalnız isim şablonu; değer içermez
store_review/             # Python paketi
  config/                 # Ayarlar, çok dillilik, tema (CSS)
  core/                   # Analiz motoru ve isteğe bağlı model katmanı
  data/                   # Heuristik verisi, PDF fontu vb.
  fetchers/               # Mağaza, dosya ve yapıştırma kaynakları
  ui/                     # Paneller, dashboard, masthead
  utils/                  # Dışa aktarma, doğrulama, yardımcılar
```

---

## Davranışa dair kısa notlar

- Aynı yorumun tekrarı ve anlamsız satırlar mümkün olduğunca elenir; yeni uygulama veya kaynak seçildiğinde önceki havuz karışmaması için durum sıfırlanır.
- Zengin modda çok büyük havuzlar, kararlılık için parçalara bölünebilir; arayüzde “devam” benzeri adımlarla ilerlenebilir (sürüme bağlıdır).
- Kural tabanlı sözlük `store_review/data/heuristic_lexicon.json` dosyasındadır; değişiklikten sonra uygulamayı yeniden başlatmak gerekir.

---

## English summary

**Purpose:** Ingest Play / App Store reviews (or file / paste), classify into **positive / negative / request–neutral**, show a dashboard, and export **CSV, Excel, and PDF**.

**Modes:** **Fast** — local heuristics, no API keys. **Rich** — optional LLM path when you configure provider keys in `.env` or host secrets.

**Privacy:** Never commit real keys or personal data. Rich mode sends review text to your chosen provider under their terms. Use `.env.example` only as a variable name template.

**Run:** Python 3.10+, `pip install -r requirements.txt`, then `streamlit run streamlit_app.py`. Optional `.env` for rich mode.

**Layout:** Main app in `streamlit_app.py`; package code under `store_review/`.
