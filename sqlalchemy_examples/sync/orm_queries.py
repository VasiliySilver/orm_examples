"""
Примеры ORM запросов с SQLAlchemy (синхронная версия)
Демонстрация различных паттернов работы с ORM
"""
from sqlalchemy import select, func, and_, or_, desc
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy_examples.sync.models import User, Post, Comment, get_session, init_db, drop_db


def example_1_basic_crud():
    """Пример 1: Базовые CRUD операции"""
    print("\n=== Пример 1: Базовые CRUD операции ===\n")
    
    with get_session() as session:
        # CREATE - Создание пользователей
        user1 = User(username="john_doe", email="john@example.com", full_name="John Doe")
        user2 = User(username="jane_smith", email="jane@example.com", full_name="Jane Smith")
        user3 = User(username="bob_wilson", email="bob@example.com", full_name="Bob Wilson")
        
        session.add_all([user1, user2, user3])
        session.commit()
        print(f"✓ Создано 3 пользователя")
        
        # READ - Чтение одного объекта
        user = session.get(User, 1)
        print(f"✓ Получен пользователь: {user}")
        
        # UPDATE - Обновление
        user.full_name = "John Updated Doe"
        session.commit()
        print(f"✓ Обновлен пользователь: {user}")
        
        # DELETE - Удаление
        session.delete(user3)
        session.commit()
        print(f"✓ Удален пользователь bob_wilson")


def example_2_filtering():
    """Пример 2: Фильтрация и поиск"""
    print("\n=== Пример 2: Фильтрация и поиск ===\n")
    
    with get_session() as session:
        # Простой фильтр
        stmt = select(User).where(User.username == "john_doe")
        user = session.execute(stmt).scalar_one()
        print(f"✓ Найден пользователь по username: {user}")
        
        # Фильтр с LIKE
        stmt = select(User).where(User.email.like("%example.com"))
        users = session.execute(stmt).scalars().all()
        print(f"✓ Найдено {len(users)} пользователей с email *@example.com")
        
        # Множественные условия (AND)
        stmt = select(User).where(
            and_(
                User.username.startswith("j"),
                User.email.contains("example")
            )
        )
        users = session.execute(stmt).scalars().all()
        print(f"✓ Найдено {len(users)} пользователей (username начинается с 'j' И email содержит 'example')")
        
        # OR условия
        stmt = select(User).where(
            or_(
                User.username == "john_doe",
                User.username == "jane_smith"
            )
        )
        users = session.execute(stmt).scalars().all()
        print(f"✓ Найдено {len(users)} пользователей (john_doe ИЛИ jane_smith)")


def example_3_relationships():
    """Пример 3: Работа с relationships"""
    print("\n=== Пример 3: Работа с relationships ===\n")
    
    with get_session() as session:
        # Получаем пользователей
        john = session.execute(select(User).where(User.username == "john_doe")).scalar_one()
        jane = session.execute(select(User).where(User.username == "jane_smith")).scalar_one()
        
        # Создаем посты через relationship
        post1 = Post(
            title="First Post by John",
            content="This is my first post!",
            author=john  # Используем relationship
        )
        post2 = Post(
            title="Second Post by John",
            content="Another great post",
            author=john
        )
        post3 = Post(
            title="Jane's Post",
            content="Hello from Jane",
            author=jane
        )
        
        session.add_all([post1, post2, post3])
        session.commit()
        print(f"✓ Создано 3 поста")
        
        # Доступ к связанным объектам
        print(f"✓ Посты John: {len(john.posts)} шт.")
        for post in john.posts:
            print(f"  - {post.title}")


def example_4_eager_loading():
    """Пример 4: Eager loading (оптимизация запросов)"""
    print("\n=== Пример 4: Eager loading ===\n")
    
    with get_session() as session:
        # N+1 проблема (плохо)
        print("• Без eager loading (N+1 проблема):")
        stmt = select(User)
        users = session.execute(stmt).scalars().all()
        for user in users:
            print(f"  {user.username}: {len(user.posts)} постов")  # Каждый раз новый запрос!
        
        # selectinload (хорошо) - отдельный SELECT IN запрос
        print("\n• С selectinload:")
        stmt = select(User).options(selectinload(User.posts))
        users = session.execute(stmt).scalars().all()
        for user in users:
            print(f"  {user.username}: {len(user.posts)} постов")
        
        # joinedload (хорошо) - JOIN в одном запросе
        print("\n• С joinedload:")
        stmt = select(User).options(joinedload(User.posts))
        users = session.execute(stmt).unique().scalars().all()
        for user in users:
            print(f"  {user.username}: {len(user.posts)} постов")


def example_5_aggregations():
    """Пример 5: Агрегации и группировки"""
    print("\n=== Пример 5: Агрегации ===\n")
    
    with get_session() as session:
        # Подсчет постов
        total_posts = session.execute(select(func.count(Post.id))).scalar()
        print(f"✓ Всего постов: {total_posts}")
        
        # Группировка - количество постов по авторам
        stmt = (
            select(User.username, func.count(Post.id).label("post_count"))
            .join(Post, User.id == Post.author_id)
            .group_by(User.id, User.username)
            .order_by(desc("post_count"))
        )
        results = session.execute(stmt).all()
        print(f"✓ Посты по авторам:")
        for username, count in results:
            print(f"  {username}: {count} постов")


def main():
    """Запуск всех примеров"""
    print("\n" + "="*60)
    print("SQLAlchemy ORM - Синхронные примеры")
    print("="*60)
    
    # Пересоздаем БД
    drop_db()
    init_db()
    
    # Запускаем примеры
    example_1_basic_crud()
    example_2_filtering()
    example_3_relationships()
    example_4_eager_loading()
    example_5_aggregations()
    
    print("\n" + "="*60)
    print("✓ Все примеры выполнены успешно!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
