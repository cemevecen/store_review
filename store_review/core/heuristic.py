"""Heuristic sentiment engine for store reviews (legacy v3.0 logic preserved)."""

def heuristic_analysis(text, rating=None):
    """
    Heuristic Engine v3.0
    - 1750+ Instagram/App Store yorumuyla eğitildi
    - TR / EN / AR / RU / FR / DE / ES / NL / RO / BG destekli
    - Rating-aware: puan ile içerik çelişirse içeriği önce denetler
    - Sarkasm, pivot (ama/but), "öne çıksın" tuzağı tespiti
    """
    t = str(text).lower().strip()
    if not t or len(t) < 2:
        return {"olumlu": 0.33, "olumsuz": 0.34, "istek_gorus": 0.33, "method": "Heuristic+"}

    # ── 1. PUAN BAZLI HIZLI SINYALLER ────────────────────────────────────────
    # Rating parametresi varsa güçlü sinyal olarak kullan
    _rating = None
    if rating is not None:
        try:
            _rating = int(str(rating).strip().split('.')[0])
        except:
            pass

    # ── 2. PUAN MANİPÜLASYON TUZAĞI ("öne çıksın diye 5 yıldız") ────────────
    manipulation_patterns = [
        "öne çıksın diye", "üste çıksın diye", "en üste çıksın",
        "görülsün diye yüksek", "fark edilsin diye", "dikkat çeksin diye",
        "yüksek puan verdim ama", "5 yıldız verdim ama", "beş yıldız verdim ama",
        "puan verdim ama aslında", "5 puan ama",
    ]
    if any(p in t for p in manipulation_patterns):
        return {"olumlu": 0.05, "olumsuz": 0.88, "istek_gorus": 0.07, "method": "Heuristic+"}

    # ── 3. YILDIZ İFADESİ METİN İÇİNDE ──────────────────────────────────────
    if any(x in t for x in ["1 yıldız", "bir yıldız", "1 stern", "1 star", "1 étoile", "1/5", "one star"]):
        return {"olumlu": 0.03, "olumsuz": 0.94, "istek_gorus": 0.03, "method": "Heuristic+"}
    if any(x in t for x in ["5 yıldız", "beş yıldız", "5 stars", "5 étoiles", "5/5", "five stars", "5 stern"]):
        return {"olumlu": 0.94, "olumsuz": 0.03, "istek_gorus": 0.03, "method": "Heuristic+"}

    # ── 4. TAM EŞLEŞMELİ KISA METİNLER (exact match) ─────────────────────────
    EXACT_POS = {
        # TR
        "harika", "mükemmel", "süper", "güzel", "iyi", "başarılı", "şahane",
        "teşekkürler", "sağolun", "bayıldım", "muhteşem", "muq", "müq", "çok iyi",
        "çok güzel", "on numara", "bravo", "aferin", "efsane", "müthiş",
        # EN
        "best", "great", "amazing", "perfect", "love", "excellent", "wonderful",
        "fantastic", "awesome", "brilliant", "superb", "outstanding", "good",
        "nice", "top", "cool", "super",
        # AR
        "ممتاز", "احبه", "رائع", "جميل", "افضل", "الافضل", "تمام", "مبدع",
        # RU
        "отлично", "супер", "топ", "хорошо", "нравится", "класс",
        "великолепно", "замечательно", "прекрасно",
        # FR
        "génial", "magnifique", "parfait", "incroyable", "bravo",
        "top", "bien", "excellent",
        # DE
        "toll", "super", "ausgezeichnet", "wunderbar", "prima", "klasse", "perfekt",
        # ES/PT
        "excelente", "genial", "fantástico", "ótimo", "maravilhoso", "buenísimo",
        # PL/RO/Other
        "świetne", "niezawodny", "foarte bună", "super",
    }
    if t in EXACT_POS:
        return {"olumlu": 0.95, "olumsuz": 0.02, "istek_gorus": 0.03, "method": "Heuristic+"}

    EXACT_NEG = {
        # TR
        "çöp", "berbat", "rezalet", "rezil", "saçma", "iğrenç", "kötü",
        "berbatsin", "berbattın", "bk gibi", "çöp gibi",
        # EN
        "trash", "scam", "worst", "terrible", "horrible", "awful",
        "disgusting", "garbage", "pathetic", "useless", "rubbish",
        "bad", "broken",
        # AR
        "سيء", "أسوأ", "مروع", "فاشل",
        # RU
        "ужасно", "отстой", "мусор", "кошмар",
        # DE
        "schrecklich", "schlecht", "furchtbar", "mist",
        # FR
        "nul", "catastrophique", "horrible",
        # TR kısa
        "kötü", "çöp", "saçma",
    }
    if t in EXACT_NEG:
        return {"olumlu": 0.03, "olumsuz": 0.94, "istek_gorus": 0.03, "method": "Heuristic+"}

    # ── 5. SARKASM / İRONİ TESPİTİ ───────────────────────────────────────────
    SARKASM = [
        "ne indirin ne de indirin", "ne indirin nede",
        "aferin size", "aferin sizlere",
        "tebrikler size", "tebrikler size gerçekten",
        "çok faydalı olacaktır",  # "böyle yapmaya devam edin, meta'ya çok faydalı olacaktır"
        "böyle yapmaya devam edin",
        "sizi bildiği gibi yapsın", "allah belanızı versin", "başınıza taş yağsın",
        "bravo size", "helal olsun yine",  # "helal olsun yine çöktü" → negatif
        "indirdim ve bağımlı", "indirdim ve bir otist",
        "indirmeden önce çok normaldim",
        "this app destroyed",
        "destroyed all my happiness",
        "fix your appp",
        "fire every single one",
        "shame on this company",
        "get rid of meta",
        "go out see a band",
        "stay off socials",
        "best app for spending",
        "best app for anyone who is interested in spending",
        "roblox is ruined",
        "you killed a",
        "kids are dying cuz of",
        "please destroy the game",
        "before you destroy the game",
        "i rated this 5 stars so people can see",
        "i only put 5 stars so",
        "i give 5 stars so people",
        "i put 5 stars because i want people to see",
        "i'm going to roblox headquarters",
        "get ur age verified it's not that hard",
        "ceo needs to be fired",
        "quit ya jobs",
        "hope whoever made these updates get",
        "this game should be studied",
        "kötü gazeteciler gibi davranmaya",
        "çok ucuz bu",
        "hem ücretli üyelik yapıyorsunuz hem programla ilgilenmiyorsunuz",
        "ne yapıyorsunuz bu ara",
    ]
    sarkasm_hit = any(p in t for p in SARKASM)

    # ── 6. KEYWORD LİSTELERİ ─────────────────────────────────────────────────

    NEG_WORDS = [
        # TR — Hesap sorunları (EN ÇOK şikayet)
        "askıya", "askıya alındı", "askıya alınmış", "askıya alınıyor",
        "hesabım kapatıldı", "hesabımı kapattılar", "hesaplarım kapandı",
        "hesabım kapandı", "kapatılmış", "kapatıldı",
        "itiraz", "itiraz ettim", "kayboldu", "silindi",
        "yok oldu", "nereye gitti", "kaybolmuş", "bulamıyorum",
        "giriş yapamıyorum", "giremiyorum", "giriş yapamıyorum",
        "hesabıma giremiyorum", "hesabıma girilmiyor",
        "şifre yanlış", "şifremi doğru girdiğim halde",
        "şifre doğru ama yanlış", "şifre doğru olmasına rağmen",
        "durduruldu", "askıda",
        "ip ban", "cihaz ban", "cihaz banı", "ip banı",
        "yeni hesap açınca da kapanıyor", "açtığım her hesap",
        "her hesap kapatılıyor", "her hesabım kapanıyor",
        "20 hesap", "10 hesap", "5 hesap",  # "10 hesap açtım hepsi kapandı"

        # TR — Uygulama sorunları
        "donuyor", "kasıyor", "çöküyor", "çöktü", "kapanıyor",
        "çalışmıyor", "yavaş", "hata veriyor", "hata var",
        "bozuk", "bozuldu", "berbat", "kötü", "rezil", "rezalet",
        "sorun", "problem", "çöp", "saçma", "yaramaz", "iğrenç",
        "durduruldu", "sildim", "siliyorum", "kaldırdım", "kaldırıyorum",
        "yüklenmiyor", "açılmıyor", "gözükmüyor", "görünmüyor",
        "boş ekran", "lag", "atıyor", "uygulama atıyor",
        "uygulama çöküyor", "uygulama donuyor",

        # TR — Finans/kur uygulaması özel
        "sıfırlandı", "hepsi sıfırlandı", "veriler sıfırlandı",
        "varlık sıfır", "bilgiler kayboldu", "veriler kayboldu",
        "alarm kuramaz", "alarm kurulmuyor", "alarm çalışmıyor",
        "alarm gelmiyor", "bildirim gelmiyor", "bildirimler gelmiyor",
        "bildirime tıklıyorum açılmıyor",
        "favori listem görünmüyor", "favoriler görünmez",
        "favoriler kayboldu", "favori görünmez oldu",
        "arka planda güncelleme yapmıyor",
        "arka planda çalışmıyor",
        "fiyatlar güncellenmiyor", "kurlar güncellenmiyor",
        "kurlar donuyor", "rakamlar donuyor",
        "yetkiniz yok", "yetki hatası",
        "cüzdan çalışmıyor", "cüzdana ekleyemiyor",
        "cüzdanda hata", "cüzdan bölümü çalışmıyor",
        "düzenle butonu çalışmıyor", "düzenle çalışmıyor",
        "hopörlerden ses", "hoparlörden ses",
        "hantallık var", "çok hantal",
        "açılmıyorki", "giremiyor",
        "erişilebilirlik yok", "voiceover çalışmıyor",
        "görme engelli",
        "premium aldık ama", "para ödedik ama",
        "ücretli üyelik ama", "paralı uygulama oldu",
        "hem ücretli hem",
        "sinir bozucu olmuş", "her seferinde sormak",
        "virgül sonrası kaldırılmış",
        "tablette destek yok", "tablet desteği yok",


        # TR — Veri kaybı / Silme sorunları
        "silinmiyor", "silindi", "siliniyor", "silindiler",
        "silinemedi", "silinemiyorum", "silinemedi",
        "kayboldu", "kayıp", "kayboldular",
        "veri silme sorunu", "veri silemiyorum",
        "alarmlar silinmiyor", "rehber kayıtları silinmiyor",
        "nedir", "hatalar silinmiyor", "hata mesajları silinmiyor",

        # TR — Donma/Freeze Sorunları
        "donuyor", "donmuş", "donmaya başladı", "çok sık donuyor",
        "kasıyor", "kastı", "kastığı", "kasıp",

        # TR — Açılmama/Giriş Sorunları  
        "açılmıyor", "açılamıyor", "açılmaz", "hiç açılmıyor",
        "giremiyorum", "giriş yapamıyorum", "giriş yapılamıyor",

        # TR — Çalışmama Sorunları
        "kaydedilemedi", "kaydı yapılamıyor", "kaydı yapılamıyor",
        "güncellenmiyor", "güncellemediği", "güncellemediğini",
        "yüklenmiyor", "yüklenme hatası",

        # TR — Özellik Kaybı/Bozulma
        "seçeneği kayboldu", "opsiyonu kayboldu", "veriler gidiyor",
        "veriler kayıp", "hepsi silindi", "hepsi kayboldu",
        "kırık", "bozuk", "tabletinde destek yok",

        # TR — Finans uygulaması istekleri
        "yatırım fonu ekle", "fonlar eklensin", "fonları da ekle",
        "halka arz ekle", "halka arz sayfası",
        "akaryakıt fiyatları ekle", "akaryakıt da eklensin",
        "dünya borsaları ekle", "borsa ekle",
        "widget güncellensin", "anlık güncelleme butonu",
        "yorum yapma özelliği", "yorum özelliği getirilmeli",
        "takvimi elle yaz", "elle tarih giriş",
        "banka eklenmesi", "daha fazla banka",
        "tarih aralığı seçimi", "üç aylık seçenek",
        "erişilebilirlik ekle", "ekran okuyucu entegre",
        "bildirim içeriği daha açık",

        # TR — Chat/mesaj sorunları
        "mesaj gitmiyor", "mesajlar gitmiyor", "mesaj gelmiyor",
        "mesajlara giremiyorum", "dm sorunu", "mesaj yüklenmiyor",
        "sohbet açılmıyor", "mesaj düşmüyor",

        # TR — Reklam
        "reklam çok", "aşırı reklam", "her yerden reklam",
        "full reklam", "çok reklam", "reklam dolu",
        "her reels reklam", "2 reels 1 reklam", "1 reklam 1 reels",
        "34 reels 19 reklam",  # spesifik sayım
        "reklam sayfasına atıyor", "reklam geçilmiyor",
        "reklam donuyor",

        # TR — İçerik/feed sorunları
        "eski gönderiler", "4 günlük", "günler önceki",
        "feed yenilenmiyor", "akış yenilenmiyor",
        "takip etmediğim", "alakasız videolar", "alakasız içerik",
        "yabancı dil videoları",

        # TR — Müzik
        "müzik yok", "müzik çalışmıyor", "müzik kaldırıldı",
        "ses yok", "ses gitmiyor", "ses çalışmıyor",
        "audio çalışmıyor",

        # TR — Tema/filtre
        "tema gitti", "temalar gitti", "temalar kaldırıldı", "tema yok",
        "filtreler gitti", "eski filtreler", "efektler kaldırıldı",

        # TR — Fotoğraf/galeri
        "fotoğraflar karışık", "galeri karışık", "fotoğraf seçemiyorum",
        "fotoğraf açılmıyor", "foto açılamadı", "resim yüklenmiyor",
        "fotoğraf yüklenmiyor", "profil fotoğrafı değişmiyor",
        "profil resmi yüklenmiyor",

        # TR — Arşiv/anı
        "anılar yok", "arşiv yok", "geçmiş hikayeler gözükmüyor",
        "eski hikayeler yok", "anılar çıkmıyor", "anım çıkmıyor",

        # TR — Kayıtlar
        "kaydedilenlerden silince başa dönüyor",
        "kaydedilenler başa atıyor", "kaydettiklerim karışık",

        # TR — Güncelleme
        "güncelleme kötü", "güncelleme bozdu", "yeni güncelleme kötü",
        "son güncelleme berbat", "güncelleme sonrası bozuldu",

        # TR — Reel/video
        "reels açılmıyor", "video açılmıyor", "reels izleyemiyorum",
        "video yüklenmiyor", "siyah ekran", "kara ekran",
        "videolar görünmüyor", "reels çalışmıyor",

        # TR — Genel kötü deneyim
        "mahvoldu", "batık", "mağdur", "mağdurum",
        "yeter artık", "bıktım artık", "artık bıktım",
        "gına geldi", "sinir bozucu", "can sıkıcı",
        "berbatlaştı", "kötüleşti", "giderek kötü",
        "eskiden iyiydi", "eskisi daha iyiydi",
        "eski haline getirin", "eski haline dönün",
        "eski instagram", "eski versiyonu",

        # TR — Safariden giriyor ama uygulamadan girmiyor
        "safariden giriyor ama uygulamadan",
        "google chrome giriyor ama uygulama",
        "telefonumdan giremiyorum",
        "kendi telefonumdan giremiyorum",
        "başka cihazdan giriyor ama",

        # TR — Özellik gelmiyor
        "bana gelmiyor", "hesabıma gelmiyor",
        "güncelleme gelmiyor", "özellik gelmiyor",
        "herkeste var bende yok",

        # TR — Moderasyon
        "haksız", "haksız yere", "sebepsiz", "sebepsiz yere",
        "hiçbir şey yapmadığım halde", "suçum yok ama",
        "topluluk kuralları ihlali yok ama",

        # EN — Account/ban
        "suspended", "suspension", "banned", "ban", "disabled",
        "account disabled", "account suspended", "account banned",
        "no reason", "false ban", "wrongly banned",
        "cant login", "can't login", "login loop", "login issue",
        "permanently banned", "permanently disabled", "permanently suspended",
        "lost my account", "lost access",
        "falsely banned for cse", "cse ban", "false cse",
        "wrongfully banned cse", "accused of cse",

        # EN — App issues
        "crashing", "crashes", "keeps crashing", "crash",
        "freezing", "freeze", "lag", "lagging", "laggy",
        "not working", "doesn't work", "won't work", "stopped working",
        "bug", "glitch", "glitching", "broken",
        "terrible", "horrible", "awful", "disgusting", "garbage",
        "worst app", "worst update", "hate this", "ruined",

        # EN — Ads
        "too many ads", "ads everywhere", "all ads", "ad every",
        "non stop ads", "constant ads", "flooded with ads",
        "ad breaks", "mid video ads",

        # EN — Photos out of order
        "photos out of order", "pictures out of order",
        "not in chronological order", "photos jumbled",
        "photos all mixed up", "gallery mixed up",

        # EN — Login via browser not app
        "can login on safari but not app",
        "works on browser not app",
        "can log in on computer but not app",

        # EN — No human support
        "no human support", "no human review", "no real person",
        "can't reach anyone", "no way to contact",
        "zero support", "no support contact",
        "appeal ignored", "appeal rejected instantly",

        # EN — Music
        "no music", "music not working", "music removed", "music banned",
        "audio unavailable", "no audio",

        # EN — Themes
        "themes gone", "themes removed", "themes disappeared",

        # EN — Messages
        "messages not loading", "cant send messages",
        "messages not working", "messages not sending",
        "messages failed", "dm not working",

        # EN — General
        "scam", "fraud",
        "fix this", "fix your app", "fix it",
        "something went wrong",
        "error", "not loading",

        # Game/Platform — Chat & moderation
        "bring chat back", "chat back", "chat is gone",
        "chat removed", "no chat", "cant chat", "can't chat",
        "chat was removed", "remove chat", "took the chat",
        "taking away chat", "deleted chat", "chat gone",
        "chat is horrible", "silent servers",

        # Game/Platform — Age verification
        "age verification", "face verification", "face check",
        "face scan", "age check", "age group wrong",
        "ai age check", "persona ai", "scanning faces",
        "scan my face", "harvesting faces", "data leak",
        "identity leak", "verification broken",
        "age check broken", "ai gets age wrong",
        "thinks i'm", "says i am", "placed me in wrong",

        # Game/Platform — Bans & moderation
        "got banned for saying", "banned for saying hi",
        "banned for no reason", "chat suspended",
        "moderation is horrible", "bad moderation",
        "report them nothing happens", "hackers don't get banned",
        "toxic players don't get banned",
        "got my account deleted", "account got deleted",
        "voice chat taken", "voice chat removed", "vc removed",
        "vc disappeared", "vc gone",

        # Game/Platform — Content & updates
        "ruined roblox", "roblox is ruined", "ruining roblox",
        "roblox is dying", "platform is dying",
        "classic faces removed", "removing classic faces",
        "classic faces gone", "deleted faces",
        "brainrot games", "all brainrot", "only brainrot",
        "slop games", "slop farm", "ai generated games",
        "boring repeats", "money hungry",
        "pay to upload", "cost robux to upload",
        "premium just to upload", "need premium to",
        "expensive now", "getting expensive",

        # Game/Platform — Technical
        "kicks me out", "kicking me out", "kicked me out",
        "kick me from", "keeps kicking", "disconnected",
        "keeps disconnecting", "constant disconnects",
        "laggy server", "server lag",

        # Game/Platform — Safety
        "predators", "preds", "pdfs",
        "inappropriate games", "dating game",
        "not safe for kids", "unsafe for kids",
        "grooming", "child predator",
        "ruining itself", "kill itself",
        "investors not players",

        # Game/Platform — Robux/scam
        "robux scam", "robux stolen", "robux vanished",
        "lost robux", "robux missing", "robux disappeared",
        "didn't receive robux", "never got robux",
        "scam", "daylight robbery", "absolute robbery",
        "items removed without refund", "no refund",
        "removed without refund",
        "youtubers are quitting", "players are leaving",
        "gonna quit", "may quit", "undownloaded", "un-downloaded",
        "deleted the app", "deleting this app",

        # EN — Ek
        "falsely banned", "falsely suspended",

        # DE — Ek
        "stocken", "stockt", "ruckelt",
        "non stop grundlos",

        # TR — Ek
        "düzeltin artık", "düzeltilmesi lazım",
        "hikayeler gözükmüyor", "hikayeler yüklenmiyor",
        "sohbetteki eski", "fotoğraflar yüklenmiyor",
        "arşivimde yok", "eski hikayelerim yok",
        "kapanıyor hesabım", "yeniden kapandı",
        "hesabım askıya", "durduk yere",
        "rezil bir uygulama",
        "kesinlikle yüklemeyin",
        "giderek kötüleşti",
        "vpn çalışmıyor", "vpn ile çalışmıyor",
        "indirilemiyor",

        # RU — Ek
        "постоянно вылетает", "вылетает приложение",
        "не работает с vpn", "vpn не работает",
        "удалили музыку", "убрали музыку",
        "верните музыку",

        # FR — Ek
        "ban sans raison", "banni sans raison",
        "compte suspendu sans raison",
        "ergonomie catastrophique",

        # IT — Ek
        "pesantissima", "instabile", "pessima qualità",
        "crash", "si blocca", "non funciona più",

        # RU
        "заблокировали", "блокировка", "аккаунт заблокирован",
        "бан", "забанили", "не работает",
        "удалили", "пропало", "исчезло", "убрали",
        "не грузится", "не загружается", "глючит", "виснет",
        "зависает", "не открывается", "ошибка",
        "ужасно", "отвратительно", "верните",
        "перестало работать", "сломали", "испортили",
        "не приходят сообщения", "темы пропали",
        "музыка не работает", "музыку убрали",
        "фото не по порядку", "галерея перемешана",
        "не могу загрузить фото",

        # FR
        "suspendu", "banni", "compte supprimé", "compte suspendu",
        "ne fonctionne plus", "ne fonctionne pas",
        "plante", "bloqué", "erreur", "problème", "nul",
        "horrible", "catastrophique", "trop de pubs",
        "thèmes disparus", "messages ne chargent pas",
        "photos mélangées", "photos dans le désordre",

        # DE
        "gesperrt", "konto gesperrt", "account gesperrt",
        "funktioniert nicht", "abstürzt", "fehler",
        "schlecht", "schrecklich", "zu viel werbung",
        "themen weg", "nachrichten laden nicht",
        "fotos durcheinander", "bilder durcheinander",
        "grundlos gesperrt",

        # AR
        "حظر", "محظور", "تم حظر", "تعطيل", "معطل",
        "لا يعمل", "لا تعمل", "مشكلة", "خطأ",
        "سيء", "أسوأ", "مروع", "فشل",
        "الرسائل لا تصل", "لا يوجد موسيقى",

        # ES
        "suspendido", "baneado", "no funciona", "error",
        "terrible", "horrible", "demasiada publicidad",
        "fotos desordenadas", "fotos mezcladas",

        # RO/BG/Other
        "temele dispărut", "nu funcționează", "blocat", "suspendat",
        "темите изчезнаха", "не работи", "забранен",
    ]

    POS_WORDS = [
        # TR
        "teşekkür", "harika", "mükemmel", "güzel", "süper", "başarılı",
        "memnun", "seviyorum", "bayıldım", "efsane", "müthiş", "kusursuz",
        "pratik", "hızlı", "kaliteli", "faydalı", "yararlı", "şahane",
        "en iyi", "çok iyi", "beğendim", "beğeniyorum", "tavsiye ederim",
        "ideal", "keyifli", "harikasınız", "sağolun", "tebrikler",
        "iyiki", "çok güzel", "çok seviyorum", "seviyorum",
        "on numara", "muhteşem",

        # EN
        "love", "amazing", "great", "excellent", "perfect", "wonderful",
        "fantastic", "awesome", "best", "brilliant", "superb",
        "outstanding", "helpful", "useful", "recommend", "enjoy",
        "enjoying", "happy", "pleased", "satisfied", "good job",
        "well done", "keep it up",

        # AR
        "ممتاز", "احبه", "رائع", "جميل", "افضل", "الافضل",
        "احب", "رائعة", "مميز", "شكرا", "مبدع",

        # RU
        "отлично", "супер", "топ", "нравится", "класс",
        "великолепно", "замечательно", "лучшее", "люблю", "обожаю",
        "молодцы", "спасибо", "прекрасно",

        # FR
        "adore", "j'adore", "génial", "magnifique", "fantastique",
        "parfait", "excellent", "bravo", "merci",

        # DE
        "toll", "ausgezeichnet", "fantastisch", "wunderbar",
        "hervorragend", "prima", "danke", "perfekt",

        # ES/PT
        "ótimo", "excelente", "fantástico", "maravilhoso",
        "buenísimo", "genial",

        # Other
        "świetne", "niezawodny", "très bien", "très bonne",
    ]

    NEU_WORDS = [
        # TR — İstek
        "keşke", "gelse", "olsa", "olurdu", "ekleyin", "ekleseniz",
        "geri getirin", "geri getirilsin", "ne zaman", "neden gelmiyor",
        "yapın", "istiyoruz", "öneri", "eksik",
        "daha iyi olabilir", "bi baksanız", "eklense", "gelsin",
        "düzeltilsin", "düzeltin lütfen", "lütfen ekle",
        "fikrim", "önerim", "bekliyoruz", "özellik istiyorum",
        "ekleyebilirler", "ekleseler",

        # TR — Yeni özellik talepleri (bu veriden)
        "repost özelliği gelsin", "repost geri gelsin",
        "profil görüntüleme gelsin", "takipten çıkanları görelim",
        "hikaye yorumları gelsin", "canlı yayın herkese",
        "çoklu profil fotoğrafı gelsin", "eski filtreleri geri getir",
        "kronolojik sıra", "tarih sırasına göre sıralasın",

        # EN
        "please add", "please fix", "please bring back", "when will",
        "would be nice", "i wish", "suggestion", "request",
        "feature request", "bring back", "need this", "want this",
        "could you add", "consider adding", "hope you add",

        # AR
        "أتمنى", "أريد", "يرجى", "من فضلكم", "اقتراح", "متى",

        # RU
        "хотелось бы", "было бы хорошо", "добавьте", "верните",
        "просьба", "предлагаю", "когда добавят",

        # FR
        "j'aimerais", "serait bien", "s'il vous plaît", "suggestion",
        "quand est-ce",

        # DE
        "wäre schön", "bitte fügt", "wünsche mir", "vorschlag",

        # EN — Ek istek
        "bring back", "please bring back",
        "still don't have", "i still don't have",
        "where is the feature", "when will you add",
        "repost feature", "add repost",
        "story comments", "please add story",
        "reorganize grid", "grid reorder",
        "who views my profile", "profile visits",
        "voice effects", "voice effect update",
        "please return", "return to normal",
        "old layout", "old format",

        # TR — Ek istek
        "repost özelliği", "repost geri",
        "profil ziyareti gelsin", "kim görüntüledi",
        "ses efekti gelmedi", "ses efekti bana",
        "eski düzene dön", "eski arayüze dön",
        "ekleyin lütfen", "geri getirin lütfen",
        "yeni özellik istiyorum",

        # RU — Ek istek
        "верните старый", "верните функцию",
        "добавьте репост", "когда добавят",
        "хотелось бы вернуть",

        # FR — Ek istek
        "remettre", "remettez", "ramener",
        "pouvoir ajouter", "pourrait-on ajouter",

        # DE — Ek istek
        "bringt zurück", "bitte fügt hinzu",
        "wünsche mir zurück",

        # Game/Platform — İstek
        "add chat back", "give us chat",
        "remove age verification", "remove face verification",
        "remove face check", "remove age check",
        "classic faces back", "bring back classic faces",
        "bring back connections", "bring back friends",
        "fix moderation", "fix the moderation",
        "fix age check", "fix face verification",
        "free robux", "give robux",
        "make it free", "should be free",
        "listen to players", "listen to us",
        "listen to your community",
        "fix glitches", "please fix the glitch",
        "add voice chat back", "bring vc back",
    ]

    # ── 7. KRİTİK BUG/CRASH KEYWORDS ─ ÖNCELİKLİ ────────────────────────────────────
    # Bu kelimeler single hit bile olsa olumsuz sinyal vermelidir
    CRITICAL_BUG = [
        "açılmıyor", "añılmıyor", "opens", "doesn't open", "won't open",
        "çalışmıyor", "doesn't work", "won't work", "stopped working",
        "crash", "crashing", "keeps crashing", "crashes", "çöktü", "çöküyor", "çöküp",
        "donuyor", "donmuş", "freezing", "freeze", "laggy", "lag",
        "kayboldu", "kayıp oldu", "disappeared", "disappeared completely", "gone missing",
        "silinmiş", "silindi", "ıraklı veriler", "veriler kayboldu",
        "giremiyorum", "giriş yapamıyorum", "can't login", "login issue",
        "kapanıyor", "closing", "keeps closing",
        "açılmaz", "açılamıyor", "can't open",
        "hata veriyor", "error message", "yine hata",
        "bozuldu", "uygulama bozdu", "app is broken",
        "sikayetler", "ticipale çalışmıyor", "prematüre crashing",
    ]
    
    # ── 8. KEYWORD SCORING ────────────────────────────────────────────────────
    neg_score = sum(1 for w in NEG_WORDS if w in t)
    pos_score = sum(1 for w in POS_WORDS if w in t)
    neu_score = sum(1 for w in NEU_WORDS if w in t)
    
    if any(kw in t for kw in CRITICAL_BUG):
        # Kritik bug bulundu → belki evet ama kontrol et
        if _rating != 5 or neg_score > 0:  # Rating 5 ama bug → content wins
            return {"olumlu": 0.04, "olumsuz": 0.92, "istek_gorus": 0.04, "method": "Heuristic+CriticalBug"}

    # Negatif kelimeler biraz daha ağır
    neg_score_w = neg_score * 1.25

    # Sarkasm bulunmuşsa → içeriği negatif say
    # (ne indirin ne de indirin → keyword yok ama sarkasm var)
    if sarkasm_hit:
        # Eğer açıkça pozitif keyword baskın değilse → olumsuz
        if pos_score <= neg_score or pos_score == 0:
            return {"olumlu": 0.05, "olumsuz": 0.90, "istek_gorus": 0.05, "method": "Heuristic+"}

    # ── 9. "AMA/BUT" PIVOT KURALI ─────────────────────────────────────────────
    PIVOT_TR = [" ama ", " fakat ", " lakin ", " ancak ", " ne var ki "]
    PIVOT_EN = [" but ", " however ", " although ", " though "]
    ALL_PIVOTS = PIVOT_TR + PIVOT_EN

    for pivot in ALL_PIVOTS:
        if pivot in t:
            parts = t.split(pivot, 1)
            after = parts[1] if len(parts) > 1 else ""

            after_neg = sum(1 for w in NEG_WORDS if w in after)
            after_pos = sum(1 for w in POS_WORDS if w in after)

            if after_neg > after_pos and after_neg > 0:
                conf = min(0.88, 0.70 + after_neg * 0.04)
                return {"olumlu": 0.06, "olumsuz": round(conf, 3),
                        "istek_gorus": round(1-conf-0.06, 3), "method": "Heuristic+"}
            if after_pos > after_neg and after_pos > 0:
                conf = min(0.88, 0.70 + after_pos * 0.04)
                return {"olumlu": round(conf, 3), "olumsuz": 0.06,
                        "istek_gorus": round(1-conf-0.06, 3), "method": "Heuristic+"}
            # pivot var ama net karar yok → genel keyword scoring devam etsin
            break

    # ── 9. RATING OVERRIDE (son adım) ────────────────────────────────────────
    # İçerik keyword'lerden karar veremediyse rating'e bak
    total_kw = pos_score + neg_score + neu_score

    if total_kw == 0:
        # Hiç keyword yok → rating'e bak
        if _rating == 1:
            return {"olumlu": 0.05, "olumsuz": 0.88, "istek_gorus": 0.07, "method": "Heuristic+"}
        if _rating == 2:
            return {"olumlu": 0.15, "olumsuz": 0.72, "istek_gorus": 0.13, "method": "Heuristic+"}
        if _rating == 4:
            return {"olumlu": 0.72, "olumsuz": 0.15, "istek_gorus": 0.13, "method": "Heuristic+"}
        if _rating == 5:
            return {"olumlu": 0.85, "olumsuz": 0.08, "istek_gorus": 0.07, "method": "Heuristic+"}
        # rating 3 veya bilinmiyor → nötr
        return {"olumlu": 0.35, "olumsuz": 0.33, "istek_gorus": 0.32, "method": "Heuristic+"}

    # Rating 1 + negatif keyword varsa → çok güçlü negatif sinyal
    if _rating == 1 and neg_score > 0:
        conf = min(0.96, 0.80 + neg_score * 0.04)
        return {"olumlu": round((1-conf)/2, 3), "olumsuz": round(conf, 3),
                "istek_gorus": round((1-conf)/2, 3), "method": "Heuristic+"}

    # Rating 5 ama içerikte net negatif var → content wins
    if _rating == 5 and neg_score > pos_score and neg_score >= 1:
        conf = min(0.88, 0.65 + neg_score * 0.05)
        return {"olumlu": 0.06, "olumsuz": round(conf, 3),
                "istek_gorus": round(1-conf-0.06, 3), "method": "Heuristic+"}

    # ── 10. NORMAL KARAR ──────────────────────────────────────────────────────
    if neg_score_w > pos_score and neg_score_w >= neu_score:
        conf = min(0.95, 0.68 + (neg_score_w / (pos_score + neg_score_w + neu_score)) * 0.27)
        return {"olumlu": round((1-conf)/2, 3), "olumsuz": round(conf, 3),
                "istek_gorus": round((1-conf)/2, 3), "method": "Heuristic+"}

    if pos_score > neg_score and pos_score >= neu_score:
        conf = min(0.95, 0.68 + (pos_score / (pos_score + neg_score_w + neu_score)) * 0.27)
        return {"olumlu": round(conf, 3), "olumsuz": round((1-conf)/2, 3),
                "istek_gorus": round((1-conf)/2, 3), "method": "Heuristic+"}

    if neu_score >= pos_score and neu_score >= neg_score:
        return {"olumlu": 0.08, "olumsuz": 0.07, "istek_gorus": 0.85, "method": "Heuristic+"}

    return {"olumlu": 0.35, "olumsuz": 0.33, "istek_gorus": 0.32, "method": "Heuristic+"}
