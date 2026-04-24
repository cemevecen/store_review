"""Hafif, bağımlılıksız i18n katmanı.

Kullanım:
    from store_review.config.i18n import t
    st.button(t("common.fetch_reviews"))

Bir anahtar mevcut dilde tanımlı değilse Türkçe (default) değere düşer; Türkçe
de yoksa `default` argümanı veya anahtarın kendisi döner.
"""

from __future__ import annotations

import streamlit as st

LANGUAGES: list[tuple[str, str, str]] = [
    ("tr", "Türkçe", "🇹🇷"),
    ("en", "English", "🇬🇧"),
    ("es", "Español", "🇪🇸"),
    ("de", "Deutsch", "🇩🇪"),
    ("fr", "Français", "🇫🇷"),
    ("ar", "العربية", "🇸🇦"),
    ("zh", "简体中文", "🇨🇳"),
    ("ru", "Русский", "🇷🇺"),
    ("pt", "Português", "🇵🇹"),
]

DEFAULT_LANG = "tr"
_LANG_CODES = {code for code, _, _ in LANGUAGES}

STRINGS: dict[str, dict[str, str]] = {
    # --------- Navigation / masthead ---------
    "source.store": {
        "tr": "Mağaza", "en": "Store", "es": "Tienda", "de": "Shop",
        "fr": "Boutique", "ar": "المتجر", "zh": "商店", "ru": "Магазин", "pt": "Loja",
    },
    "source.file": {
        "tr": "Dosya", "en": "File", "es": "Archivo", "de": "Datei",
        "fr": "Fichier", "ar": "ملف", "zh": "文件", "ru": "Файл", "pt": "Arquivo",
    },
    "source.text": {
        "tr": "Metin", "en": "Text", "es": "Texto", "de": "Text",
        "fr": "Texte", "ar": "نص", "zh": "文本", "ru": "Текст", "pt": "Texto",
    },
    "source.compare": {
        "tr": "Uygulama karşılaştır", "en": "Compare apps", "es": "Comparar apps",
        "de": "Apps vergleichen", "fr": "Comparer les apps", "ar": "مقارنة التطبيقات",
        "zh": "应用对比", "ru": "Сравнить приложения", "pt": "Comparar apps",
    },
    "nav.about": {
        "tr": "hakkında", "en": "about", "es": "acerca de", "de": "über",
        "fr": "à propos", "ar": "حول", "zh": "关于", "ru": "о проекте", "pt": "sobre",
    },
    "nav.home": {
        "tr": "ana sayfa", "en": "home", "es": "inicio", "de": "Startseite",
        "fr": "accueil", "ar": "الرئيسية", "zh": "首页", "ru": "главная", "pt": "início",
    },
    "nav.data_source": {
        "tr": "Veri kaynağı", "en": "Data source", "es": "Fuente de datos",
        "de": "Datenquelle", "fr": "Source de données", "ar": "مصدر البيانات",
        "zh": "数据源", "ru": "Источник данных", "pt": "Fonte de dados",
    },
    # --------- Platform + scope toggles ---------
    "platform.label": {
        "tr": "Platform", "en": "Platform", "es": "Plataforma", "de": "Plattform",
        "fr": "Plateforme", "ar": "المنصة", "zh": "平台", "ru": "Платформа", "pt": "Plataforma",
    },
    "scope.label": {
        "tr": "Yorum kaynağı", "en": "Review source", "es": "Fuente de reseñas",
        "de": "Rezensionsquelle", "fr": "Source des avis", "ar": "مصدر المراجعات",
        "zh": "评论来源", "ru": "Источник отзывов", "pt": "Fonte de avaliações",
    },
    "scope.local": {
        "tr": "Yerel", "en": "Local", "es": "Local", "de": "Lokal",
        "fr": "Local", "ar": "محلي", "zh": "本地", "ru": "Локальный", "pt": "Local",
    },
    "scope.global": {
        "tr": "Global", "en": "Global", "es": "Global", "de": "Global",
        "fr": "Global", "ar": "عالمي", "zh": "全球", "ru": "Глобальный", "pt": "Global",
    },
    "scope.help": {
        "tr": "yerel: yalnızca türkiye storefront'u. global: tüm ülkelerden birleşik havuz (varsayılan).",
        "en": "local: turkish storefront only. global: merged pool from all countries (default).",
        "es": "local: solo tienda de turquía. global: pool combinado de todos los países (predeterminado).",
        "de": "lokal: nur türkischer storefront. global: kombinierter pool aller länder (standard).",
        "fr": "local : uniquement la boutique turque. global : pool combiné de tous les pays (par défaut).",
        "ar": "محلي: متجر تركيا فقط. عالمي: تجمع موحد من جميع الدول (افتراضي).",
        "zh": "本地：仅土耳其商店。全球：合并所有国家的评论（默认）。",
        "ru": "локальный: только турецкий сторфронт. глобальный: объединённый пул всех стран (по умолчанию).",
        "pt": "local: apenas loja da turquia. global: pool unificado de todos os países (padrão).",
    },
    # --------- Date range ---------
    "date.range": {
        "tr": "Tarih aralığı", "en": "Date range", "es": "Rango de fechas",
        "de": "Zeitraum", "fr": "Plage de dates", "ar": "النطاق الزمني",
        "zh": "日期范围", "ru": "Период", "pt": "Intervalo de datas",
    },
    "date.placeholder": {
        "tr": "tarih aralığı seç", "en": "select date range", "es": "selecciona el rango",
        "de": "Zeitraum wählen", "fr": "choisir la période", "ar": "اختر النطاق الزمني",
        "zh": "选择日期范围", "ru": "выберите период", "pt": "selecionar intervalo",
    },
    "date.week": {
        "tr": "Son 1 hafta", "en": "Last 7 days", "es": "Última semana",
        "de": "Letzte Woche", "fr": "7 derniers jours", "ar": "آخر ٧ أيام",
        "zh": "最近 1 周", "ru": "За неделю", "pt": "Últimos 7 dias",
    },
    "date.month1": {
        "tr": "Son 1 ay", "en": "Last month", "es": "Último mes",
        "de": "Letzter Monat", "fr": "Dernier mois", "ar": "آخر شهر",
        "zh": "最近 1 个月", "ru": "За месяц", "pt": "Último mês",
    },
    "date.month3": {
        "tr": "Son 3 ay", "en": "Last 3 months", "es": "Últimos 3 meses",
        "de": "Letzte 3 Monate", "fr": "3 derniers mois", "ar": "آخر ٣ أشهر",
        "zh": "最近 3 个月", "ru": "За 3 месяца", "pt": "Últimos 3 meses",
    },
    "date.month6": {
        "tr": "Son 6 ay", "en": "Last 6 months", "es": "Últimos 6 meses",
        "de": "Letzte 6 Monate", "fr": "6 derniers mois", "ar": "آخر ٦ أشهر",
        "zh": "最近 6 个月", "ru": "За 6 месяцев", "pt": "Últimos 6 meses",
    },
    "date.year1": {
        "tr": "Son 1 yıl", "en": "Last year", "es": "Último año",
        "de": "Letztes Jahr", "fr": "Dernière année", "ar": "آخر سنة",
        "zh": "最近 1 年", "ru": "За год", "pt": "Último ano",
    },
    "date.year2": {
        "tr": "Son 2 yıl", "en": "Last 2 years", "es": "Últimos 2 años",
        "de": "Letzte 2 Jahre", "fr": "2 dernières années", "ar": "آخر سنتين",
        "zh": "最近 2 年", "ru": "За 2 года", "pt": "Últimos 2 anos",
    },
    # --------- Common buttons ---------
    "common.fetch_reviews": {
        "tr": "Yorumları çek", "en": "Fetch reviews", "es": "Obtener reseñas",
        "de": "Rezensionen abrufen", "fr": "Récupérer les avis", "ar": "جلب المراجعات",
        "zh": "获取评论", "ru": "Загрузить отзывы", "pt": "Carregar avaliações",
    },
    "common.start_compare": {
        "tr": "Karşılaştırmayı başlat", "en": "Start comparison", "es": "Iniciar comparación",
        "de": "Vergleich starten", "fr": "Démarrer la comparaison", "ar": "بدء المقارنة",
        "zh": "开始比较", "ru": "Начать сравнение", "pt": "Iniciar comparação",
    },
    "common.reset": {
        "tr": "Sıfırla", "en": "Reset", "es": "Reiniciar", "de": "Zurücksetzen",
        "fr": "Réinitialiser", "ar": "إعادة تعيين", "zh": "重置", "ru": "Сбросить", "pt": "Redefinir",
    },
    "common.reset_selection": {
        "tr": "Seçimi sıfırla", "en": "Clear selection", "es": "Limpiar selección",
        "de": "Auswahl zurücksetzen", "fr": "Effacer la sélection", "ar": "مسح الاختيار",
        "zh": "清除选择", "ru": "Сбросить выбор", "pt": "Limpar seleção",
    },
    "common.select": {
        "tr": "Seç", "en": "Select", "es": "Elegir", "de": "Wählen",
        "fr": "Choisir", "ar": "اختر", "zh": "选择", "ru": "Выбрать", "pt": "Selecionar",
    },
    "common.show_more": {
        "tr": "Daha fazla göster", "en": "Show more", "es": "Mostrar más",
        "de": "Mehr anzeigen", "fr": "Voir plus", "ar": "عرض المزيد",
        "zh": "显示更多", "ru": "Показать ещё", "pt": "Mostrar mais",
    },
    "common.clear_results": {
        "tr": "Sonuçları temizle", "en": "Clear results", "es": "Limpiar resultados",
        "de": "Ergebnisse löschen", "fr": "Effacer les résultats", "ar": "مسح النتائج",
        "zh": "清除结果", "ru": "Очистить результаты", "pt": "Limpar resultados",
    },
    "common.show_all": {
        "tr": "Tümünü gör", "en": "Show all", "es": "Ver todo",
        "de": "Alle anzeigen", "fr": "Tout afficher", "ar": "عرض الكل",
        "zh": "全部显示", "ru": "Показать всё", "pt": "Ver tudo",
    },
    # --------- Review cards ---------
    "cards.expand_with_count": {
        "tr": "genişlet · {n} yorum daha göster",
        "en": "expand · show {n} more reviews",
        "es": "expandir · mostrar {n} reseñas más",
        "de": "erweitern · {n} weitere Rezensionen anzeigen",
        "fr": "développer · afficher {n} avis de plus",
        "ar": "توسيع · عرض {n} مراجعة إضافية",
        "zh": "展开 · 再显示 {n} 条评论",
        "ru": "развернуть · показать ещё {n} отзывов",
        "pt": "expandir · mostrar mais {n} avaliações",
    },
    "cards.collapse_to_preview": {
        "tr": "daralt · ilk 5 yoruma dön",
        "en": "collapse · back to first 5 reviews",
        "es": "contraer · volver a las 5 primeras reseñas",
        "de": "einklappen · zurück zu den ersten 5 Rezensionen",
        "fr": "réduire · revenir aux 5 premiers avis",
        "ar": "طيّ · العودة إلى أول 5 مراجعات",
        "zh": "收起 · 返回前 5 条评论",
        "ru": "свернуть · вернуться к первым 5 отзывам",
        "pt": "recolher · voltar às 5 primeiras avaliações",
    },
    "cards.prev": {
        "tr": "Önceki", "en": "Previous", "es": "Anterior", "de": "Zurück",
        "fr": "Précédent", "ar": "السابق", "zh": "上一页", "ru": "Назад", "pt": "Anterior",
    },
    "cards.next": {
        "tr": "Sonraki", "en": "Next", "es": "Siguiente", "de": "Weiter",
        "fr": "Suivant", "ar": "التالي", "zh": "下一页", "ru": "Далее", "pt": "Próximo",
    },
    "cards.paging_hint": {
        "tr": "Çok sayfa ({n}); **Önceki** / **Sonraki** ile gezinin.",
        "en": "Many pages ({n}); navigate with **Previous** / **Next**.",
        "es": "Muchas páginas ({n}); navega con **Anterior** / **Siguiente**.",
        "de": "Viele Seiten ({n}); mit **Zurück** / **Weiter** navigieren.",
        "fr": "Plusieurs pages ({n}); naviguez avec **Précédent** / **Suivant**.",
        "ar": "صفحات كثيرة ({n})؛ تنقل عبر **السابق** / **التالي**.",
        "zh": "共 {n} 页；使用 **上一页** / **下一页** 浏览。",
        "ru": "Много страниц ({n}); используйте **Назад** / **Далее**.",
        "pt": "Muitas páginas ({n}); use **Anterior** / **Próximo**.",
    },
    "cards.collapse_list": {
        "tr": "50'şer göster", "en": "Show in pages of 50",
        "es": "Mostrar de 50 en 50", "de": "In 50er-Schritten anzeigen",
        "fr": "Afficher par tranches de 50", "ar": "عرض كل 50",
        "zh": "每页 50 条", "ru": "Показывать по 50", "pt": "Mostrar de 50 em 50",
    },
    "cards.page_info": {
        "tr": "**{start}–{end}** / {n} yorum · sayfa **{page}** / **{total}**",
        "en": "**{start}–{end}** / {n} reviews · page **{page}** / **{total}**",
        "es": "**{start}–{end}** / {n} reseñas · página **{page}** / **{total}**",
        "de": "**{start}–{end}** / {n} Rezensionen · Seite **{page}** / **{total}**",
        "fr": "**{start}–{end}** / {n} avis · page **{page}** / **{total}**",
        "ar": "**{start}–{end}** / {n} مراجعة · صفحة **{page}** / **{total}**",
        "zh": "**{start}–{end}** / {n} 条评论 · 第 **{page}** / **{total}** 页",
        "ru": "**{start}–{end}** / {n} отзывов · стр. **{page}** / **{total}**",
        "pt": "**{start}–{end}** / {n} avaliações · página **{page}** / **{total}**",
    },
    # --------- Compare panel ---------
    "compare.slot_heading": {
        "tr": "Uygulama {i}", "en": "App {i}", "es": "App {i}", "de": "App {i}",
        "fr": "App {i}", "ar": "التطبيق {i}", "zh": "应用 {i}", "ru": "Приложение {i}", "pt": "App {i}",
    },
    "compare.analysis_settings": {
        "tr": "Analiz ayarları", "en": "Analysis settings", "es": "Ajustes de análisis",
        "de": "Analyse-Einstellungen", "fr": "Paramètres d'analyse", "ar": "إعدادات التحليل",
        "zh": "分析设置", "ru": "Настройки анализа", "pt": "Configurações de análise",
    },
    "compare.method_fast": {
        "tr": "Hızlı (heuristic)", "en": "Fast (heuristic)", "es": "Rápido (heurística)",
        "de": "Schnell (heuristisch)", "fr": "Rapide (heuristique)", "ar": "سريع (استدلالي)",
        "zh": "快速（启发式）", "ru": "Быстрый (эвристика)", "pt": "Rápido (heurística)",
    },
    "compare.method_rich": {
        "tr": "Zengin (LLM)", "en": "Rich (LLM)", "es": "Avanzado (LLM)",
        "de": "Ausführlich (LLM)", "fr": "Enrichi (LLM)", "ar": "غني (LLM)",
        "zh": "丰富（LLM）", "ru": "Расширенный (LLM)", "pt": "Avançado (LLM)",
    },
    "compare.depth_label": {
        "tr": "Derinlik (yalnız zengin)", "en": "Depth (rich only)",
        "es": "Profundidad (solo avanzado)", "de": "Tiefe (nur ausführlich)",
        "fr": "Profondeur (enrichi)", "ar": "العمق (غني فقط)",
        "zh": "深度（仅丰富）", "ru": "Глубина (только расширенный)",
        "pt": "Profundidade (apenas avançado)",
    },
    "compare.depth_std": {
        "tr": "Standart", "en": "Standard", "es": "Estándar", "de": "Standard",
        "fr": "Standard", "ar": "قياسي", "zh": "标准", "ru": "Стандарт", "pt": "Padrão",
    },
    "compare.depth_adv": {
        "tr": "Gelişmiş", "en": "Advanced", "es": "Avanzado", "de": "Erweitert",
        "fr": "Avancé", "ar": "متقدم", "zh": "高级", "ru": "Расширенный", "pt": "Avançado",
    },
    "compare.prep_title": {
        "tr": "yorum havuzu hazırlanıyor", "en": "preparing review pool",
        "es": "preparando reseñas", "de": "Rezensionspool wird vorbereitet",
        "fr": "préparation des avis", "ar": "تحضير تجمع المراجعات",
        "zh": "正在准备评论池", "ru": "готовим пул отзывов", "pt": "preparando avaliações",
    },
    "compare.pool_summary_head": {
        "tr": "havuzdaki yorum", "en": "reviews in pool", "es": "reseñas en pool",
        "de": "Rezensionen im Pool", "fr": "avis dans le pool", "ar": "المراجعات في التجمع",
        "zh": "池中评论数", "ru": "отзывов в пуле", "pt": "avaliações no pool",
    },
    "compare.hint_pick_date": {
        "tr": "iki uygulamayı seçtikten sonra tarih aralığı seçince havuzlar otomatik hazırlanır.",
        "en": "after picking both apps, choosing a date range will automatically prepare the pools.",
        "es": "tras elegir ambas apps, seleccionar un rango de fechas preparará los pools automáticamente.",
        "de": "nach Auswahl beider Apps startet das Vorbereiten der Pools automatisch, sobald ein Zeitraum gewählt wird.",
        "fr": "après avoir choisi les deux apps, le choix d'une période prépare automatiquement les pools.",
        "ar": "بعد اختيار التطبيقين، سيؤدي تحديد النطاق الزمني إلى تحضير التجمعات تلقائيًا.",
        "zh": "选定两个应用后，选择日期范围将自动开始准备评论池。",
        "ru": "после выбора двух приложений выбор периода автоматически запустит подготовку пулов.",
        "pt": "após escolher os dois apps, selecionar um intervalo de datas prepara os pools automaticamente.",
    },
    "compare.elapsed": {
        "tr": "geçen", "en": "elapsed", "es": "transcurrido", "de": "vergangen",
        "fr": "écoulé", "ar": "مضى", "zh": "已用", "ru": "прошло", "pt": "decorrido",
    },
    # --------- Store panel ---------
    "store.input_label": {
        "tr": "Uygulama ara veya mağaza linki / ID",
        "en": "Search an app or paste a store link / ID",
        "es": "Busca una app o pega un enlace / ID",
        "de": "App suchen oder Link / ID einfügen",
        "fr": "Rechercher une app ou coller un lien / ID",
        "ar": "ابحث عن تطبيق أو ألصق رابط / معرف المتجر",
        "zh": "搜索应用或粘贴商店链接 / ID",
        "ru": "Поиск приложения либо ссылка / ID магазина",
        "pt": "Busque um app ou cole link / ID da loja",
    },
    "store.input_placeholder": {
        "tr": "Örn. döviz, com.whatsapp mağaza linki",
        "en": "e.g. finance, com.whatsapp, store link",
        "es": "Ej. finanzas, com.whatsapp, enlace a la tienda",
        "de": "z. B. Finanzen, com.whatsapp, Store-Link",
        "fr": "ex. finance, com.whatsapp, lien boutique",
        "ar": "مثال: تطبيق مالي أو com.whatsapp أو رابط متجر",
        "zh": "例如：finance、com.whatsapp、商店链接",
        "ru": "Напр. finance, com.whatsapp, ссылка магазина",
        "pt": "Ex. finanças, com.whatsapp, link da loja",
    },
    "compare.input_placeholder": {
        "tr": "Örn. trendyol, com.example, App Store ID veya mağaza linki",
        "en": "e.g. trendyol, com.example, App Store ID or store link",
        "es": "Ej. trendyol, com.example, ID de App Store o enlace",
        "de": "z. B. trendyol, com.example, App-Store-ID oder Link",
        "fr": "ex. trendyol, com.example, ID App Store ou lien boutique",
        "ar": "مثال: trendyol أو com.example أو معرف App Store أو رابط متجر",
        "zh": "例如：trendyol、com.example、App Store ID 或商店链接",
        "ru": "Напр. trendyol, com.example, App Store ID или ссылка",
        "pt": "Ex. trendyol, com.example, ID do App Store ou link",
    },
    "store.found_apps": {
        "tr": "Bulunan uygulamalar ({n})",
        "en": "Apps found ({n})",
        "es": "Apps encontradas ({n})",
        "de": "Gefundene Apps ({n})",
        "fr": "Apps trouvées ({n})",
        "ar": "التطبيقات الموجودة ({n})",
        "zh": "找到的应用（{n}）",
        "ru": "Найдено приложений ({n})",
        "pt": "Apps encontrados ({n})",
    },
    "store.no_results": {
        "tr": "Sonuç bulunamadı. Farklı anahtar kelime veya platform deneyin.",
        "en": "No results. Try a different keyword or platform.",
        "es": "Sin resultados. Prueba otra palabra clave o plataforma.",
        "de": "Keine Treffer. Bitte anderes Stichwort oder Plattform probieren.",
        "fr": "Aucun résultat. Essayez un autre mot-clé ou plateforme.",
        "ar": "لا توجد نتائج. جرّب كلمة أو منصة أخرى.",
        "zh": "无结果。请尝试其他关键字或平台。",
        "ru": "Ничего не найдено. Попробуйте другое слово или платформу.",
        "pt": "Sem resultados. Tente outra palavra-chave ou plataforma.",
    },
    "store.need_selection": {
        "tr": "Önce listeden bir uygulama **Seç** deyin veya geçerli paket / ID / ürün linki girin.",
        "en": "Please **Select** an app from the list or enter a valid package / ID / product link.",
        "es": "**Elige** una app de la lista o introduce un paquete / ID / enlace válido.",
        "de": "Bitte eine App aus der Liste **wählen** oder gültiges Paket / ID / Link eingeben.",
        "fr": "**Choisissez** une app dans la liste ou saisissez un package / ID / lien valide.",
        "ar": "يرجى **اختيار** تطبيق من القائمة أو إدخال حزمة / معرف / رابط صالح.",
        "zh": "请从列表中 **选择** 应用，或输入有效的包名 / ID / 商品链接。",
        "ru": "**Выберите** приложение из списка или введите пакет / ID / ссылку.",
        "pt": "**Selecione** um app da lista ou insira um pacote / ID / link válido.",
    },
    "store.loaded_summary": {
        "tr": "{n} benzersiz yorum yüklendi ({range} · {scope}).",
        "en": "{n} unique reviews loaded ({range} · {scope}).",
        "es": "{n} reseñas únicas cargadas ({range} · {scope}).",
        "de": "{n} eindeutige Rezensionen geladen ({range} · {scope}).",
        "fr": "{n} avis uniques chargés ({range} · {scope}).",
        "ar": "تم تحميل {n} مراجعة فريدة ({range} · {scope}).",
        "zh": "已加载 {n} 条独立评论（{range} · {scope}）。",
        "ru": "Загружено {n} уникальных отзывов ({range} · {scope}).",
        "pt": "{n} avaliações únicas carregadas ({range} · {scope}).",
    },
    "store.fetch_error": {
        "tr": "Çekim hatası: {err}", "en": "Fetch error: {err}",
        "es": "Error al obtener: {err}", "de": "Abruffehler: {err}",
        "fr": "Erreur de récupération : {err}", "ar": "خطأ في الجلب: {err}",
        "zh": "获取错误：{err}", "ru": "Ошибка загрузки: {err}", "pt": "Erro ao buscar: {err}",
    },
    # --------- File / paste tabs ---------
    "file.upload_label": {
        "tr": "Dosya seç", "en": "Choose a file", "es": "Elegir archivo",
        "de": "Datei wählen", "fr": "Choisir un fichier", "ar": "اختر ملفًا",
        "zh": "选择文件", "ru": "Выбрать файл", "pt": "Escolher arquivo",
    },
    "file.clear_pool": {
        "tr": "Dosya havuzunu temizle", "en": "Clear file pool",
        "es": "Limpiar pool de archivos", "de": "Dateipool leeren",
        "fr": "Vider le pool de fichiers", "ar": "مسح تجمع الملفات",
        "zh": "清除文件池", "ru": "Очистить файл-пул", "pt": "Limpar pool de arquivos",
    },
    "file.loaded_single": {
        "tr": "Yüklenen dosya: **{file}** — **{n}** yorum. Başka dosya ekleyerek havuzu büyütebilirsiniz.",
        "en": "Uploaded file: **{file}** — **{n}** reviews. Add more files to grow the pool.",
        "es": "Archivo cargado: **{file}** — **{n}** reseñas. Puedes añadir más archivos.",
        "de": "Hochgeladene Datei: **{file}** — **{n}** Rezensionen. Weitere Dateien hinzufügen möglich.",
        "fr": "Fichier chargé : **{file}** — **{n}** avis. Ajoutez d'autres fichiers pour agrandir le pool.",
        "ar": "الملف المحمّل: **{file}** — **{n}** مراجعة. يمكن إضافة ملفات أخرى.",
        "zh": "已上传文件：**{file}** — **{n}** 条评论。可继续添加文件扩充评论池。",
        "ru": "Загруженный файл: **{file}** — **{n}** отзывов. Можно добавить ещё.",
        "pt": "Arquivo carregado: **{file}** — **{n}** avaliações. Adicione outros para ampliar o pool.",
    },
    "file.loaded_merged": {
        "tr": "**{count} dosya** birleşik havuz ({files}{more}) — **{n}** benzersiz yorum. Yeni dosya ekleyebilirsiniz.",
        "en": "**{count} files** merged pool ({files}{more}) — **{n}** unique reviews. You can add more.",
        "es": "**{count} archivos** pool combinado ({files}{more}) — **{n}** reseñas únicas. Puedes añadir más.",
        "de": "**{count} Dateien** kombinierter Pool ({files}{more}) — **{n}** eindeutige Rezensionen.",
        "fr": "**{count} fichiers** pool combiné ({files}{more}) — **{n}** avis uniques.",
        "ar": "**{count} ملفات** تجمع موحد ({files}{more}) — **{n}** مراجعة فريدة.",
        "zh": "**{count} 个文件** 合并池（{files}{more}）— **{n}** 条独立评论。",
        "ru": "**{count} файлов** объединённый пул ({files}{more}) — **{n}** уникальных отзывов.",
        "pt": "**{count} arquivos** pool combinado ({files}{more}) — **{n}** avaliações únicas.",
    },
    "paste.label": {
        "tr": "Yorumlar", "en": "Reviews", "es": "Reseñas", "de": "Rezensionen",
        "fr": "Avis", "ar": "المراجعات", "zh": "评论", "ru": "Отзывы", "pt": "Avaliações",
    },
    "paste.placeholder": {
        "tr": "Örn: Uygulama çok iyi ama bildirimler bazen geç geliyor.\nHer satıra bir yorum…",
        "en": "e.g. The app is great but notifications are sometimes late.\nOne review per line…",
        "es": "Ej.: La app es genial pero las notificaciones llegan tarde.\nUna reseña por línea…",
        "de": "z. B. Die App ist super, aber Benachrichtigungen kommen manchmal spät.\nEine Rezension pro Zeile…",
        "fr": "ex. : L'app est super mais les notifications arrivent tard.\nUn avis par ligne…",
        "ar": "مثال: التطبيق ممتاز لكن الإشعارات أحيانًا متأخرة.\nمراجعة واحدة في كل سطر…",
        "zh": "例如：应用很好，但通知有时较慢。\n每行一条评论……",
        "ru": "Напр.: Приложение классное, но уведомления иногда опаздывают.\nПо одному отзыву в строке…",
        "pt": "Ex.: O app é ótimo, mas notificações às vezes atrasam.\nUma avaliação por linha…",
    },
    "paste.upload_btn": {
        "tr": "Metni havuza yükle", "en": "Add text to pool",
        "es": "Añadir texto al pool", "de": "Text in Pool übernehmen",
        "fr": "Ajouter le texte au pool", "ar": "إضافة النص إلى التجمع",
        "zh": "将文本添加到评论池", "ru": "Добавить текст в пул", "pt": "Adicionar ao pool",
    },
    # --------- Dashboard / analysis ---------
    "metric.pool_count": {
        "tr": "Havuzdaki yorum", "en": "Reviews in pool", "es": "Reseñas en el pool",
        "de": "Rezensionen im Pool", "fr": "Avis dans le pool", "ar": "المراجعات في التجمع",
        "zh": "池中评论数", "ru": "Отзывов в пуле", "pt": "Avaliações no pool",
    },
    "section.analysis_settings": {
        "tr": "Analiz ayarları", "en": "Analysis settings",
        "es": "Ajustes de análisis", "de": "Analyse-Einstellungen",
        "fr": "Paramètres d'analyse", "ar": "إعدادات التحليل",
        "zh": "分析设置", "ru": "Настройки анализа", "pt": "Configurações de análise",
    },
    "section.reviews": {
        "tr": "Yorumlar", "en": "Reviews", "es": "Reseñas", "de": "Rezensionen",
        "fr": "Avis", "ar": "المراجعات", "zh": "评论", "ru": "Отзывы", "pt": "Avaliações",
    },
    "analysis.start": {
        "tr": "Duygu analizini başlat", "en": "Start sentiment analysis",
        "es": "Iniciar análisis de sentimiento", "de": "Sentiment-Analyse starten",
        "fr": "Démarrer l'analyse des sentiments", "ar": "بدء تحليل المشاعر",
        "zh": "开始情感分析", "ru": "Начать анализ тональности", "pt": "Iniciar análise de sentimento",
    },
    "analysis.warn_load_first": {
        "tr": "Önce yorum yükleyin.", "en": "Please load reviews first.",
        "es": "Primero carga reseñas.", "de": "Bitte zuerst Rezensionen laden.",
        "fr": "Veuillez d'abord charger des avis.", "ar": "يرجى تحميل المراجعات أولاً.",
        "zh": "请先加载评论。", "ru": "Сначала загрузите отзывы.", "pt": "Carregue avaliações primeiro.",
    },
    "analysis.err_need_api": {
        "tr": "Zengin analiz için en az bir API anahtarı gerekir.",
        "en": "Rich analysis needs at least one API key.",
        "es": "El análisis avanzado requiere al menos una clave API.",
        "de": "Ausführliche Analyse benötigt mindestens einen API-Key.",
        "fr": "L'analyse enrichie nécessite au moins une clé API.",
        "ar": "يحتاج التحليل الغني إلى مفتاح API واحد على الأقل.",
        "zh": "丰富分析至少需要一个 API 密钥。",
        "ru": "Для расширенного анализа нужен хотя бы один API-ключ.",
        "pt": "Análise avançada requer ao menos uma chave de API.",
    },
    "analysis.spinner": {
        "tr": "Yorumlar analiz ediliyor…", "en": "Analyzing reviews…",
        "es": "Analizando reseñas…", "de": "Rezensionen werden analysiert…",
        "fr": "Analyse des avis…", "ar": "جارٍ تحليل المراجعات…",
        "zh": "正在分析评论……", "ru": "Анализируем отзывы…", "pt": "Analisando avaliações…",
    },
    "compare.spinner": {
        "tr": "Uygulamalar analiz ediliyor…", "en": "Analyzing apps…",
        "es": "Analizando apps…", "de": "Apps werden analysiert…",
        "fr": "Analyse des apps…", "ar": "جارٍ تحليل التطبيقات…",
        "zh": "正在分析应用……", "ru": "Анализируем приложения…", "pt": "Analisando apps…",
    },
    "compare.warn_need_pools": {
        "tr": "Önce iki uygulama için de yorum havuzu hazırlanmalı.",
        "en": "Prepare review pools for both apps first.",
        "es": "Prepara primero los pools de ambas apps.",
        "de": "Zuerst Pools für beide Apps vorbereiten.",
        "fr": "Préparez d'abord les pools des deux apps.",
        "ar": "حضّر تجمعات المراجعات للتطبيقين أولاً.",
        "zh": "请先为两个应用准备评论池。",
        "ru": "Сначала подготовьте пулы для обоих приложений.",
        "pt": "Prepare primeiro os pools dos dois apps.",
    },
    "compare.err_unresolvable_long": {
        "tr": "Uygulama {i}: giriş çözülemedi (`{raw}…`)",
        "en": "App {i}: could not resolve input (`{raw}…`)",
        "es": "App {i}: no se pudo resolver la entrada (`{raw}…`)",
        "de": "App {i}: Eingabe nicht auflösbar (`{raw}…`)",
        "fr": "App {i} : entrée irrésolue (`{raw}…`)",
        "ar": "التطبيق {i}: تعذّر تحليل المدخل (`{raw}…`)",
        "zh": "应用 {i}：无法解析输入（`{raw}…`）",
        "ru": "Приложение {i}: не удалось распознать ввод (`{raw}…`)",
        "pt": "App {i}: entrada não resolvida (`{raw}…`)",
    },
    "compare.err_unresolvable": {
        "tr": "Uygulama {i}: giriş çözülemedi.",
        "en": "App {i}: could not resolve input.",
        "es": "App {i}: no se pudo resolver la entrada.",
        "de": "App {i}: Eingabe nicht auflösbar.",
        "fr": "App {i} : entrée irrésolue.",
        "ar": "التطبيق {i}: تعذّر تحليل المدخل.",
        "zh": "应用 {i}：无法解析输入。",
        "ru": "Приложение {i}: не удалось распознать ввод.",
        "pt": "App {i}: entrada não resolvida.",
    },
    "compare.err_rich_api": {
        "tr": "Zengin analiz için en az bir API anahtarı gerekir (.env veya Streamlit secrets).",
        "en": "Rich analysis needs at least one API key (.env or Streamlit secrets).",
        "es": "El análisis avanzado requiere al menos una clave API (.env o Streamlit secrets).",
        "de": "Ausführliche Analyse benötigt mindestens einen API-Key (.env oder Streamlit-Secrets).",
        "fr": "L'analyse enrichie nécessite au moins une clé API (.env ou Streamlit secrets).",
        "ar": "يحتاج التحليل الغني إلى مفتاح API واحد على الأقل (.env أو Streamlit secrets).",
        "zh": "丰富分析至少需要一个 API 密钥（.env 或 Streamlit secrets）。",
        "ru": "Для расширенного анализа нужен хотя бы один API-ключ (.env или Streamlit secrets).",
        "pt": "Análise avançada requer ao menos uma chave de API (.env ou Streamlit secrets).",
    },
    # --------- Downloads ---------
    "download.raw_section": {
        "tr": "Ham veriyi indir (analiz öncesi)", "en": "Download raw data (before analysis)",
        "es": "Descargar datos sin procesar (antes del análisis)",
        "de": "Rohdaten herunterladen (vor der Analyse)",
        "fr": "Télécharger les données brutes (avant analyse)",
        "ar": "تنزيل البيانات الخام (قبل التحليل)",
        "zh": "下载原始数据（分析前）",
        "ru": "Скачать исходные данные (до анализа)",
        "pt": "Baixar dados brutos (antes da análise)",
    },
    "download.csv": {
        "tr": "CSV indir", "en": "Download CSV", "es": "Descargar CSV",
        "de": "CSV herunterladen", "fr": "Télécharger CSV", "ar": "تنزيل CSV",
        "zh": "下载 CSV", "ru": "Скачать CSV", "pt": "Baixar CSV",
    },
    "download.excel": {
        "tr": "Excel indir", "en": "Download Excel", "es": "Descargar Excel",
        "de": "Excel herunterladen", "fr": "Télécharger Excel", "ar": "تنزيل Excel",
        "zh": "下载 Excel", "ru": "Скачать Excel", "pt": "Baixar Excel",
    },
    "download.pdf": {
        "tr": "PDF indir", "en": "Download PDF", "es": "Descargar PDF",
        "de": "PDF herunterladen", "fr": "Télécharger PDF", "ar": "تنزيل PDF",
        "zh": "下载 PDF", "ru": "Скачать PDF", "pt": "Baixar PDF",
    },
    "download.analysis_csv": {
        "tr": "Sonuçları CSV indir", "en": "Download results (CSV)",
        "es": "Descargar resultados (CSV)", "de": "Ergebnisse als CSV herunterladen",
        "fr": "Télécharger les résultats (CSV)", "ar": "تنزيل النتائج (CSV)",
        "zh": "下载结果 (CSV)", "ru": "Скачать результаты (CSV)", "pt": "Baixar resultados (CSV)",
    },
    "download.analysis_pdf": {
        "tr": "Sonuçları PDF indir", "en": "Download results (PDF)",
        "es": "Descargar resultados (PDF)", "de": "Ergebnisse als PDF herunterladen",
        "fr": "Télécharger les résultats (PDF)", "ar": "تنزيل النتائج (PDF)",
        "zh": "下载结果 (PDF)", "ru": "Скачать результаты (PDF)", "pt": "Baixar resultados (PDF)",
    },
    # --------- Analysis dashboard ---------
    "dash.page_title": {
        "tr": "Analiz Sonuçları ve İstatistikler", "en": "Analysis results & statistics",
        "es": "Resultados del análisis y estadísticas", "de": "Analyseergebnisse & Statistiken",
        "fr": "Résultats d'analyse & statistiques", "ar": "نتائج التحليل والإحصائيات",
        "zh": "分析结果与统计", "ru": "Результаты анализа и статистика",
        "pt": "Resultados da análise e estatísticas",
    },
    "dash.sent_dist": {
        "tr": "Duygu Dağılımı", "en": "Sentiment distribution",
        "es": "Distribución de sentimiento", "de": "Sentiment-Verteilung",
        "fr": "Distribution du sentiment", "ar": "توزيع المشاعر",
        "zh": "情感分布", "ru": "Распределение тональности", "pt": "Distribuição de sentimento",
    },
    "dash.score_dist": {
        "tr": "Puan Dağılımı", "en": "Rating distribution",
        "es": "Distribución de puntuaciones", "de": "Bewertungsverteilung",
        "fr": "Distribution des notes", "ar": "توزيع التقييمات",
        "zh": "评分分布", "ru": "Распределение оценок", "pt": "Distribuição de notas",
    },
    "dash.no_data_yet": {
        "tr": "Henüz yeterli veri yok.", "en": "Not enough data yet.",
        "es": "Aún no hay suficientes datos.", "de": "Noch nicht genug Daten.",
        "fr": "Pas encore assez de données.", "ar": "لا توجد بيانات كافية بعد.",
        "zh": "数据尚不足。", "ru": "Данных пока недостаточно.", "pt": "Dados insuficientes ainda.",
    },
    "dash.missing_cols": {
        "tr": "Analiz sonucu sütunları eksik.", "en": "Analysis output columns are missing.",
        "es": "Faltan columnas del resultado del análisis.", "de": "Analyse-Ergebnisspalten fehlen.",
        "fr": "Colonnes du résultat d'analyse manquantes.", "ar": "أعمدة نتائج التحليل مفقودة.",
        "zh": "分析结果列缺失。", "ru": "Нет колонок с результатом анализа.",
        "pt": "Faltam colunas do resultado da análise.",
    },
    "dash.exp_score": {
        "tr": "Genel Deneyim Skoru", "en": "Overall experience score",
        "es": "Puntuación global de experiencia", "de": "Gesamt-Erlebnis-Score",
        "fr": "Score d'expérience global", "ar": "درجة التجربة العامة",
        "zh": "总体体验评分", "ru": "Общая оценка опыта", "pt": "Pontuação geral de experiência",
    },
    "dash.trend": {
        "tr": "Trend", "en": "Trend", "es": "Tendencia", "de": "Trend",
        "fr": "Tendance", "ar": "الاتجاه", "zh": "趋势", "ru": "Тренд", "pt": "Tendência",
    },
    "dash.daily_neg": {
        "tr": "Günlük Olumsuz Oran", "en": "Daily negative rate",
        "es": "Tasa diaria de negativos", "de": "Tägliche Negativrate",
        "fr": "Taux négatif quotidien", "ar": "النسبة السلبية اليومية",
        "zh": "每日负面比率", "ru": "Доля негатива по дням", "pt": "Taxa negativa diária",
    },
    "dash.persona": {
        "tr": "Kullanıcı Profili (Persona)", "en": "User profile (persona)",
        "es": "Perfil de usuario (persona)", "de": "Nutzerprofil (Persona)",
        "fr": "Profil utilisateur (persona)", "ar": "ملف المستخدم (Persona)",
        "zh": "用户画像（Persona）", "ru": "Профиль пользователя (Persona)",
        "pt": "Perfil do usuário (persona)",
    },
    "dash.sent_pos": {
        "tr": "Olumlu", "en": "Positive", "es": "Positivo", "de": "Positiv",
        "fr": "Positif", "ar": "إيجابي", "zh": "正面", "ru": "Позитивные", "pt": "Positivo",
    },
    "dash.sent_neg": {
        "tr": "Olumsuz", "en": "Negative", "es": "Negativo", "de": "Negativ",
        "fr": "Négatif", "ar": "سلبي", "zh": "负面", "ru": "Негативные", "pt": "Negativo",
    },
    "dash.sent_req": {
        "tr": "İstek/Görüş", "en": "Request / opinion", "es": "Solicitud / opinión",
        "de": "Anfrage / Meinung", "fr": "Demande / avis", "ar": "طلب / رأي",
        "zh": "建议 / 意见", "ru": "Запрос / мнение", "pt": "Sugestão / opinião",
    },
    "store.slot_input_label": {
        "tr": "{heading} — uygulama ara veya mağaza linki / ID",
        "en": "{heading} — search an app or paste a store link / ID",
        "es": "{heading} — busca una app o pega un enlace / ID",
        "de": "{heading} — App suchen oder Link / ID einfügen",
        "fr": "{heading} — rechercher une app ou coller un lien / ID",
        "ar": "{heading} — ابحث عن تطبيق أو ألصق رابط / معرف المتجر",
        "zh": "{heading} — 搜索应用或粘贴商店链接 / ID",
        "ru": "{heading} — поиск приложения либо ссылка / ID",
        "pt": "{heading} — busque um app ou cole link / ID",
    },
    # --------- Footer ---------
    "footer.language_options": {
        "tr": "Dil seçenekleri", "en": "Language options", "es": "Opciones de idioma",
        "de": "Spracheinstellungen", "fr": "Options de langue", "ar": "خيارات اللغة",
        "zh": "语言选项", "ru": "Выбор языка", "pt": "Opções de idioma",
    },
    "footer.quick_access": {
        "tr": "Hızlı erişim", "en": "Quick access", "es": "Acceso rápido",
        "de": "Schnellzugriff", "fr": "Accès rapide", "ar": "وصول سريع",
        "zh": "快速访问", "ru": "Быстрый доступ", "pt": "Acesso rápido",
    },
    "footer.developed_by": {
        "tr": "geliştiren: cem evecen", "en": "developer: cem evecen",
        "es": "desarrollador: cem evecen", "de": "Entwickler: cem evecen",
        "fr": "développeur : cem evecen", "ar": "المطور: جيم إيڤجن",
        "zh": "开发者：cem evecen", "ru": "разработчик: cem evecen",
        "pt": "desenvolvedor: cem evecen",
    },
}


def _sync_query_param(code: str) -> None:
    """Query param yaz — hem `<a href>` navigasyonunda hem sayfa yenilenmesinde
    seçilen dil korunur. `tr` default olduğundan URL'yi temiz tutmak için
    bu durumda param silinir."""
    try:
        if code == DEFAULT_LANG:
            if "lang" in st.query_params:
                del st.query_params["lang"]
        else:
            if st.query_params.get("lang") != code:
                st.query_params["lang"] = code
    except Exception:
        pass


def get_lang() -> str:
    v = st.session_state.get("app_lang")
    if isinstance(v, str) and v in _LANG_CODES:
        return v
    # Session state boşsa query param ile senkronla (ör. başka sayfadan link ile
    # gelinmişse).
    try:
        q = st.query_params.get("lang")
        if isinstance(q, str) and q in _LANG_CODES:
            st.session_state["app_lang"] = q
            return q
    except Exception:
        pass
    return DEFAULT_LANG


def set_lang(code: str) -> None:
    if code in _LANG_CODES:
        st.session_state["app_lang"] = code
        _sync_query_param(code)


def lang_query_suffix(leading: str = "?") -> str:
    """Navigasyon linkleri için `?lang=fr` tarzı ek. TR default olduğunda boş
    string döner — URL temiz kalır."""
    code = get_lang()
    if code == DEFAULT_LANG:
        return ""
    return f"{leading}lang={code}"


def lang_meta(code: str) -> tuple[str, str]:
    for c, name, flag in LANGUAGES:
        if c == code:
            return name, flag
    return code, ""


def t(key: str, default: str | None = None, **kwargs) -> str:
    lang = get_lang()
    entry = STRINGS.get(key)
    val: str | None = None
    if entry:
        val = entry.get(lang) or entry.get(DEFAULT_LANG)
    if val is None:
        val = default if default is not None else key
    if kwargs:
        try:
            val = val.format(**kwargs)
        except Exception:
            pass
    return val
