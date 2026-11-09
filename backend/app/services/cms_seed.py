import json
from sqlalchemy.orm import Session

from app.models.cms import MenuItem, SiteSetting, PageBlock
from app.models.page import Page

DEFAULT_PAGES = [
    ("home", "Главная"),
    ("product", "Продукт"),
    ("modeling", "Моделирование"),
    ("gis", "ГИС"),
    ("maintenance", "Эксплуатация"),
    ("solutions", "Решения"),
    ("features", "Возможности"),
    ("web-version", "Web-версия"),
    ("about", "О компании"),
    ("blog", "Блог"),
    ("contacts", "Контакты"),
    ("demo", "Демо"),
]

DEFAULT_MENU = [
    ("Продукт", "/product", "product", "i-lucide-box", 10),
    ("Возможности", "/features", "features", "i-lucide-layout-grid", 15),
    ("Моделирование", "/modeling", "modeling", "i-lucide-chart-no-axes-combined", 20),
    ("ГИС", "/gis", "gis", "i-lucide-map", 30),
    ("Эксплуатация", "/maintenance", "maintenance", "i-lucide-wrench", 40),
    ("Решения", "/solutions", "solutions", "i-lucide-network", 50),
    ("Web", "/web-version", "web-version", "i-lucide-globe", 60),
    # Справка собирается из инструкции веб-ТГИД (frontend/scripts/sync-manual.mjs), страницы CMS у неё нет.
    ("Документация", "/docs", None, "i-lucide-book-open", 70),
]

DEFAULT_SETTINGS = [
    ("company_name", "ПКФ «Сириус»", "Название компании", "brand", "text"),
    ("product_name", "ТГИД-07", "Название продукта", "brand", "text"),
    ("contact_email", "info@itwin.kz", "Email", "contacts", "email"),
    ("contact_phone", "", "Телефон", "contacts", "phone"),
    ("contact_address", "", "Адрес", "contacts", "textarea"),
    ("telegram_url", "", "Telegram", "contacts", "url"),
    ("whatsapp_url", "", "WhatsApp", "contacts", "url"),
    (
        "footer_text",
        "ТГИД-07 — профессиональный программный комплекс ПКФ «Сириус» для цифрового моделирования, паспортизации и предиктивного управления тепловыми сетями.",
        "Текст в подвале",
        "content",
        "textarea",
    ),
    ("google_analytics_id", "", "Google Analytics ID (GA4)", "analytics", "text"),
]

def seed_page_blocks(db: Session, pages_by_slug: dict) -> None:
    # 1. Home
    home_page = pages_by_slug.get("home")
    if home_page and db.query(PageBlock).filter(PageBlock.page_id == home_page.id).count() == 0:
        blocks = [
            PageBlock(
                page_id=home_page.id,
                block_key="home-hero",
                block_type="hero",
                eyebrow="АСУП ТГИД-07 / цифровой контур теплоснабжения",
                title="ТГИД-07: единая платформа управления тепловыми сетями",
                body="Профессиональный комплекс ПКФ «Сириус» для теплогидравлического моделирования, ГИС-паспортизации, диспетчеризации, ТОиР и предиктивной аналитики в корпоративной SQL-среде.",
                payload=json.dumps({
                    "image": "/main-func.webp",
                    "button_text": "Запросить демо",
                    "button_url": "/demo"
                }, ensure_ascii=False),
                sort_order=10,
                is_active=True
            ),
            PageBlock(
                page_id=home_page.id,
                block_key="home-features",
                block_type="cards",
                eyebrow="Ключевые возможности",
                title="Вся инженерная картина в одном продукте",
                payload=json.dumps({
                    "items": [
                        { "icon": "i-lucide-calculator", "title": "Теплогидравлические расчеты", "text": "Плановые, фактические, летние и аварийные режимы с учетом геодезии, температурных графиков и состояния оборудования." },
                        { "icon": "i-lucide-map", "title": "ГИС и паспорта", "text": "Карта сети, тепловые камеры, трубопроводы, арматура, потребители, документы и история изменений в единой базе." },
                        { "icon": "i-lucide-activity", "title": "Эксплуатация и ИСУПА", "text": "Дефекты, опрессовки, шурфовки, коррозия, заявки, ремонтные контуры и аналитика повреждаемости по участкам." },
                        { "icon": "i-lucide-radio-tower", "title": "Диспетчерский контур", "text": "Сравнение телеметрии с расчетной моделью, поиск отклонений, контроль насосных станций и критичных зон." }
                    ]
                }, ensure_ascii=False),
                sort_order=20,
                is_active=True
            ),
            PageBlock(
                page_id=home_page.id,
                block_key="home-outcomes",
                block_type="outcomes",
                eyebrow="Результат внедрения",
                title="Предприятие получает управляемую цифровую модель сети",
                payload=json.dumps({
                    "items": [
                        { "title": "Единая достоверная схема", "text": "Расчетная модель, карта, паспорта и события эксплуатации опираются на один набор данных, поэтому решения не расходятся между отделами." },
                        { "title": "Быстрее диагностика режима", "text": "Инженер видит давление, теплопотери, узкие места и последствия переключений до физического вмешательства в сеть." },
                        { "title": "Планирование ремонтов по фактам", "text": "Дефекты, опрессовки, шурфовки и коррозия превращаются в ремонтные контуры, приоритеты и отчетность." },
                        { "title": "Прозрачность для руководства", "text": "Риски, аварийность, эффект регулировки и состояние активов собираются в понятную управленческую картину." }
                    ]
                }, ensure_ascii=False),
                sort_order=30,
                is_active=True
            ),
            PageBlock(
                page_id=home_page.id,
                block_key="home-space",
                block_type="text",
                eyebrow="Единое пространство",
                title="Данные перестают жить в разных отделах",
                body="ТГИД-07 связывает расчетчиков, диспетчеров, ПТС, ремонтные службы и развитие сети. В одном контуре видны режимы, карта, договорные нагрузки, технические условия, паспорта и история событий.",
                payload=json.dumps({
                    "items": [
                        { "icon": "i-lucide-check", "title": "Плановые режимы", "text": "Расчетные схемы хранятся как сценарии, а не файлы." },
                        { "icon": "i-lucide-check", "title": "Аварийные сценарии", "text": "Моделирование последствий аварий на схеме." },
                        { "icon": "i-lucide-check", "title": "Перспективное развитие", "text": "Анализ роста нагрузок с учетом развития инфраструктуры." }
                    ]
                }, ensure_ascii=False),
                sort_order=40,
                is_active=True
            ),
            PageBlock(
                page_id=home_page.id,
                block_key="home-flow",
                block_type="flow",
                eyebrow="Живая визуализация",
                title="Потоки, режимы и риски видны без перегруза интерфейса",
                body="Анимации построены на SVG и CSS, работают плавно, отключаются при reduced motion и не требуют тяжелых 3D-библиотек. Эффект есть, а производительность остается рабочей.",
                payload=json.dumps({
                    "flow_mode": "horizontal"
                }, ensure_ascii=False),
                sort_order=50,
                is_active=True
            ),
            PageBlock(
                page_id=home_page.id,
                block_key="home-roles",
                block_type="cards",
                eyebrow="АРМ по ролям",
                title="Каждая служба работает в своем сценарии, но с одной базой",
                payload=json.dumps({
                    "items": [
                        { "icon": "i-lucide-gauge", "title": "Служба режимов", "text": "Математическая модель, пьезометрические графики, дросселирующие устройства и анализ отклонений." },
                        { "icon": "i-lucide-building-2", "title": "Перспективное развитие", "text": "Оценка подключений, технические условия, резерв мощности и сценарии роста городской нагрузки." },
                        { "icon": "i-lucide-hard-hat", "title": "Производственная служба", "text": "Инвентаризация, паспортизация камер, магистралей, вводов зданий и оборудования на карте." },
                        { "icon": "i-lucide-wrench", "title": "Ремонтные службы", "text": "Планы ТОиР, дефекты, опрессовки, заявки на устранение аварий и контроль статусов работ." }
                    ]
                }, ensure_ascii=False),
                sort_order=60,
                is_active=True
            ),
            PageBlock(
                page_id=home_page.id,
                block_key="home-impact",
                block_type="metrics",
                eyebrow="Эффективность",
                title="Результаты внедрения в цифрах",
                payload=json.dumps({
                    "items": [
                        { "value": "15-20%", "title": "меньше аварийности", "text": "По оценкам разработчиков, СППР и предиктивная аналитика помогают снизить аварийность за счет раннего выявления зон риска." },
                        { "value": "5-20%", "title": "снижение затрат", "text": "Иерархические расчетные технологии поддерживают оптимизацию генерации тепла и перекачки теплоносителя." },
                        { "value": "0.1 мм", "title": "точность настройки", "text": "Расчет сопел и дроссельных диафрагм позволяет балансировать сопротивление сети до физической установки устройств." }
                    ]
                }, ensure_ascii=False),
                sort_order=70,
                is_active=True
            ),
            PageBlock(
                page_id=home_page.id,
                block_key="home-cta",
                block_type="cta",
                eyebrow="Готовность к запуску",
                title="Готовы увидеть ТГИД-07 в работе?",
                body="Подготовим демонстрацию под вашу структуру сети: режимы, карту, паспорта, дефекты, ремонты и web-доступ для выездных служб.",
                payload=json.dumps({
                    "button_text": "Назначить демо",
                    "button_url": "/demo"
                }, ensure_ascii=False),
                sort_order=80,
                is_active=True
            ),
        ]
        for b in blocks:
            db.add(b)

    # 2. Product
    product_page = pages_by_slug.get("product")
    if product_page and db.query(PageBlock).filter(PageBlock.page_id == product_page.id).count() == 0:
        blocks = [
            PageBlock(
                page_id=product_page.id,
                block_key="product-hero",
                block_type="hero",
                eyebrow="Продукт",
                title="ТГИД-07 как единая платформа управления теплосетью",
                body="АСУП ТГИД-07 от ПКФ «Сириус» объединяет расчетную модель, ГИС, паспортизацию, диспетчеризацию, эксплуатацию и аналитику активов в едином корпоративном контуре.",
                payload=json.dumps({
                    "image": "/main-func.webp",
                    "button_text": "Запросить демо",
                    "button_url": "/demo"
                }, ensure_ascii=False),
                sort_order=10,
                is_active=True
            ),
            PageBlock(
                page_id=product_page.id,
                block_key="product-modules",
                block_type="cards",
                eyebrow="Архитектура",
                title="Модули, которые работают вместе",
                payload=json.dumps({
                    "items": [
                        { "icon": "i-lucide-calculator", "title": "Расчетное ядро", "text": "Плановые, фактические, аварийные и перспективные режимы для крупных магистральных и распределительных сетей." },
                        { "icon": "i-lucide-map", "title": "ГИС-контур", "text": "Координатная карта объектов, онлайн-подложки, поиск по адресам и связанная с геометрией техническая база." },
                        { "icon": "i-lucide-file-check-2", "title": "Паспортизация", "text": "Паспорта трубопроводов, камер, павильонов, арматуры, насосов, компенсаторов, опор, воздушников и дренажей." },
                        { "icon": "i-lucide-radio-tower", "title": "Диспетчеризация", "text": "Сопоставление фактических параметров и расчетной модели, поиск отклонений, анализ скрытых порывов и несанкционированных отборов." },
                        { "icon": "i-lucide-wrench", "title": "Эксплуатация и ремонты", "text": "Дефекты, опрессовки, шурфовки, коррозия, ремонтные контуры, заявки и контроль выполнения работ." },
                        { "icon": "i-lucide-monitor-cog", "title": "Web-доступ и администрирование", "text": "Браузерный доступ к данным, роли пользователей, заявки на демонстрацию, контент и SEO через административный интерфейс." }
                    ]
                }, ensure_ascii=False),
                sort_order=20,
                is_active=True
            ),
            PageBlock(
                page_id=product_page.id,
                block_key="product-inside",
                block_type="text",
                eyebrow="Что внутри",
                title="От графического калькулятора к EAM-системе",
                body="ТГИД-07 развивает расчетное ядро в полноценную автоматизированную систему управления производством. Платформа хранит состояние активов, связывает подразделения и помогает принимать решения до того, как проблема станет аварией.",
                payload=json.dumps({
                    "items": [
                        { "icon": "i-lucide-database", "title": "Единая корпоративная SQL-база", "text": "Расчетные схемы, паспорта, договорные нагрузки, технические условия, дефекты и ремонты не расходятся по разным файлам." },
                        { "icon": "i-lucide-network", "title": "АСУП / АСУД для подразделений", "text": "Служба режимов, диспетчерская, ПТС, ремонтные службы и развитие сети работают с одной картиной, но через свои задачи." },
                        { "icon": "i-lucide-satellite-dish", "title": "Интеграции с SCADA и картами", "text": "Система готова к связке с телеметрией, насосными станциями, Google Maps, OpenStreetMap, Visicom, Excel и AutoCAD." },
                        { "icon": "i-lucide-graduation-cap", "title": "Методология внедрения", "text": "Продукт поддержан учебной программой для операторов ТГИД-07 и инженерными сценариями принятия решений." }
                    ]
                }, ensure_ascii=False),
                sort_order=30,
                is_active=True
            ),
            PageBlock(
                page_id=product_page.id,
                block_key="product-flow",
                block_type="steps",
                eyebrow="Предиктивная эксплуатация",
                title="ИСУПА помогает перейти от реакции к предупреждению",
                payload=json.dumps({
                    "items": [
                        { "title": "Описать активы", "text": "Каждый участок, камера и элемент оборудования получают координаты, параметры, документы и историю." },
                        { "title": "Накопить события", "text": "Дефекты, опрессовки, шурфовки, ремонты и коррозионные данные привязываются к конкретному месту сети." },
                        { "title": "Найти риск", "text": "Аналитика повреждаемости и наработка на отказ выдеруют зоны, где ресурс подходит к критическому порогу." },
                        { "title": "Запланировать работу", "text": "Система помогает сформировать ремонтный контур, заявку, сроки, ответственных и отчетность." }
                    ]
                }, ensure_ascii=False),
                sort_order=40,
                is_active=True
            ),
            PageBlock(
                page_id=product_page.id,
                block_key="product-metrics",
                block_type="metrics",
                eyebrow="Метрики",
                title="Основные характеристики платформы",
                payload=json.dumps({
                    "items": [
                        { "value": "SQL", "title": "корпоративная база", "text": "Подходит для крупных сетей с разделением на магистральные и распределительные уровни." },
                        { "value": "SCADA", "title": "готовность к телеметрии", "text": "Расчетная модель может сравниваться с фактическими параметрами в режиме оперативного контроля." },
                        { "value": "EAM", "title": "управление активами", "text": "Фокус смещается с устранения аварий на прогнозирование, ресурс и планирование обслуживания." }
                    ]
                }, ensure_ascii=False),
                sort_order=50,
                is_active=True
            ),
            PageBlock(
                page_id=product_page.id,
                block_key="product-cta",
                block_type="cta",
                eyebrow="Следующий шаг",
                title="Разберем архитектуру под вашу теплосеть",
                body="Покажем, как связать расчетные схемы, карту, паспорта, диспетчерские данные и ремонтные процессы в единую систему.",
                payload=json.dumps({
                    "button_text": "Запросить демо",
                    "button_url": "/demo"
                }, ensure_ascii=False),
                sort_order=60,
                is_active=True
            )
        ]
        for b in blocks:
            db.add(b)

    # 3. GIS
    gis_page = pages_by_slug.get("gis")
    if gis_page and db.query(PageBlock).filter(PageBlock.page_id == gis_page.id).count() == 0:
        blocks = [
            PageBlock(
                page_id=gis_page.id,
                block_key="gis-hero",
                block_type="hero",
                eyebrow="Паспортизация и ГИС",
                title="Электронная карта тепловой сети с паспортами объектов",
                body="Модуль переводит бумажные архивы в цифровую среду: объект на карте связан с координатами, техническими параметрами, документами, дефектами и историей работ.",
                payload=json.dumps({
                    "image": "/gis_map.webp",
                    "button_text": "Запросить демо",
                    "button_url": "/demo"
                }, ensure_ascii=False),
                sort_order=10,
                is_active=True
            ),
            PageBlock(
                page_id=gis_page.id,
                block_key="gis-features",
                block_type="cards",
                eyebrow="Геоданные",
                title="Вся сеть в понятной геометрии",
                payload=json.dumps({
                    "items": [
                        { "icon": "i-lucide-map-pinned", "title": "Интерактивная карта", "text": "Полная привязка схемы теплоснабжения к координатам местности, городским планам и онлайн-подложкам." },
                        { "icon": "i-lucide-search", "title": "Геобаза и поиск", "text": "Быстрый поиск по адресу, улице, инвентарному номеру, объекту сети или абоненту." },
                        { "icon": "i-lucide-file-stack", "title": "Автоматические паспорта", "text": "Генерация паспортов магистральных и распределительных участков на основе введенных данных." },
                        { "icon": "i-lucide-route", "title": "Связность сети", "text": "Маршруты, границы участков, зависимости камер, вводов и потребителей без разрыва между схемой и базой." },
                        { "icon": "i-lucide-layers-3", "title": "Подложки", "text": "Google Maps, OpenStreetMap, Visicom, спутниковые снимки и растровые планы города." },
                        { "icon": "i-lucide-zap", "title": "Дополнительные сети", "text": "При необходимости можно учитывать ЛЭП, трансформаторы и насосные агрегаты с привязкой к карте." }
                    ]
                }, ensure_ascii=False),
                sort_order=20,
                is_active=True
            ),
            PageBlock(
                page_id=gis_page.id,
                block_key="gis-objects",
                block_type="text",
                eyebrow="Паспорта без ручной сборки",
                title="Карточки объектов становятся техническим реестром сети",
                body="ТГИД-07 хранит не только линии на карте. В базе есть материалы, диаметры, годы прокладки, изоляция, арматура, узлы, камеры, павильоны, насосные агрегаты и связанные документы.",
                payload=json.dumps({
                    "items": [
                        { "icon": "i-lucide-pipeline", "title": "Трубопроводы", "text": "Диаметр, материал, год прокладки, тип прокладки, изоляция, состояние и принадлежность участка." },
                        { "icon": "i-lucide-box", "title": "Камеры и узлы", "text": "Павильоны, колодцы, тепловые камеры и детализация до задвижек, воздушников и дренажей." },
                        { "icon": "i-lucide-cog", "title": "Оборудование", "text": "Компенсаторы, опоры, насосы, регулирующие органы и заводские характеристики в карточках." },
                        { "icon": "i-lucide-file-text", "title": "Документы и схемы", "text": "Схемы узлов, спецификации, паспорта, акты, журналы и связанные эксплуатационные материалы." }
                    ]
                }, ensure_ascii=False),
                sort_order=30,
                is_active=True
            ),
            PageBlock(
                page_id=gis_page.id,
                block_key="gis-capabilities",
                block_type="outcomes",
                eyebrow="Картографический контур",
                title="Инженер быстро находит объект и сразу видит его контекст",
                payload=json.dumps({
                    "items": [
                        { "title": "Переход от карты к паспорту", "text": "Клик по объекту открывает карточку с параметрами, историей, документами и связанными событиями эксплуатации." },
                        { "title": "Работа с городскими планами", "text": "Можно использовать современные онлайн-карты, спутниковые снимки или растровые планы, если предприятие опирается на собственную картографию." },
                        { "title": "Поиск для выездных служб", "text": "Мастер участка быстро находит камеру, адрес или потребителя в поле и видит параметры объекта без звонков в офис." },
                        { "title": "Отчеты из базы", "text": "Паспорта и спецификации формируются автоматически, поэтому данные не нужно заново собирать вручную перед каждой выгрузкой." }
                    ]
                }, ensure_ascii=False),
                sort_order=40,
                is_active=True
            ),
            PageBlock(
                page_id=gis_page.id,
                block_key="gis-cta",
                block_type="cta",
                eyebrow="Следующий шаг",
                title="Покажем пример цифрового паспорта",
                body="Разберем структуру паспортов, карточек объектов, картографических подложек и автоматических отчетов.",
                payload=json.dumps({
                    "button_text": "Запросить демо",
                    "button_url": "/demo"
                }, ensure_ascii=False),
                sort_order=50,
                is_active=True
            )
        ]
        for b in blocks:
            db.add(b)

    # 4. Modeling
    mod_page = pages_by_slug.get("modeling")
    if mod_page and db.query(PageBlock).filter(PageBlock.page_id == mod_page.id).count() == 0:
        blocks = [
            PageBlock(
                page_id=mod_page.id,
                block_key="modeling-hero",
                block_type="hero",
                eyebrow="Моделирование",
                title="Высокоточные теплогидравлические расчеты и наладка режимов",
                body="Сердце ТГИД-07 - математическая модель теплосети. Она показывает поведение системы в плановых, фактических, летних и аварийных условиях до выезда бригады на место.",
                payload=json.dumps({
                    "image": "/modeling_dashboard.webp",
                    "button_text": "Запросить демо",
                    "button_url": "/demo"
                }, ensure_ascii=False),
                sort_order=10,
                is_active=True
            ),
            PageBlock(
                page_id=mod_page.id,
                block_key="modeling-features",
                block_type="cards",
                eyebrow="Расчеты",
                title="Модель, которой можно доверять",
                payload=json.dumps({
                    "items": [
                        { "icon": "i-lucide-git-branch", "title": "Плановый режим", "text": "Расчет идеального состояния сети для настройки дросселирующих устройств, сопел и шайб с учетом нормативных потерь." },
                        { "icon": "i-lucide-activity", "title": "Фактический режим", "text": "Моделирование реальной ситуации с учетом дефектов, отключений, состояния оборудования и ремонтных ограничений." },
                        { "icon": "i-lucide-sun", "title": "Летний режим и ГВС", "text": "Алгоритмы для межотопительного периода, тупиковых и циркуляционных схем горячего водоснабжения." },
                        { "icon": "i-lucide-chart-line", "title": "Пьезометрические графики", "text": "Автоматическое построение графиков давления по выбранному пути с учетом рельефа и статических зон." },
                        { "icon": "i-lucide-thermometer", "title": "Тепловые потери", "text": "Нормативные и фактические потери через изоляцию и утечки с учетом типа прокладки и температуры грунта." },
                        { "icon": "i-lucide-settings-2", "title": "Дросселирующие устройства", "text": "Расчет диаметров сопел и диафрагм до десятых долей миллиметра для балансировки сопротивления сети." }
                    ]
                }, ensure_ascii=False),
                sort_order=20,
                is_active=True
            ),
            PageBlock(
                page_id=mod_page.id,
                block_key="modeling-outcomes",
                block_type="outcomes",
                eyebrow="Инженерный результат",
                title="Расчет отвечает не только «сколько», но и «почему»",
                payload=json.dumps({
                    "items": [
                        { "title": "До изменения режима", "text": "Инженер видит, какие участки ограничивают сеть, где давление выходит за допустимые границы и какие потребители рискуют получить недотоп." },
                        { "title": "После переключения", "text": "Можно заранее проверить последствия вывода участка, изменения насосной группы или изменения нагрузок у абонентов." },
                        { "title": "Для экономического обоснования", "text": "Расчет теплопотерь и режимных отклонений формирует базу для тарифов, инвестиций и программ энергосбережения." },
                        { "title": "Для диспетчера", "text": "Сравнение расчетной модели и фактической телеметрии помогает выявлять скрытые порывы и несанкционированный отбор воды." }
                    ]
                }, ensure_ascii=False),
                sort_order=30,
                is_active=True
            ),
            PageBlock(
                page_id=mod_page.id,
                block_key="modeling-diagnostics",
                block_type="steps",
                eyebrow="Диагностика",
                title="Пьезометрический график показывает режим по профилю сети",
                payload=json.dumps({
                    "items": [
                        { "title": "Выбрать путь", "text": "Маршрут строится по магистрали, распределительной сети или проблемному направлению потребителя." },
                        { "title": "Построить график", "text": "Система автоматически показывает линии статического и динамического давления относительно профиля местности." },
                        { "title": "Найти опасность", "text": "На графике видны зоны вскипания, кавитации, недостаточного напора или превышения допустимых давлений." },
                        { "title": "Принять решение", "text": "Инженер получает основание для настройки, ремонта, изменения схемы или регулирования насосной станции." }
                    ]
                }, ensure_ascii=False),
                sort_order=40,
                is_active=True
            ),
            PageBlock(
                page_id=mod_page.id,
                block_key="modeling-cta",
                block_type="cta",
                eyebrow="Следующий шаг",
                title="Закажите расчет модели",
                body="Покажем плановый и фактический режимы, пьезометрический график, теплопотери и узкие места на ваших исходных данных.",
                payload=json.dumps({
                    "button_text": "Запросить демо",
                    "button_url": "/demo"
                }, ensure_ascii=False),
                sort_order=50,
                is_active=True
            )
        ]
        for b in blocks:
            db.add(b)

    # 5. Maintenance
    maint_page = pages_by_slug.get("maintenance")
    if maint_page and db.query(PageBlock).filter(PageBlock.page_id == maint_page.id).count() == 0:
        blocks = [
            PageBlock(
                page_id=maint_page.id,
                block_key="maintenance-hero",
                block_type="hero",
                eyebrow="Эксплуатация и ремонты",
                title="Управление надежностью: ремонты, опрессовка, дефекты",
                body="АРМ эксплуатационных служб ведет полную историю жизни теплосети, помогает планировать работы, контролировать сроки и видеть аварийность по конкретным участкам.",
                payload=json.dumps({
                    "image": "/maintenance_tablet.webp",
                    "button_text": "Запросить демо",
                    "button_url": "/demo"
                }, ensure_ascii=False),
                sort_order=10,
                is_active=True
            ),
            PageBlock(
                page_id=maint_page.id,
                block_key="maintenance-features",
                block_type="cards",
                eyebrow="Обслуживание",
                title="Цикл работ под контролем",
                payload=json.dumps({
                    "items": [
                        { "icon": "i-lucide-clipboard-list", "title": "План работ", "text": "Сезонные задачи, сроки, ответственные, статусы и контроль выполнения ремонтной программы." },
                        { "icon": "i-lucide-triangle-alert", "title": "Нарушения и дефекты", "text": "Порывы, свищи, неисправности арматуры и другие события фиксируются на карте с классификацией причин." },
                        { "icon": "i-lucide-gauge", "title": "Гидравлические испытания", "text": "Создание контуров опрессовки на схеме, фиксация повреждений и формирование актов и графиков." },
                        { "icon": "i-lucide-hammer", "title": "ТОиР", "text": "Капитальные, текущие и инвестиционные ремонты со статусами «План», «В работе», «Завершено»." },
                        { "icon": "i-lucide-flask-conical", "title": "Коррозионный мониторинг", "text": "Индикаторы коррозии, потеря массы образцов, агрессивность сетевой воды и оценка остаточного ресурса." },
                        { "icon": "i-lucide-chart-no-axes-combined", "title": "Аналитика аварийности", "text": "Статистика повреждаемости, зоны риска, наработка на отказ и приоритеты замены труб до прорыва." }
                    ]
                }, ensure_ascii=False),
                sort_order=20,
                is_active=True
            ),
            PageBlock(
                page_id=maint_page.id,
                block_key="maintenance-outcomes",
                block_type="outcomes",
                eyebrow="От журнала к аналитике",
                title="Каждый дефект получает место, причину и историю устранения",
                payload=json.dumps({
                    "items": [
                        { "title": "Эксплуатация", "text": "Инциденты и нарушения заносятся сразу с привязкой к объекту, участку, дате, источнику и ответственным." },
                        { "title": "Обходы и осмотры", "text": "Полевые замечания не теряются, а попадают в журнал дефектов и становятся частью истории объекта." },
                        { "title": "Опрессовка", "text": "Контуры испытаний создаются на схеме, а найденные повреждения фиксируются в реальном времени." },
                        { "title": "Шурфовки и коррозия", "text": "Результаты обследований и индикаторов помогают прогнозировать износ и планировать замену участков." }
                    ]
                }, ensure_ascii=False),
                sort_order=30,
                is_active=True
            ),
            PageBlock(
                page_id=maint_page.id,
                block_key="maintenance-steps",
                block_type="steps",
                eyebrow="Жизненный цикл работ",
                title="От выявления до закрытия и анализа ресурса",
                payload=json.dumps({
                    "items": [
                        { "title": "Выявить", "text": "Дефект, повреждение или риск создается на карте и связывается с конкретным объектом сети." },
                        { "title": "Запланировать", "text": "Формируется ремонтный контур, сроки, ресурсы, ответственные и приоритет выполнения." },
                        { "title": "Исполнить", "text": "Статусы работ обновляются по ходу выполнения, а документы и акты прикладываются к событию." },
                        { "title": "Проанализировать", "text": "История повреждений показывает повторяемость проблем и помогает корректировать инвестиционную программу." }
                    ]
                }, ensure_ascii=False),
                sort_order=40,
                is_active=True
            ),
            PageBlock(
                page_id=maint_page.id,
                block_key="maintenance-cta",
                block_type="cta",
                eyebrow="Следующий шаг",
                title="Покажем эксплуатационный контур",
                body="Соберем демонстрацию по дефектам, опрессовкам, ремонтным контурам, коррозии и отчетности для руководства.",
                payload=json.dumps({
                    "button_text": "Запросить демо",
                    "button_url": "/demo"
                }, ensure_ascii=False),
                sort_order=50,
                is_active=True
            )
        ]
        for b in blocks:
            db.add(b)

    # 6. Solutions
    sol_page = pages_by_slug.get("solutions")
    if sol_page and db.query(PageBlock).filter(PageBlock.page_id == sol_page.id).count() == 0:
        blocks = [
            PageBlock(
                page_id=sol_page.id,
                block_key="solutions-hero",
                block_type="hero",
                eyebrow="Решения",
                title="Рабочие сценарии для диспетчеров, инженеров и руководителей",
                body="ТГИД-07 помогает разным ролям смотреть на одну сеть через свои задачи: расчеты, ТОиР, карту, аналитику, развитие и отчетность.",
                payload=json.dumps({
                    "button_text": "Запросить демо",
                    "button_url": "/demo"
                }, ensure_ascii=False),
                sort_order=10,
                is_active=True
            ),
            PageBlock(
                page_id=sol_page.id,
                block_key="solutions-roles",
                block_type="cards",
                eyebrow="Роли",
                title="Один продукт для нескольких команд",
                payload=json.dumps({
                    "items": [
                        { "icon": "i-lucide-radio-tower", "title": "Диспетчерская", "text": "Оперативный контроль параметров, отклонений, аварийных зон и переход к проблемному участку на карте." },
                        { "icon": "i-lucide-calculator", "title": "Служба режимов", "text": "Расчеты плановых, фактических, аварийных и летних режимов, настройка насосов и дросселирующих устройств." },
                        { "icon": "i-lucide-map-pinned", "title": "ПТС и паспортизация", "text": "Инвентаризация камер, магистралей, тепловых вводов, арматуры и оборудования с документами." },
                        { "icon": "i-lucide-hard-hat", "title": "Эксплуатация", "text": "Дефекты, обходы, опрессовки, шурфовки, коррозия и история обслуживания объектов сети." },
                        { "icon": "i-lucide-building-2", "title": "Перспективное развитие", "text": "Технические условия, новые подключения, резерв мощности, договорные нагрузки и сценарии роста." },
                        { "icon": "i-lucide-presentation", "title": "Руководство", "text": "Сводные показатели, аварийность, риски, ремонтная программа и экономический эффект в понятной управленческой форме." }
                    ]
                }, ensure_ascii=False),
                sort_order=20,
                is_active=True
            ),
            PageBlock(
                page_id=sol_page.id,
                block_key="solutions-steps",
                block_type="steps",
                eyebrow="Сквозной сценарий",
                title="Решение одной проблемы проходит через все службы",
                payload=json.dumps({
                    "items": [
                        { "title": "Сигнал", "text": "Диспетчер видит отклонение давления, температуры или расхода по контуру." },
                        { "title": "Расчет", "text": "Инженер проверяет фактический режим и строит пьезометрический график." },
                        { "title": "Контекст", "text": "ПТС уточняет паспорт объекта, историю дефектов и текущие ремонтные ограничения." },
                        { "title": "Решение", "text": "Команда планирует работу, фиксирует результат и получает аналитику для следующего цикла." }
                    ]
                }, ensure_ascii=False),
                sort_order=30,
                is_active=True
            ),
            PageBlock(
                page_id=sol_page.id,
                block_key="solutions-cta",
                block_type="cta",
                eyebrow="Следующий шаг",
                title="Соберем сценарий под вашу службу",
                body="Покажем продукт глазами диспетчера, расчетчика, ПТС, ремонтной службы или руководителя.",
                payload=json.dumps({
                    "button_text": "Запросить демо",
                    "button_url": "/demo"
                }, ensure_ascii=False),
                sort_order=40,
                is_active=True
            )
        ]
        for b in blocks:
            db.add(b)

    # 7. Web-version
    web_page = pages_by_slug.get("web-version")
    if web_page and db.query(PageBlock).filter(PageBlock.page_id == web_page.id).count() == 0:
        blocks = [
            PageBlock(
                page_id=web_page.id,
                block_key="web-hero",
                block_type="hero",
                eyebrow="Web-версия",
                title="Доступ к актуальной схеме теплоснабжения из браузера",
                body="Руководители, мастера участков и выездные бригады получают карту, параметры объектов, поиск, режимы и отчеты без тяжелых локальных установок.",
                payload=json.dumps({
                    "image": "/web_access.webp",
                    "button_text": "Запросить демо",
                    "button_url": "/demo"
                }, ensure_ascii=False),
                sort_order=10,
                is_active=True
            ),
            PageBlock(
                page_id=web_page.id,
                block_key="web-access",
                block_type="cards",
                eyebrow="Доступ",
                title="Быстро, безопасно, адаптивно",
                payload=json.dumps({
                    "items": [
                        { "icon": "i-lucide-laptop", "title": "Работа из браузера", "text": "Доступ через Chrome, Safari и другие браузеры без установки тяжелого рабочего места." },
                        { "icon": "i-lucide-tablet-smartphone", "title": "Адаптивность", "text": "Интерфейс сохраняет читаемость и рабочие сценарии на desktop, планшете и мобильном экране." },
                        { "icon": "i-lucide-map-pinned", "title": "Карта и карточки", "text": "Параметры узла, трубы, камеры или потребителя открываются кликом по карте." },
                        { "icon": "i-lucide-search", "title": "Поиск в поле", "text": "Быстрый поиск абонентов, тепловых камер, адресов и объектов сети во время выезда." },
                        { "icon": "i-lucide-chart-line", "title": "Режимы удаленно", "text": "Просмотр пьезометрических графиков, текущих режимов и расчетных результатов без доступа к desktop-клиенту." },
                        { "icon": "i-lucide-lock-keyhole", "title": "Права и SSL", "text": "Разграничение чтения и записи, защищенный обмен данными и администрирование пользователей." }
                    ]
                }, ensure_ascii=False),
                sort_order=20,
                is_active=True
            ),
            PageBlock(
                page_id=web_page.id,
                block_key="web-field",
                block_type="text",
                eyebrow="Работа в поле",
                title="Инженер получает данные там, где находится объект",
                body="Web-версия открывается в Chrome, Safari и других современных браузерах на ПК, планшете или смартфоне. Сотруднику не нужно искать бумажный паспорт или звонить диспетчеру, чтобы уточнить параметры камеры или потребителя.",
                payload=json.dumps({
                    "items": [
                        { "icon": "i-lucide-navigation", "title": "Найти объект", "text": "По адресу, инвентарному номеру, названию камеры, абоненту или участку сети." },
                        { "icon": "i-lucide-mouse-pointer-click", "title": "Открыть параметры", "text": "Открыть характеристики трубы, камеры, потребителя, оборудования и связанные документы." },
                        { "icon": "i-lucide-chart-spline", "title": "Проверить режим", "text": "Посмотреть расчетные параметры и пьезометрические графики перед принятием решения." },
                        { "icon": "i-lucide-send", "title": "Передать действие", "text": "Сформировать обращение, уточнение или задачу для эксплуатационной команды." }
                    ]
                }, ensure_ascii=False),
                sort_order=30,
                is_active=True
            ),
            PageBlock(
                page_id=web_page.id,
                block_key="web-security",
                block_type="outcomes",
                eyebrow="Контроль доступа",
                title="Данные открываются по ролям, а не всем подряд",
                payload=json.dumps({
                    "items": [
                        { "title": "Роли пользователей", "text": "Руководитель, диспетчер, инженер, мастер участка и подрядчик могут видеть разные наборы данных." },
                        { "title": "Чтение и запись", "text": "Для полевых сотрудников можно оставить просмотр, а внесение изменений разрешить только ответственным ролям." },
                        { "title": "Защищенное подключение", "text": "SSL-шифрование и серверная авторизация снижают риск доступа к производственным данным вне контура предприятия." },
                        { "title": "Администрирование сайта", "text": "Пользователи, заявки, контент и SEO управляются из отдельной административной зоны." }
                    ]
                }, ensure_ascii=False),
                sort_order=40,
                is_active=True
            ),
            PageBlock(
                page_id=web_page.id,
                block_key="web-cta",
                block_type="cta",
                eyebrow="Следующий шаг",
                title="Запросите web-демо",
                body="Покажем работу с картой, поиском, карточками объектов, режимами и правами доступа на desktop и мобильном экране.",
                payload=json.dumps({
                    "button_text": "Запросить демо",
                    "button_url": "/demo"
                }, ensure_ascii=False),
                sort_order=50,
                is_active=True
            )
        ]
        for b in blocks:
            db.add(b)

    db.commit()

def seed_cms_defaults(db: Session) -> None:
    pages_by_slug = {}

    for slug, title in DEFAULT_PAGES:
        page = db.query(Page).filter(Page.slug == slug).first()
        if not page:
            page = Page(slug=slug, title=title, is_active=True)
            db.add(page)
            db.flush()
        pages_by_slug[slug] = page

    for title, url, slug, icon, sort_order in DEFAULT_MENU:
        existing = db.query(MenuItem).filter(MenuItem.url == url).first()
        if existing:
            continue

        db.add(
            MenuItem(
                title=title,
                url=url,
                page_id=pages_by_slug.get(slug).id if pages_by_slug.get(slug) else None,
                icon=icon,
                sort_order=sort_order,
                is_active=True,
                is_external=False,
            )
        )

    for key, value, label, group_name, field_type in DEFAULT_SETTINGS:
        existing = db.query(SiteSetting).filter(SiteSetting.key == key).first()
        if existing:
            continue

        db.add(
            SiteSetting(
                key=key,
                value=value,
                label=label,
                group_name=group_name,
                field_type=field_type,
            )
        )

    db.commit()
    seed_page_blocks(db, pages_by_slug)
