from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import Users, Posts

# SQLite вместо MySQL
engine = create_engine("sqlite:///./laborator_9.db", connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()

def add_user():
    """Добавляет пользователей в таблицу"""
    users = [
        Users(username="Egor", email="egorkrylovv@yandex.ru", password="123123"),
        Users(username="Yasha", email="mops@yandex.ru", password="45354"),
        Users(username="Olga", email="mango@yandex.ru", password="909090")
    ]
    session.add_all(users)
    session.commit()

def add_posts():
    """Добавляет посты в таблицу"""
    users = session.query(Users).all()
    posts = [
        Posts(title="test 1", text="new text 1", user_id=users[0].id),
        Posts(title="test 2", text="new text 2", user_id=users[0].id),
        Posts(title="mango", text="vkusnoye", user_id=users[2].id)
    ]
    session.add_all(posts)
    session.commit()

def show_users():
    """Выводит всех пользователей"""
    users = session.query(Users).all()
    for user in users:
        print(f"id: {user.id}, username: {user.username}, email: {user.email}")

def show_post_authors():
    """Выводит все посты и их авторов"""
    posts = session.query(Posts).all()
    users = {user.id: user.username for user in session.query(Users).all()}
    for post in posts:
        author = users.get(post.user_id, "Неизвестен")
        print(f"Заголовок: {post.title}, текст: {post.text}, Автор: {author}")

def search_by_id(user_id):
    """Поиск постов по ID автора"""
    posts = session.query(Posts).filter(Posts.user_id == user_id).all()
    for post in posts:
        print(f"Юзер: {user_id}, Заголовок: {post.title}, Текст: {post.text}")

def recreate_email(old_email, new_email):
    """Изменение email пользователя"""
    user = session.query(Users).filter(Users.email == old_email).first()
    if user:
        print(f"Ваша старая почта: {old_email}")
        user.email = new_email
        session.commit()
        print(f"Изменена на: {user.email}")
    else:
        print("Пользователь не найден")

def recreate_text(title, new_text):
    """Изменение текста поста по заголовку"""
    post = session.query(Posts).filter(Posts.title == title).first()
    if post:
        print(f"Вы поменяли текст ({post.text})")
        post.text = new_text
        session.commit()
        print(f"Изменено на ({post.text})")
    else:
        print("Пост не найден")

def delete_post(title):
    """Удаление поста по заголовку"""
    post = session.query(Posts).filter(Posts.title == title).first()
    if post:
        print(f"Удаление поста: {post.title}, текст: {post.text}")
        session.delete(post)
        session.commit()
        print("Пост удалён")
    else:
        print("Пост не найден")

def delete_user(username):
    """Удаление пользователя и всех его постов"""
    user = session.query(Users).filter(Users.username == username).first()
    if user:
        posts = session.query(Posts).filter(Posts.user_id == user.id).all()
        for post in posts:
            print(f"Пост {post.title} удалён")
            session.delete(post)
        session.delete(user)
        session.commit()
        print(f"Пользователь {username} удалён")
    else:
        print("Пользователь не найден")

