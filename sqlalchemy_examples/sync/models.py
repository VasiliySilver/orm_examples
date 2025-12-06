from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, Numeric, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from config import SYNC_DATABASE_URL, ECHO_SQL


class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""
    pass


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    
    # Relationships
    posts: Mapped[List["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"User(id={self.id}, username='{self.username}', email='{self.email}')"


class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    views: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.now(timezone.utc))
    
    # Relationships
    author: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"Post(id={self.id}, title='{self.title}', author_id={self.author_id})"


class Comment(Base):
    __tablename__ = "comments"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    
    # Relationships
    post: Mapped["Post"] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship(back_populates="comments")
    
    def __repr__(self) -> str:
        return f"Comment(id={self.id}, post_id={self.post_id}, author_id={self.author_id})"


# Утилиты для работы с БД
def get_engine():
    """Создание синхронного engine"""
    return create_engine(SYNC_DATABASE_URL, echo=ECHO_SQL)


def init_db():
    """Инициализация БД - создание всех таблиц"""
    engine = get_engine()
    Base.metadata.create_all(engine)
    print("✓ База данных инициализирована")


def drop_db():
    """Удаление всех таблиц"""
    engine = get_engine()
    Base.metadata.drop_all(engine)
    print("✓ Все таблицы удалены")


def get_session() -> Session:
    """Получение сессии для работы с БД"""
    engine = get_engine()
    return Session(engine)


if __name__ == "__main__":
    # Пересоздание БД
    drop_db()
    init_db()