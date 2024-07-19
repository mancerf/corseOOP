import json
import os

from src.API_HH import HH, HH_save, HH_work
import pytest


@pytest.fixture()
def example():
    return HH()


@pytest.fixture()
def text():
    return 'Разработчик'


@pytest.fixture()
def count():
    return 10


def test_vac_import(example, text, count):
    HH.vac_import(example, text, count)
    assert len(example.vacancies) == count


@pytest.fixture()
def document():
    return 'vacancies.json'


def test_save_vacancies(example, text, count, document):
    HH.vac_import(example, text, count)
    work_save = HH_save(example.vacancies)
    HH_save.save_vacancies(work_save, document)
    with open(document, 'r', encoding='utf8') as file:
        prime_data = json.load(file)
        assert len(prime_data) == count


@pytest.fixture()
def work_open(document):
    return HH_work(document)


def test_vacancies_open(work_open, count):
    HH_work.vacancies_open(work_open)
    assert len(work_open.prime_data) == count


def test_vacancies_salary(work_open, count):
    HH_work.vacancies_open(work_open)
    salary = HH_work.vacancies_salary(work_open, '1000-10000')
    assert salary[0] == 1000
    assert salary[1] == 10000


@pytest.fixture()
def filter_word():
    return ['RUR', 'KZT', 'USD']


def test_vacancies_sort_value(work_open, filter_word):
    HH_work.vacancies_open(work_open)
    HH_work.vacancies_sort_value(work_open, filter_word[0])
    for i in range(len(work_open.id)):
        assert work_open.data[work_open.id[i]]['salary']['currency'] == filter_word[0] or \
               work_open.data[work_open.id[i]]['salary']['currency'] == 'не указано'


def test_vacancies_sort_salary(work_open):
    HH_work.vacancies_open(work_open)
    HH_work.vacancies_sort_salary(work_open, HH_work.vacancies_salary(work_open, '1000-10000'))
    for i in range(len(work_open.id) - 1):
        assert work_open.data[work_open.id[i]]['salary']['from'] >= work_open.data[work_open.id[i + 1]]['salary']['from']



def test_vacancies_sort_city(work_open):
    HH_work.vacancies_open(work_open)
    HH_work.vacancies_sort_city(work_open,'Москва')
    for i in range(len(work_open.id)):
        city = work_open.data[work_open.id[i]]['address'].split(',')[0]
        assert city == 'Москва' or city == 'Не указано'

