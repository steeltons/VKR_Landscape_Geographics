from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import User
from models.users_model import *
from utils import get_db_connection
router = APIRouter()


@router.get("/users/one", tags=["UserController"])
async def users_get_one_user(user_id: int):
    """
      Описание: получение данных об одном пользователе по его ID (кроме картинки).
    """
    conn = get_db_connection()
    x = get_one_user(conn, user_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: пользователь с данным ID не найден.")
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/users/onewithoutpassword", tags=["UserController"])
async def users_get_one_user_without_password(user_id: int):
    """
      Описание: получение данных об одном пользователе по его ID (кроме картинки и пароля).
    """
    conn = get_db_connection()
    x = get_one_user_without_password(conn, user_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: пользователь с данным ID не найден.")
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)


@router.post("/users/authorisation/", tags=["UserController"])
async def users_post_authorisation(user: User.UserAuthorization):
    """
      Описание: авторизация. На ввод подаются логин и пароль.
      Если пользователь с такими логином и паролем есть в системе, то возвращается его ID, иначе выводится ошибка.
    """
    conn = get_db_connection()
    x = authorisation(conn, user.user_login, user.user_password)
    if len(x) == 0:
        raise HTTPException(status_code=401, detail="Ошибка: неправильный логин или пароль.")
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/users/all", tags=["UserController"])
async def users_get_select_all():
    """
      Описание: получение данных обо всех пользователях.
    """
    conn = get_db_connection()
    x = get_users(conn)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/users/allwithoutpassword", tags=["UserController"])
async def users_get_select_all_without_password():
    """
      Описание: получение данных обо всех пользователях (кроме паролей).
    """
    conn = get_db_connection()
    x = get_users_without_password(conn)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/users/allwithoutpasswordadmins", tags=["UserController"])
async def users_get_select_all_without_password_admins():
    """
      Описание: получение данных обо всех пользователях-администраторах (кроме паролей).
    """
    conn = get_db_connection()
    x = get_users_without_password_admins(conn)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/users/allwithoutpasswordnoadmins", tags=["UserController"])
async def users_get_select_all_without_password_noadmins():
    """
      Описание: получение данных обо всех пользователях, которые не являются администраторами (кроме паролей).
    """
    conn = get_db_connection()
    x = get_users_without_password_noadmins(conn)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.post("/users/delete", tags=["UserController"])
async def users_post_delete(user_id: int):
    """
      Описание: удаление пользователя по его ID.
    """
    conn = get_db_connection()
    y = get_one_user(conn, user_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: пользователь с данным ID не найден, потому удалить его невозможно.")
    x = delete_user(conn, user_id)
    return Response("{'messdelete':'Пользователь удалён.'}", status_code=200)

@router.post("/users/insert", tags=["UserController"])
async def users_post_insert(user: User.UserRegister):
    """
      Описание: добавление пользователя. На ввод подаются логин, пароль и электронная почта.
      Ограничения: 1) логин пользователя должен иметь длину не более 20 символов и не быть пустым;
                   2) пароль пользователя должен иметь длину не более 20 символов и не быть пустым;
                   3) электронная почта пользователя должна иметь длину не более 30 символов, и содержать символ @, и не быть пустой;
                   4) логин пользователя должен быть уникален (повторы не допускаются);
                   5) электронная почта пользователя должна быть уникальна (повторы не допускаются).
    """
    conn = get_db_connection()
    if ((len(user.user_login) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: логин пользователя не должен быть пустым.")
    if ((len(user.user_password) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: пароль пользователя не должен быть пустым.")
    if ((len(user.user_email) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: электронная почта пользователя не должна быть пустой.")
    if ((len(user.user_login) > 20)):
        raise HTTPException(status_code=400, detail="Ошибка: логин пользователя должен иметь длину не более 20 символов.")
    if ((len(user.user_password) > 20)):
        raise HTTPException(status_code=400, detail="Ошибка: пароль пользователя должен иметь длину не более 20 символов.")
    if ((len(user.user_email) > 30) or (not('@' in user.user_email))):
        raise HTTPException(status_code=400, detail="Ошибка: электронная почта пользователя должна иметь длину не более 30 символов и содержать символ @.")
    y = find_user_login(conn, user.user_login)
    if len(y) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: пользователь с таким логином уже есть в системе. Введите другой логин.")
    z = find_user_email(conn, user.user_email)
    if len(z) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: на эту электронную почту уже был зарегистрирован аккаунт пользователя. Введите другую электронную почту.")
    x = insert_user(conn, user.user_login, user.user_password, user.user_email)
    return Response("{'messinsert':'Пользователь зарегистрирован.'}", status_code=200)

@router.post("/users/update/login", tags=["UserController"])
async def users_post_update_login(user_id: int, user_login: str):
    """
      Описание: изменение логина пользователя.
      Ограничения: 1) логин пользователя должен иметь длину не более 20 символов и не быть пустым;
                   2) логин пользователя должен быть уникален (повторы не допускаются).
    """
    conn = get_db_connection()
    if ((len(user_login) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: логин пользователя не должен быть пустым.")
    if ((len(user_login) > 20)):
        raise HTTPException(status_code=400, detail="Ошибка: логин пользователя должен иметь длину не более 20 символов.")
    y = find_user_login(conn, user_login)
    if len(y) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: пользователь с таким логином уже есть в системе. Введите другой логин.")
    x = update_user_login(conn, user_id, user_login)
    return Response("{'messlogin':'Логин пользователя обновлён.'}", status_code=200)

@router.post("/users/update/password", tags=["UserController"])
async def users_post_update_password(user_id: int, user_password: str):
    """
      Описание: изменение пароля пользователя.
      Ограничения: пароль пользователя должен иметь длину не более 20 символов и не быть пустым;
    """
    conn = get_db_connection()
    if ((len(user_password) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: пароль пользователя не должен быть пустым.")
    if ((len(user_password) > 20)):
        raise HTTPException(status_code=400, detail="Ошибка: пароль пользователя должен иметь длину не более 20 символов.")
    x = update_user_password(conn, user_id, user_password)
    return Response("{'messpassword':'Пароль пользователя обновлён.'}", status_code=200)

@router.post("/users/update/email", tags=["UserController"])
async def users_post_update_email(user_id: int, user_email: str):
    """
      Описание: изменение электронной почты пользователя.
      Ограничения: 1) электронная почта пользователя должна иметь длину не более 30 символов, и содержать символ @, и не быть пустой;
                   2) электронная почта пользователя должна быть уникальна (повторы не допускаются).
    """
    conn = get_db_connection()
    if ((len(user_email) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: электронная почта пользователя не должна быть пустой.")
    if ((len(user_email) > 30) or (not('@' in user_email))):
        raise HTTPException(status_code=400, detail="Ошибка: электронная почта пользователя должна иметь длину не более 30 символов и содержать символ @.")
    z = find_user_email(conn, user_email)
    if len(z) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: на эту электронную почту уже был зарегистрирован аккаунт пользователя. Введите другую электронную почту.")
    x = update_user_email(conn, user_id, user_email)
    return Response("{'messemail':'Электронная почта пользователя обновлена.'}", status_code=200)

@router.post("/users/update/surname", tags=["UserController"])
async def users_post_update_surname(user_id: int, user_surname: str):
    """
      Описание: изменение фамилии пользователя.
      Ограничения: длина фамилии пользователя должна быть <= 20 символов.
    """
    conn = get_db_connection()
    if ((len(user_surname) > 20)):
        raise HTTPException(status_code=400, detail="Ошибка: фамилия пользователя должна иметь длину не более 20 символов.")
    x = update_user_surname(conn, user_id, user_surname)
    return Response("{'messsurname':'Фамилия пользователя обновлена.'}", status_code=200)

@router.post("/users/update/name", tags=["UserController"])
async def users_post_update_name(user_id: int, user_name: str):
    """
      Описание: изменение имени пользователя.
      Ограничения: длина имени пользователя должна быть <= 20 символов.
    """
    conn = get_db_connection()
    if ((len(user_name) > 20)):
        raise HTTPException(status_code=400, detail="Ошибка: имя пользователя должно иметь длину не более 20 символов.")
    x = update_user_name(conn, user_id, user_name)
    return Response("{'messname':'Имя пользователя обновлено.'}", status_code=200)

@router.post("/users/update/fathername", tags=["UserController"])
async def users_post_update_fathername(user_id: int, user_fathername: str):
    """
      Описание: изменение отчества пользователя.
      Ограничения: длина отчества пользователя должна быть <= 20 символов.
    """
    conn = get_db_connection()
    if ((len(user_fathername) > 20)):
        raise HTTPException(status_code=400, detail="Ошибка: отчество пользователя должно иметь длину не более 20 символов.")
    x = update_user_fathername(conn, user_id, user_fathername)
    return Response("{'messfathername':'Отчество пользователя обновлено.'}", status_code=200)

@router.post("/users/update/age", tags=["UserController"])
async def users_post_update_age(user_id: int, user_age: int):
    """
      Описание: изменение возраста пользователя.
      Ограничения: возраст пользователя должен принадлежать интервалу [3; 120].
    """
    conn = get_db_connection()
    if ((user_age < 3) or (user_age > 120)):
        raise HTTPException(status_code=400, detail="Ошибка: возраст пользователя должен принадлежать интервалу [3; 120].")
    x = update_user_age(conn, user_id, user_age)
    return Response("{'message':'Возраст пользователя обновлён.'}", status_code=200)

@router.post("/users/update/isFemale", tags=["UserController"])
async def users_post_update_isFemale(user_id: int, user_isFemale: int):
    """
      Описание: изменение пола пользователя.
      Ограничения: пол пользователя может быть только 0 (мужчина) или 1 (женщина).
    """
    conn = get_db_connection()
    if ((user_isFemale < 0) or (user_isFemale > 1)):
        raise HTTPException(status_code=400, detail="Ошибка: пол пользователя может быть только 0 (мужчина) или 1 (женщина).")
    x = update_user_isFemale(conn, user_id, user_isFemale)
    return Response("{'messisFemale':'Обновлён пол пользователя.'}", status_code=200)

@router.post("/users/update/picture", tags=["UserController"])
async def users_post_update_picture(user: User.UserPicture):
    """
      Описание: изменение картинки (аватарки) пользователя.
      Ограничения: длина содержимого файла с картинкой должна быть <= 10000000 символов.
    """
    conn = get_db_connection()
    if ((len(user.user_picture) > 10000000)):
        raise HTTPException(status_code=400, detail="Ошибка: содержимое файла с картинкой должно иметь длину не более 10000000 символов.")
    x = update_user_picture(conn, user.user_id, user.user_picture)
    return Response("{'messpicture':'Картинка пользователя обновлена.'}", status_code=200)

@router.post("/users/update/isAdmin", tags=["UserController"])
async def users_post_update_isAdmin(user_id: int, user_isAdmin: int):
    """
      Описание: изменение статуса пользователя (обычный или администратор).
      Ограничения: пользователь может быть только или обычным (0), или администратором (1).
    """
    conn = get_db_connection()
    if ((user_isAdmin < 0) or (user_isAdmin > 1)):
        raise HTTPException(status_code=400, detail="Ошибка: пользователь может быть только или обычным (0), или администратором (1).")
    x = update_user_isAdmin(conn, user_id, user_isAdmin)
    return Response("{'messisAdmin':'Обновлено, является ли пользователь администратором.'}", status_code=200)

@router.get("/users/get/picture", tags=["UserController"])
async def users_get_picture(user_id: int):
    """
      Описание: получение картинки пользователя.
    """
    conn = get_db_connection()
    y = get_one_user(conn, user_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: пользователь с данным ID не найден, потому получить его картинку невозможно.")
    x = get_user_picture(conn, user_id)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)