from fastapi import FastAPI, Body, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SessionType
from create_db import Users, Posts

engine = create_engine("sqlite:///./laborator_9.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["Начальная страница"])
def start_page():
    return (
        "Добавить юзера - POST /users (в body: username, email, password)",
        "Добавить пост - POST /posts (в body: username, password, title, text)",
    )


@app.post("/users", tags=["Пользователи"])
def add_user(
    username: str = Body(...),
    email: str = Body(...),
    password: str = Body(...),
    db: SessionType = Depends(get_db)
):
    users = db.query(Users).all()
    for user in users:
        if user.username == username:
            return "Данный никнейм уже занят, попробуйте другой"
        elif user.email == email:
            return "Данный email уже занят, попробуйте другой"

    new_user = Users(username=username, email=email, password=password)
    db.add(new_user)
    db.commit()
    return "Пользователь успешно добавлен"


@app.post("/posts", tags=["Посты"])
def add_post(
    username: str = Body(...),
    password: str = Body(...),
    title: str = Body(...),
    text: str = Body(...),
    db: SessionType = Depends(get_db)
):
    user = db.query(Users).filter_by(username=username, password=password).first()
    if user:
        post = Posts(title=title, text=text, user_id=user.id)
        db.add(post)
        db.commit()
        return "Ваша тема успешно добавлена"
    return "Неверно введено имя или пароль"


@app.get("/users", tags=["Пользователи"])
def show_users(db: SessionType = Depends(get_db)):
    users = db.query(Users).all()
    return [f"Имя: {user.username}, email: {user.email}" for user in users]


@app.get("/posts", tags=["Посты"])
def show_posts(db: SessionType = Depends(get_db)):
    posts = db.query(Posts).all()
    users = {user.id: user.username for user in db.query(Users).all()}
    return [
        f"Заголовок: {post.title}, текст: {post.text}, автор: {users.get(post.user_id, 'Неизвестен')}"
        for post in posts
    ]


@app.put("/users/name", tags=["Пользователи"])
def change_name(
    username: str = Body(...),
    new_name: str = Body(...),
    password: str = Body(...),
    db: SessionType = Depends(get_db)
):
    user = db.query(Users).filter_by(username=username).first()
    if user and user.password == password:
        user.username = new_name
        db.commit()
        return HTMLResponse("<h1>Смена произошла удачно</h1>")
    return HTMLResponse("<h1>Что-то пошло не так</h1>")


@app.put("/users/email", tags=["Пользователи"])
def change_email(
    username: str = Body(...),
    new_email: str = Body(...),
    password: str = Body(...),
    db: SessionType = Depends(get_db)
):
    user = db.query(Users).filter_by(username=username).first()
    if user and user.password == password:
        user.email = new_email
        db.commit()
        return HTMLResponse("<h1>Смена произошла удачно</h1>")
    return HTMLResponse("<h1>Что-то пошло не так</h1>")


@app.put("/posts/title", tags=["Посты"])
def change_title(
    title: str = Body(...),
    new_title: str = Body(...),
    password: str = Body(...),
    db: SessionType = Depends(get_db)
):
    post = db.query(Posts).filter_by(title=title).first()
    if post:
        user = db.query(Users).filter_by(id=post.user_id).first()
        if user and user.password == password:
            post.title = new_title
            db.commit()
            return HTMLResponse("<h1>Изменения успешны</h1>")
    return HTMLResponse("<h1>Что-то не так</h1>")


@app.delete("/users/{username}", tags=["Пользователи"])
def delete_user(username: str, db: SessionType = Depends(get_db)):
    user = db.query(Users).filter_by(username=username).first()
    if user:
        posts = db.query(Posts).filter_by(user_id=user.id).all()
        for post in posts:
            db.delete(post)
        db.delete(user)
        db.commit()
        return HTMLResponse(f"<h1>{username} удалён</h1>")
    return HTMLResponse("<h1>Пользователь не найден</h1>")


@app.delete("/posts/{title}", tags=["Посты"])
def delete_post(title: str, db: SessionType = Depends(get_db)):
    post = db.query(Posts).filter_by(title=title).first()
    if post:
        db.delete(post)
        db.commit()
        return "Пост удалён"
    return "Пост не найден"