from dataclasses import asdict
from typing import List, Type, Union

import dataset


class BaseRepository:
    """
    A base class for database repositories.

    Attributes:
        table_name (str): The name of the table.
        model_class (Type): The class of the model.
        _database (dataset.Database): The database instance to connect to.
        _table (dataset.Table): The table instance to connect to.
    """
    _database: dataset.Database
    _table: dataset.Table
    table_name: str
    model_class: Type

    def __init__(
        self, database: dataset.Database, table_name: str, model_class: Type
    ) -> None:
        """
        Initializes a new instance of the BaseRepository class.

        Args:
            database (dataset.Database): The database instance to connect to.
            table_name (str): The name of the table.
            model_class (Type): The class of the model.
        """
        self.table_name = table_name
        self.model_class = model_class
        self._database = database
        self._table = self._database[self.table_name]


    def insert(self, items: List[object]) -> None:
        """
        Inserts the given items into the database.

        Args:
            items (List[object]): The items to insert into the database.
        """
        items_dicts = list(map(asdict, items))
        self._table.insert_many(items_dicts)

    def find(
        self,
        ids: Union[List[int], None] = None,
        **kwargs
    ) -> List[object]:
        """
        Finds the items in the database.

        Args:
            ids (Union[List[int], None], optional): The ids of the items to
                find. Defaults to None.
            **kwargs: The keyword arguments for finding the items.

        Returns:
            List[object]: The list of items found.
        """
        if ids is not None:
            results = self._table.find(id=ids)
        elif kwargs:
            results = self._table.find(**kwargs)
        else:
            return []
        instancies = [self.model_class(**r) for r in results]
        return instancies

    def find_one(self, id_: int) -> Union[object, None]:
        """
        Finds a single item in the database with the specified ID.

        Args:
            id_ (int): The ID of the item to find.

        Returns:
            Union[object, None]: The matching item, or None if not found.
        """
        result = self._table.find_one(id=id_)
        instance = self.model_class(**result) if result else None
        return instance

    def all(self, page: int = None, page_size: int = None) -> List[object]:
        """
        Returns all items in the database, optionally paginated.

        Args:
            page (int, optional): The page number to retrieve.
                If not provided, retrieves all items.
            page_size (int, optional): The number of items per page.
                If not provided, retrieves all items.

        Returns:
            List[object]: A list of all items in the database, paginated if applicable.
        """
        if page is not None and page_size is not None:
            offset = (page - 1) * page_size
            results = self._table.find(_offset=offset, _limit=page_size)
        else:
            results = self._table.all()
        instancies = [self.model_class(**r) for r in results]
        return instancies

    def update(self, item: object) -> None:
        """
        Updates an item in the database.

        Args:
            item (object): The item to update.
        """
        item_dict = asdict(item)
        self._table.update(item_dict, ['id'])

    def delete(self, id_: int) -> None:
        """
        Deletes an item from the database with the specified ID.

        Args:
            id_ (int): The ID of the item to delete.
        """
        self._table.delete(id=id_)
