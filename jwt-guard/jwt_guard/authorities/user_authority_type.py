from enum import Enum


class UserAuthorityType(Enum):

    # Работа с пользователями
    ADD_USERS = ("ADD_USERS", "Добавление пользователей")
    REMOVE_USERS = ("REMOVE_USERS", "Удаление пользователей")
    EDIT_USERS = ("EDIT_USERS", "Редактирование пользователей")
    GRANT_PERMISSIONS = ('GRANT_PERMISSIONS', 'Выдача прав')
    REVOKE_PERMISSIONS = ('REVOKE_PERMISSIONS', 'Отзыв прав')

    # Работа со справочниками
    EDIT_DICTIONARY = ("EDIT_DICTIONARY", "Внесение правок в справочник")
    DELETE_DICTIONARY = ("DELETE_DICTIONARY", "Удаление данных из справочника")
    ADMIN = ('ADMIN', 'Администратор')

    def __new__(cls, system_name: str, display_name: str):
        obj = object.__new__(cls)
        obj._value_ = system_name
        obj.system_name = system_name
        obj.display_name = display_name
        return obj

    @classmethod
    def from_system_name(cls, code: str) -> "UserAuthorityType":
        for item in cls:
            if item.system_name == code:
                return item
        raise ValueError(f"Unknown authority code: {code}")