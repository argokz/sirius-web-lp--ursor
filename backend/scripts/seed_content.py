import sys
import os
from sqlalchemy.orm import Session

# Добавляем корневой путь проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal
from app.models.page import Page, Section
from app.models.content import ContentItem
from app.models.seo import SEOMetadata

def seed_data():
    db = SessionLocal()
    try:
        # 1. Очистка старых данных (опционально, но лучше для чистого сида)
        # db.query(ContentItem).delete()
        # db.query(Section).delete()
        # db.query(Page).delete()
        # db.commit()

        # 2. Создание страниц
        pages_data = [
            {"slug": "home", "title": "Главная"},
            {"slug": "modeling", "title": "Моделирование и расчеты"},
            {"slug": "gis", "title": "Паспортизация и ГИС"},
            {"slug": "maintenance", "title": "Эксплуатация и Ремонты"},
            {"slug": "web-version", "title": "Web-версия"},
        ]

        for p_data in pages_data:
            page = db.query(Page).filter(Page.slug == p_data["slug"]).first()
            if not page:
                page = Page(**p_data)
                db.add(page)
                db.commit()
                db.refresh(page)
            
            # Добавляем SEO
            seo = db.query(SEOMetadata).filter(SEOMetadata.page_id == page.id).first()
            if not seo:
                seo = SEOMetadata(
                    page_id=page.id,
                    title=f"{page.title} - Сириус ТГИД-07",
                    description=f"Инновационная система управления теплоснабжением ТГИД-07. {page.title}.",
                    keywords="ТГИД-07, теплоснабжение, АСУП, Сириус, гидравлика"
                )
                db.add(seo)

        db.commit()

        # 3. Наполнение контентом (Пример для Главной)
        home_page = db.query(Page).filter(Page.slug == "home").first()
        if home_page:
            content_items = [
                {"content_key": "hero_title", "content_value": "АСУП ТГИД-07 SQL — Цифровизация и эффективность систем теплоснабжения", "content_type": "title"},
                {"content_key": "hero_subtitle", "content_value": "Единый информационный комплекс для расчетов, паспортизации и управления эксплуатацией тепловых сетей любого масштаба", "content_type": "text"},
                {"content_key": "about_text", "content_value": "АСУП ТГИД-07 SQL — это мощная платформа на базе Microsoft SQL Server, объединяющая задачи производственно-технических служб, диспетчерских и инженеров-расчетчиков. Мы предлагаем не просто программу для расчета гидравлики, а полноценный инструмент управления жизненным циклом теплосети: от создания цифровой модели до планирования ремонтных кампаний и анализа аварийности.", "content_type": "text"},
            ]
            for c_data in content_items:
                item = db.query(ContentItem).filter(ContentItem.page_id == home_page.id, ContentItem.content_key == c_data["content_key"]).first()
                if not item:
                    item = ContentItem(page_id=home_page.id, **c_data)
                    db.add(item)
        
        # Моделирование
        modeling_page = db.query(Page).filter(Page.slug == "modeling").first()
        if modeling_page:
           content_items = [
                {"content_key": "page_title", "content_value": "Высокоточные теплогидравлические расчеты и наладка режимов", "content_type": "title"},
                {"content_key": "intro_text", "content_value": "Сердце системы — модуль создания математической модели тепловой сети. Он позволяет моделировать поведение системы в любых условиях, рассчитывать дроссельные устройства и находить причины 'недотопов' или перерасхода энергии.", "content_type": "text"},
            ]
           for c_data in content_items:
                item = db.query(ContentItem).filter(ContentItem.page_id == modeling_page.id, ContentItem.content_key == c_data["content_key"]).first()
                if not item:
                    item = ContentItem(page_id=modeling_page.id, **c_data)
                    db.add(item)

        db.commit()
        print("База данных успешно наполнена контентом!")

    except Exception as e:
        print(f"Ошибка при сидировании: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
