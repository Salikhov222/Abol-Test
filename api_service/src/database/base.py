from sqlalchemy import MetaData
from sqlalchemy.orm import as_declarative, declared_attr

# создание общей схемы
metadata = MetaData()

@as_declarative()
class Base:
    """ Определение общего базового класса, от которого будут наследоваться все модели"""
    id: int
    __name__: str
    metadata = metadata

    @declared_attr
    def __tablename__(cls) -> str:
        """Автоматическое генерация имени таблицы"""
        return cls.__name__.lower()