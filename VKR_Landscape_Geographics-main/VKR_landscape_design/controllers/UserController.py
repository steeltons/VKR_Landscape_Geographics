from fastapi import APIRouter, Response, HTTPException
import json
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import timedelta
from typing import Optional
from models.users_model import *
from utils import get_db_connection
from auth import create_access_token, verify_password, SECRET_KEY, ALGORITHM

router = APIRouter()
security = HTTPBearer()

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
    "user_is_admin": 'true',
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
        "user_is_admin": 'true',
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
        "user_is_admin": 'true',
        "user_picture_id": 1,
        "user_picture_base64": "base64_encoded_string_for_user"
    }
]

def get_user_by_login(conn, user_login: str):
    user = pd.read_sql(f'''
        SELECT * FROM users WHERE user_login = "{user_login}"
    ''', conn)
    if not user.empty:
        return user.iloc[0]
    return None

def authenticate_user(conn, user_login: str, user_password: str):
    user = get_user_by_login(conn, user_login)
    if user is None:
        return False
    if not verify_password(user_password, user['user_password']):
        return False
    return user

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    conn = get_db_connection()
    user = get_user_by_login(conn, username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_admin_user(current_user: dict = Depends(get_current_user)):
    print(current_user)
    if not current_user['user_is_admin']:
        raise HTTPException(status_code=403, detail="Ошибка: у вас недостаточно прав для использования данного функционала.")
    return current_user

@router.post("/login", tags=["Authorisation"])
async def login_for_access_token(username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    user = authenticate_user(conn, username, password)
    print(user)
    print(type(user))
    print((type(user) is bool))
    if ((type(user) is bool)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные логин или пароль. Пожалуйста, попробуйте ещё раз.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=300)
    access_token = create_access_token(
        data={"sub": user['user_login'], "is_admin": user['user_is_admin']},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout", tags=["Authorisation"])
async def logout():
    """
    Описание: Метод для выхода пользователя из системы.
    На клиенте необходимо удалить токен из хранилища.
    """
    return {"message": "Вы успешно вышли из системы. Клиентская часть должна удалить токен."}

@router.get("/users/all", tags=["UserController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with pictures": {
                        "value": [user_list_example]
                    }
                }
            }
        }
    },
    400: {
        "description": "Invalid input parameters",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: недопустимые параметры пагинации или поиска."}
            }
        }
    }
})
async def users_get_select_all(
    is_need_pictures: bool = False,
    search_query: str | None = None,
    page: int | None = None,
    elements: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)
):
    """Описание: получение данных обо всех пользователях с поддержкой пагинации и поиска."""
    if page is not None and page < 1:
        raise HTTPException(status_code=400, detail="Ошибка: номер страницы должен быть положительным числом.")
    if elements is not None and elements < 1:
        raise HTTPException(status_code=400, detail="Ошибка: количество объектов на странице должно быть положительным числом.")

    conn = get_db_connection()
    x = get_users(conn, is_need_pictures, search_query, page, elements)
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
    },
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: у вас нет прав для доступа к данным этого пользователя."}
            }
        }
    }
})
async def users_get_one_user(
    user_id: int,
    is_need_pictures: bool = False,
    current_user: dict = Depends(get_current_user)
):
    """Описание: получение данных об одном пользователе по его идентификатору."""
    if not current_user['user_is_admin'] and current_user['user_id'] != user_id:
        raise HTTPException(
            status_code=403,
            detail="Ошибка: у вас нет прав для доступа к данным этого пользователя."
        )

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
    },
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: у вас нет прав для удаления этого пользователя."}
            }
        }
    }
})
async def users_delete(
    user_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Описание: удаление пользователя по его ID."""
    if not current_user['user_is_admin'] and current_user['user_id'] != user_id:
        raise HTTPException(
            status_code=403,
            detail="Ошибка: у вас нет прав для удаления этого пользователя."
        )

    conn = get_db_connection()
    y = get_one_user(conn, user_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: пользователь с данным ID не найден, потому удалить его невозможно.")

    x = delete_user(conn, user_id)
    return Response("{'message':'Пользователь удалён.'}", status_code=200)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):
    return pwd_context.hash(password)


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
async def users_insert(
    user_login: str,
    user_password: str,
    user_email: str,
    user_surname: str | None = None,
    user_name: str | None = None,
    user_fathername: str | None = None,
    user_age: int | None = None,
    user_is_female: int | None = None,
    user_picture_id: int | None = None
):
    """Описание: добавление пользователя. На ввод подаются логин, пароль, email, фамилия, имя, отчество, возраст, пол и идентификатор картинки."""
    conn = get_db_connection()
    if user_login is not None and len(user_login) >= 3:
        raise HTTPException(status_code=400, detail="Ошибка: логин пользователя должен быть не менее 3 символов.")
    if user_login is not None and len(user_login) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина логина должна быть меньше или равна 30 символов.")
    if user_password is not None and len(user_password) >= 6:
        raise HTTPException(status_code=400, detail="Ошибка: пароль пользователя должен быть не менее 6 символов.")
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

    hashed_password = get_password_hash(user_password)
    x = insert_user(conn, user_login, hashed_password, user_email, user_surname, user_name, user_fathername, user_age, user_is_female, user_picture_id)
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
    },
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: у вас нет прав для обновления данных этого пользователя."}
            }
        }
    }
})
async def users_update(
    user_id: int,
    user_login: str | None = None,
    user_password: str | None = None,
    user_email: str | None = None,
    user_surname: str | None = None,
    user_name: str | None = None,
    user_fathername: str | None = None,
    user_age: int | None = None,
    user_is_female: int | None = None,
    user_picture_id: int | None = None,
    current_user: dict = Depends(get_current_user)
):
    """Описание: изменение параметров пользователя. На ввод подаются идентификатор, логин, пароль, email, фамилия, имя, отчество, возраст, пол и идентификатор картинки."""
    if not current_user['user_is_admin'] and current_user['user_id'] != user_id:
        raise HTTPException(
            status_code=403,
            detail="Ошибка: у вас нет прав для обновления данных этого пользователя."
        )

    conn = get_db_connection()
    if user_login is not None and len(user_login) >= 3:
        raise HTTPException(status_code=400, detail="Ошибка: логин пользователя должен быть не менее 3 символов.")
    if user_login is not None and len(user_login) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина логина должна быть меньше или равна 30 символов.")
    if user_password is not None and len(user_password) >= 6:
        raise HTTPException(status_code=400, detail="Ошибка: пароль пользователя должен быть не менее 6 символов.")
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

    if len(find_user_login_with_id(conn, user_id, user_login)) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: логин должен быть уникальным (повторы не допускаются).")

    y = get_one_user(conn, user_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: пользователь с данным ID не найден, потому удалить его невозможно.")

    hashed_password = get_password_hash(user_password) if user_password else None
    x = update_user(conn, user_id, user_login, hashed_password, user_email, user_surname, user_name, user_fathername, user_age, user_is_female, user_picture_id)
    return Response("{'message':'Пользователь обновлён.'}", status_code=200)

@router.patch("/users/{user_id}/set-admin", tags=["UserController"], responses={
    200: {
        "description": "User set as admin successfully",
        "content": {
            "application/json": {
                "example": {"message": "Пользователь назначен администратором."}
            }
        }
    },
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: у вас нет прав для изменения статуса администратора."}
            }
        }
    }
})
async def set_user_as_admin(
    user_id: int,
    current_user: dict = Depends(get_current_active_admin_user)
):
    """Описание: установка пользователя как администратора."""
    conn = get_db_connection()
    y = get_one_user(conn, user_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: пользователь с данным ID не найден, потому удалить его невозможно.")

    x = update_user_set_admin(conn, user_id)
    return Response("{'message':'Пользователь назначен администратором.'}", status_code=200)

@router.patch("/users/{user_id}/unset-admin", tags=["UserController"], responses={
    200: {
        "description": "User unset as admin successfully",
        "content": {
            "application/json": {
                "example": {"message": "Статус администратора снят с пользователя."}
            }
        }
    },
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: у вас нет прав для изменения статуса администратора."}
            }
        }
    }
})
async def unset_user_as_admin(
    user_id: int,
    current_user: dict = Depends(get_current_active_admin_user)
):
    """Описание: снятие статуса администратора с пользователя."""
    conn = get_db_connection()
    y = get_one_user(conn, user_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: пользователь с данным ID не найден, потому удалить его невозможно.")

    x = update_user_set_notadmin(conn, user_id)
    return Response("{'message':'Статус администратора снят с пользователя.'}", status_code=200)