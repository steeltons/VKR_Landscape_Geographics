from fastapi import APIRouter, Response, HTTPException
import json
from models.users_model import *
from utils import get_db_connection

router = APIRouter()

user_example = {
    "user_id": 1,
    "user_login": "user1",
    "user_password": "password1",
    "user_email": "user1@example.com",
    "user_surname": "Иванов",
    "user_name": "Иван",
    "user_fathername": "Иванович",
    "user_age": 30,
    "user_is_female": 0,
    "user_is_admin": 1,
    "user_picture_id": 1,
    "user_picture_base64": "base64_encoded_string_for_user"
}


user_list_example = [
    {
        "user_id": 1,
        "user_login": "user1",
        "user_password": "password1",
        "user_email": "user1@example.com",
        "user_surname": "Иванов",
        "user_name": "Иван",
        "user_fathername": "Иванович",
        "user_age": 30,
        "user_is_female": 0,
        "user_is_admin": 1,
        "user_picture_id": 1,
        "user_picture_base64": "base64_encoded_string_for_user"
    },
    {
        "user_id": 2,
        "user_login": "user2",
        "user_password": "password2",
        "user_email": "user2@example.com",
        "user_surname": "Петров",
        "user_name": "Петр",
        "user_fathername": "Петрович",
        "user_age": 25,
        "user_is_female": 0,
        "user_is_admin": 0,
        "user_picture_id": 1,
        "user_picture_base64": "base64_encoded_string_for_user"
    }
]

@router.get("/users/all", tags=["UserController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with pictures": {
                        "value": user_list_example
                    }
                }
            }
        }
    }
})
async def users_get_select_all(is_need_pictures: bool = False):
    """Описание: получение данных обо всех пользователях."""
    conn = get_db_connection()
    x = get_users(conn, is_need_pictures)
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

@router.get("/users/one", tags=["UserController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with picture": {
                        "value": user_example
                    }
                }
            }
        }
    },
    404: {
        "description": "User not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: пользователь с данным ID не найден."}
            }
        }
    }
})
async def users_get_one_user(user_id: int, is_need_pictures: bool = False):
    """Описание: получение данных об одном пользователе по его идентификатору."""
    conn = get_db_connection()
    x = get_one_user(conn, user_id, is_need_pictures)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: пользователь с данным ID не найден.")
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

@router.delete("/users/delete", tags=["UserController"], responses={
    200: {
        "description": "User deleted successfully",
        "content": {
            "application/json": {
                "example": {"message": "Пользователь удалён."}
            }
        }
    },
    404: {
        "description": "User not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: пользователь с данным ID не найден, потому удалить его невозможно."}
            }
        }
    }
})
async def users_delete(user_id: int):
    """Описание: удаление пользователя по его ID."""
    conn = get_db_connection()
    y = get_one_user(conn, user_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: пользователь с данным ID не найден, потому удалить его невозможно.")
    x = delete_user(conn, user_id)
    return Response("{'message':'Пользователь удалён.'}", status_code=200)

@router.post("/users/insert", tags=["UserController"], responses={
    200: {
        "description": "User created successfully",
        "content": {
            "application/json": {
                "example": {"message": "Пользователь создан."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty login": {
                        "value": {"detail": "Ошибка: логин пользователя не должен быть пустым."}
                    },
                    "Login too long": {
                        "value": {"detail": "Ошибка: длина логина должна быть меньше или равна 30 символов."}
                    },
                    "Empty password": {
                        "value": {"detail": "Ошибка: пароль пользователя не должен быть пустым."}
                    },
                    "Empty email": {
                        "value": {"detail": "Ошибка: email пользователя не должен быть пустым."}
                    },
                    "Surname too long": {
                        "value": {"detail": "Ошибка: длина фамилии должна быть меньше или равна 30 символов."}
                    },
                    "Name too long": {
                        "value": {"detail": "Ошибка: длина имени должна быть меньше или равна 30 символов."}
                    },
                    "Fathername too long": {
                        "value": {"detail": "Ошибка: длина отчества должна быть меньше или равна 30 символов."}
                    },
                    "Invalid age": {
                        "value": {"detail": "Ошибка: возраст должен быть больше 0."}
                    },
                    "Invalid picture ID": {
                        "value": {"detail": "Ошибка: идентификатор картинки должен быть больше 0."}
                    },
                    "Duplicate login": {
                        "value": {"detail": "Ошибка: логин должен быть уникальным (повторы не допускаются)."}
                    }
                }
            }
        }
    }
})
async def users_insert(user_login: str, user_password: str, user_email: str, user_surname: str | None = None, user_name: str | None = None, user_fathername: str | None = None, user_age: int | None = None, user_is_female: int | None = None, user_is_admin: int | None = None, user_picture_id: int | None = None):
    """Описание: добавление пользователя. На ввод подаются логин, пароль, email, фамилия, имя, отчество, возраст, пол, статус администратора и идентификатор картинки."""
    conn = get_db_connection()
    if user_login is not None and len(user_login) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: логин пользователя не должен быть пустым.")
    if user_login is not None and len(user_login) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина логина должна быть меньше или равна 30 символов.")
    if user_password is not None and len(user_password) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: пароль пользователя не должен быть пустым.")
    if user_email is not None and len(user_email) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: email пользователя не должен быть пустым.")
    if user_surname is not None and len(user_surname) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина фамилии должна быть меньше или равна 30 символов.")
    if user_name is not None and len(user_name) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина имени должна быть меньше или равна 30 символов.")
    if user_fathername is not None and len(user_fathername) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина отчества должна быть меньше или равна 30 символов.")
    if user_age is not None and user_age < 0:
        raise HTTPException(status_code=400, detail="Ошибка: возраст должен быть больше 0.")
    if user_picture_id is not None and user_picture_id < 0:
        raise HTTPException(status_code=400, detail="Ошибка: идентификатор картинки должен быть больше 0.")
    if len(find_user_login(conn, user_login)) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: логин должен быть уникальным (повторы не допускаются).")
    x = insert_user(conn, user_login, user_password, user_email, user_surname, user_name, user_fathername, user_age, user_is_female, user_is_admin, user_picture_id)
    return Response("{'message':'Пользователь создан.'}", status_code=200)

@router.patch("/users/update", tags=["UserController"], responses={
    200: {
        "description": "User updated successfully",
        "content": {
            "application/json": {
                "example": {"message": "Пользователь обновлён."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty login": {
                        "value": {"detail": "Ошибка: логин пользователя не должен быть пустым."}
                    },
                    "Login too long": {
                        "value": {"detail": "Ошибка: длина логина должна быть меньше или равна 30 символов."}
                    },
                    "Empty password": {
                        "value": {"detail": "Ошибка: пароль пользователя не должен быть пустым."}
                    },
                    "Empty email": {
                        "value": {"detail": "Ошибка: email пользователя не должен быть пустым."}
                    },
                    "Surname too long": {
                        "value": {"detail": "Ошибка: длина фамилии должна быть меньше или равна 30 символов."}
                    },
                    "Name too long": {
                        "value": {"detail": "Ошибка: длина имени должна быть меньше или равна 30 символов."}
                    },
                    "Fathername too long": {
                        "value": {"detail": "Ошибка: длина отчества должна быть меньше или равна 30 символов."}
                    },
                    "Invalid age": {
                        "value": {"detail": "Ошибка: возраст должен быть больше 0."}
                    },
                    "Invalid picture ID": {
                        "value": {"detail": "Ошибка: идентификатор картинки должен быть больше 0."}
                    },
                    "Duplicate login": {
                        "value": {"detail": "Ошибка: логин должен быть уникальным (повторы не допускаются)."}
                    }
                }
            }
        }
    }
})
async def users_update(user_id: int, user_login: str | None = None, user_password: str | None = None, user_email: str | None = None, user_surname: str | None = None, user_name: str | None = None, user_fathername: str | None = None, user_age: int | None = None, user_is_female: int | None = None, user_is_admin: int | None = None, user_picture_id: int | None = None):
    """Описание: изменение параметров пользователя. На ввод подаются идентификатор, логин, пароль, email, фамилия, имя, отчество, возраст, пол, статус администратора и идентификатор картинки."""
    conn = get_db_connection()
    if user_login is not None and len(user_login) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: логин пользователя не должен быть пустым.")
    if user_login is not None and len(user_login) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина логина должна быть меньше или равна 30 символов.")
    if user_password is not None and len(user_password) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: пароль пользователя не должен быть пустым.")
    if user_email is not None and len(user_email) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: email пользователя не должен быть пустым.")
    if user_surname is not None and len(user_surname) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина фамилии должна быть меньше или равна 30 символов.")
    if user_name is not None and len(user_name) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина имени должна быть меньше или равна 30 символов.")
    if user_fathername is not None and len(user_fathername) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина отчества должна быть меньше или равна 30 символов.")
    if user_age is not None and user_age < 0:
        raise HTTPException(status_code=400, detail="Ошибка: возраст должен быть больше 0.")
    if user_picture_id is not None and user_picture_id < 0:
        raise HTTPException(status_code=400, detail="Ошибка: идентификатор картинки должен быть больше 0.")
    if len(find_user_login_with_id(conn, user_id, user_login)) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: логин должен быть уникальным (повторы не допускаются).")
    x = update_user(conn, user_id, user_login, user_password, user_email, user_surname, user_name, user_fathername, user_age, user_is_female, user_is_admin, user_picture_id)
    return Response("{'message':'Пользователь обновлён.'}", status_code=200)
