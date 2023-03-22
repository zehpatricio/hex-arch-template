from dataclasses import asdict
from typing import List, Type, Union

import dataset


class BaseRepository:
    _database: dataset.Database
    _table: dataset.Table
    table_name: str
    model_class: Type

    def __init__(
        self, database: dataset.Database, table_name: str, model_class: Type
    ) -> None:
        self.table_name = table_name
        self.model_class = model_class
        self._database = database
        self._table = self._database[self.table_name]


    def insert(self, items: List[object]) -> None:
        items_dicts = list(map(asdict, items))
        self._table.insert_many(items_dicts)

    def find(
        self,
        ids: Union[List[int], None] = None,
        **kwargs
    ) -> List[object]:
        if ids is not None:
            results = self._table.find(id=ids)
        elif kwargs:
            results = self._table.find(**kwargs)
        else:
            return []
        instancies = [self.model_class(**r) for r in results]
        return instancies

    def find_one(self, id_: int) -> object:
        result = self._table.find_one(id=id_)
        instance = self.model_class(**result)
        return instance

    def all(self) -> List[object]:
        results = self._table.all()
        instancies = [self.model_class(**r) for r in results]
        return instancies

    def update(self, item: object) -> None:
        item_dict = asdict(item)
        self._table.update(item_dict, ['id'])

    def delete(self, id_: int) -> None:
        self._table.delete(id=id_)
