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
        "tr": "Mağaza araması / paket / ID / link",
        "en": "Store search / package / ID / link",
        "es": "Búsqueda / paquete / ID / enlace",
        "de": "Suche / Paket / ID / Link",
        "fr": "Recherche / package / ID / lien",
        "ar": "بحث / حزمة / معرف / رابط",
        "zh": "搜索 / 包名 / ID / 链接",
        "ru": "Поиск / пакет / ID / ссылка",
        "pt": "Busca / pacote / ID / link",
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
    "footer.developed_by": {
        "tr": "geliştiren: cem evecen", "en": "developer: cem evecen",
        "es": "desarrollador: cem evecen", "de": "Entwickler: cem evecen",
        "fr": "développeur : cem evecen", "ar": "المطور: جيم إيڤجن",
        "zh": "开发者：cem evecen", "ru": "разработчик: cem evecen",
        "pt": "desenvolvedor: cem evecen",
    },
}


def get_lang() -> str:
    v = st.session_state.get("app_lang")
    if isinstance(v, str) and v in _LANG_CODES:
        return v
    return DEFAULT_LANG


def set_lang(code: str) -> None:
    if code in _LANG_CODES:
        st.session_state["app_lang"] = code


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
