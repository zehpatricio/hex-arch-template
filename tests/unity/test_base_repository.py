from dataclasses import dataclass
from typing import Optional

import pytest
import dataset

from app.persistence.repository import BaseRepository


@dataclass
class Person:
    name: str
    email: str
    age: int
    id: Optional[int] = None


@pytest.fixture(scope='function')
def database():
    connection = dataset.connect('sqlite:///:memory:')
    yield connection
    connection.close()


@pytest.fixture(scope='function')
def repository(database):
    return BaseRepository(database, 'people', Person)


@pytest.fixture(scope='function')
def people():
    return [
        Person(name='John', email='john@example.com', age=30),
        Person(name='Jane', email='jane@example.com', age=25),
        Person(name='Joe', email='joe@example.com', age=35),
    ]


def test_insert(repository, people):
    repository.insert(people)
    results = repository.all()

    assert len(results) == 3
    assert all(isinstance(p, Person) for p in results)


def test_find(repository, people):
    repository.insert(people)
    found = repository.find(ids=[1])

    assert len(found) == 1
    assert isinstance(found[0], Person)
    assert found[0].name == 'John'

    found = repository.find(age=30)
    assert len(found) == 1
    assert isinstance(found[0], Person)
    assert found[0].name == 'John'

    found = repository.find()
    assert len(found) == 0


def test_find_one(repository, people):
    repository.insert(people)
    found = repository.find_one(id_=1)

    assert isinstance(found, Person)
    assert found.name == 'John'


def test_all(repository, people):
    repository.insert(people)
    results = repository.all()

    assert len(results) == 3
    assert all(isinstance(p, Person) for p in results)


def test_update(repository, people):
    repository.insert(people)
    person = repository.find_one(id_=1)
    person.name = 'Johnny'
    repository.update(person)
    updated = repository.find_one(id_=1)

    assert updated.name == 'Johnny'


def test_delete(repository, people):
    repository.insert(people)
    repository.delete(id_=1)
    results = repository.all()

    assert len(results) == 2
    assert all(p.id != 1 for p in results)
