"""
Примеры raw SQL запросов с SQLAlchemy (синхронная версия)
Демонстрация выполнения чистого SQL через SQLAlchemy engine
"""
from sqlalchemy import text
from sqlalchemy_examples.sync.models import get_engine, get_session, User, Post, init_db, drop_db


def example_1_basic_select():
    """Пример 1: Базовые SELECT запросы"""
    print("\n=== Пример 1: Базовые SELECT запросы ===\n")
    
    engine = get_engine()
    with engine.connect() as conn:
        # Простой SELECT
        result = conn.execute(text("SELECT * FROM users"))
        users = result.fetchall()
        print(f"✓ Всего пользователей: {len(users)}")
        for user in users:
            print(f"  - {user.username} ({user.email})")
        
        # SELECT с WHERE
        result = conn.execute(
            text("SELECT * FROM users WHERE username = :username"),
            {"username": "john_doe"}
        )
        user = result.fetchone()
        print(f"\n✓ Найден пользователь: {user.username}")
        
        # SELECT с LIKE
        result = conn.execute(
            text("SELECT username, email FROM users WHERE email LIKE :pattern"),
            {"pattern": "%example.com"}
        )
        users = result.fetchall()
        print(f"\n✓ Пользователи с email *@example.com:")
        for user in users:
            print(f"  - {user.username}: {user.email}")


def example_2_insert_update_delete():
    """Пример 2: INSERT, UPDATE, DELETE"""
    print("\n=== Пример 2: INSERT, UPDATE, DELETE ===\n")
    
    engine = get_engine()
    with engine.connect() as conn:
        # INSERT
        result = conn.execute(
            text("""
                INSERT INTO users (username, email, full_name, created_at)
                VALUES (:username, :email, :full_name, NOW())
                RETURNING id, username
            """),
            {
                "username": "alice_raw",
                "email": "alice@example.com",
                "full_name": "Alice from Raw SQL"
            }
        )
        conn.commit()
        new_user = result.fetchone()
        print(f"✓ Создан пользователь: {new_user.username} (id={new_user.id})")
        
        # UPDATE
        result = conn.execute(
            text("""
                UPDATE users 
                SET full_name = :new_name
                WHERE username = :username
                RETURNING id, username, full_name
            """),
            {
                "username": "alice_raw",
                "new_name": "Alice Updated via Raw SQL"
            }
        )
        conn.commit()
        updated = result.fetchone()
        print(f"✓ Обновлен: {updated.username} -> {updated.full_name}")
        
        # DELETE
        result = conn.execute(
            text("DELETE FROM users WHERE username = :username RETURNING id"),
            {"username": "alice_raw"}
        )
        conn.commit()
        deleted_id = result.scalar()
        print(f"✓ Удален пользователь с id={deleted_id}")


def example_3_joins():
    """Пример 3: JOIN запросы"""
    print("\n=== Пример 3: JOIN запросы ===\n")
    
    engine = get_engine()
    with engine.connect() as conn:
        # INNER JOIN - посты с авторами
        result = conn.execute(text("""
            SELECT 
                p.id,
                p.title,
                p.views,
                u.username as author
            FROM posts p
            INNER JOIN users u ON p.author_id = u.id
            ORDER BY p.created_at DESC
        """))
        posts = result.fetchall()
        print(f"✓ Посты с авторами:")
        for post in posts:
            print(f"  - '{post.title}' by {post.author} ({post.views} views)")
        
        # LEFT JOIN - пользователи и количество их постов
        result = conn.execute(text("""
            SELECT 
                u.username,
                u.email,
                COUNT(p.id) as post_count
            FROM users u
            LEFT JOIN posts p ON u.id = p.author_id
            GROUP BY u.id, u.username, u.email
            ORDER BY post_count DESC
        """))
        users_stats = result.fetchall()
        print(f"\n✓ Статистика постов по пользователям:")
        for stat in users_stats:
            print(f"  - {stat.username}: {stat.post_count} постов")


def example_4_aggregations():
    """Пример 4: Агрегации и группировки"""
    print("\n=== Пример 4: Агрегации ===\n")
    
    engine = get_engine()
    with engine.connect() as conn:
        # COUNT, AVG, MAX, MIN
        result = conn.execute(text("""
            SELECT 
                COUNT(*) as total_posts,
                AVG(views) as avg_views,
                MAX(views) as max_views,
                MIN(views) as min_views
            FROM posts
        """))
        stats = result.fetchone()
        print(f"✓ Статистика постов:")
        print(f"  - Всего: {stats.total_posts}")
        print(f"  - Средние просмотры: {stats.avg_views:.2f}")
        print(f"  - Максимум: {stats.max_views}")
        print(f"  - Минимум: {stats.min_views}")
        
        # GROUP BY с HAVING
        result = conn.execute(text("""
            SELECT 
                u.username,
                COUNT(p.id) as post_count,
                SUM(p.views) as total_views
            FROM users u
            INNER JOIN posts p ON u.id = p.author_id
            GROUP BY u.id, u.username
            HAVING COUNT(p.id) > 1
            ORDER BY total_views DESC
        """))
        active_authors = result.fetchall()
        print(f"\n✓ Активные авторы (>1 поста):")
        for author in active_authors:
            print(f"  - {author.username}: {author.post_count} постов, {author.total_views} просмотров")


def example_5_subqueries():
    """Пример 5: Подзапросы"""
    print("\n=== Пример 5: Подзапросы ===\n")
    
    engine = get_engine()
    with engine.connect() as conn:
        # Подзапрос в WHERE
        result = conn.execute(text("""
            SELECT username, email
            FROM users
            WHERE id IN (
                SELECT DISTINCT author_id 
                FROM posts 
                WHERE views > 0
            )
        """))
        authors = result.fetchall()
        print(f"✓ Авторы с просмотренными постами:")
        for author in authors:
            print(f"  - {author.username}")
        
        # Подзапрос в SELECT
        result = conn.execute(text("""
            SELECT 
                u.username,
                u.email,
                (SELECT COUNT(*) FROM posts WHERE author_id = u.id) as post_count,
                (SELECT COUNT(*) FROM comments WHERE author_id = u.id) as comment_count
            FROM users u
            ORDER BY post_count DESC
        """))
        user_activity = result.fetchall()
        print(f"\n✓ Активность пользователей:")
        for user in user_activity:
            print(f"  - {user.username}: {user.post_count} постов, {user.comment_count} комментариев")


def example_6_transactions():
    """Пример 6: Транзакции"""
    print("\n=== Пример 6: Транзакции ===\n")
    
    engine = get_engine()
    
    # Успешная транзакция
    print("• Успешная транзакция:")
    with engine.begin() as conn:  # автоматический commit
        result = conn.execute(
            text("INSERT INTO users (username, email, created_at) VALUES (:u, :e, NOW()) RETURNING id"),
            {"u": "trans_user", "e": "trans@example.com"}
        )
        user_id = result.scalar()
        
        conn.execute(
            text("INSERT INTO posts (title, content, author_id, views, created_at) VALUES (:t, :c, :a, 0, NOW())"),
            {"t": "Transaction Post", "c": "Content", "a": user_id}
        )
        print(f"  ✓ Создан пользователь и пост в одной транзакции")
    
    # Откат транзакции при ошибке
    print("\n• Транзакция с откатом:")
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO users (username, email, created_at) VALUES (:u, :e, NOW())"),
                {"u": "will_rollback", "e": "rollback@example.com"}
            )
            # Намеренная ошибка - дублирование username
            conn.execute(
                text("INSERT INTO users (username, email, created_at) VALUES (:u, :e, NOW())"),
                {"u": "trans_user", "e": "duplicate@example.com"}  # trans_user уже существует
            )
    except Exception as e:
        print(f"  ✓ Транзакция откачена из-за ошибки (как и ожидалось)")
    
    # Проверка что will_rollback не создался
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT COUNT(*) FROM users WHERE username = :u"),
            {"u": "will_rollback"}
        )
        count = result.scalar()
        print(f"  ✓ Пользователь 'will_rollback' не создан: {count == 0}")


def seed_data():
    """Заполнение БД тестовыми данными для примеров"""
    with get_session() as session:
        # Создаем пользователей через ORM
        john = User(username="john_doe", email="john@example.com", full_name="John Doe")
        jane = User(username="jane_smith", email="jane@example.com", full_name="Jane Smith")
        session.add_all([john, jane])
        session.commit()
        
        # Создаем посты через ORM
        posts_data = [
            Post(title="First Post", content="Content 1", author=john, views=10),
            Post(title="Second Post", content="Content 2", author=john, views=5),
            Post(title="Jane's Post", content="Content 3", author=jane, views=15),
        ]
        session.add_all(posts_data)
        session.commit()
        
        print("✓ Тестовые данные созданы\n")


def main():
    """Запуск всех примеров"""
    print("\n" + "="*60)
    print("SQLAlchemy Raw SQL - Синхронные примеры")
    print("="*60)
    
    # Пересоздаем БД и заполняем данными
    drop_db()
    init_db()
    seed_data()
    
    # Запускаем примеры
    example_1_basic_select()
    example_2_insert_update_delete()
    example_3_joins()
    example_4_aggregations()
    example_5_subqueries()
    example_6_transactions()
    
    print("\n" + "="*60)
    print("✓ Все примеры выполнены успешно!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()