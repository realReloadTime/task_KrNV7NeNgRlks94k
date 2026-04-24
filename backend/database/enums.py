import enum


class RoleEnum(enum.StrEnum):
    ADMIN = 'admin'
    USER = 'user'

    @classmethod
    def get_all(cls):
        return [cls.ADMIN, cls.USER]
