import requests
import json
from abc import ABC, abstractmethod
import math
class Parser(ABC):

    @abstractmethod
    def vac_import(self):
        pass
    
class Save(ABC):
    @abstractmethod
    def save_vacancies(self, document):
        pass




class HH(Parser):
    """
    Класс для работы с API HH.ru
    трибуты:
    self.url - ссылка на API HH.ru
    self.headers - библиотека, где указывается, что мы ищем вакансии как работки
    self.params - билиблиотека  ключи text- поиск вакансии по названию, page - стриница поиска, per_page - количесвто вакансии
    self.vacancies - список найденных вакансий
    """

    def __init__(self):
        super().__init__()
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []

    def vac_import(self, text, count):
        """
        метод получает данные по ключевому слову в respon конвертирует их в формат json  и полученные данные добавляет в self.vacancies
        :param text: искомая вакансия
        :param count: необходимое количество вакансий
        """
        qount = 0
        error = 0
        page = 0
        self.params['text'] = text
        while qount < count:
            self.params['page'] = page
            page +=1
            vacancies_response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies_json = vacancies_response.json()

            if len(vacancies_json['items']) >= 0:
                for i in range(len(vacancies_json['items'])):
                    self.vacancies.append(vacancies_json['items'][i])
                    if len(self.vacancies) == count:
                        break
                qount = len(self.vacancies)
            error +=1
            if error == 10:
                break



class HH_save(Save):
    """
     класс для работы с полученными вакансиями
     атрибуты:
        self.data - список вакансий
        self.salary = список зарплат
        self.id = список id
        self.name = список наименований вакансий
        self.address = список адрессов
        self.count = количество вакансий

    """

    def __init__(self,data):
        super().__init__()
        self.data = data
        self.salary = []
        self.id = []
        self.name = []
        self.address = []
        self.count = len(self.data)
        for i in range(self.count):
            self.id.append(self.data[i]['id'])
            if self.data[i]['salary'] is None:
                salary = {"from": 0, "to": 0}
                self.salary.append(salary)
            elif self.data[i]['salary']['from'] is None or self.data[i]['salary']['to'] is None:
                if self.data[i]['salary']['from'] is None:
                    self.data[i]['salary']['from'] = 0
                    self.salary.append(self.data[i]['salary'])
                else:
                    self.data[i]['salary']['to'] = 0
                    self.salary.append(self.data[i]['salary'])
            else:
                self.salary.append(self.data[i]['salary'])



            self.name.append(self.data[i]['name'])
            if self.data[i]['address'] is None:
                self.address.append('Не указано')
            elif self.data[i]['address']['raw'] is None:
                self.address.append('Не указано')
            else:
                self.address.append(self.data[i]['address']['raw'])


    def save_vacancies(self,document):
        """
        метод для сохрание вакансий в файл с необходимыми данными
        :param document: список вакансий
        """
        with open(document, 'w', encoding='utf8') as file:
            up = []
            for i in range(self.count):
                up.append({
                        'id': self.id[i],
                        'name': self.name[i],
                        'salary': self.salary[i],
                        'address': self.address[i],
                    })
            json.dump(up, file, indent = 2, ensure_ascii = False)

class HH_work():
    """
    класс для обработки вакансий
    атрибуты:
        self.document - адрес файла в формате json, где хранятся вакансии
        self.index - инекс вакансий
        self.data = вакансии
    """

    def __init__(self, document):
        self.document = document
        self.prime_data = []
        self.id = []
        self.data = {}




    def vacancies_open(self):
        """
        сохраниет содержимое файла в переменную self.data
        """
        with open(self.document,'r',encoding='utf8') as file:
            self.prime_data = json.load(file)
            for i in range(len(self.prime_data)):
                self.id.append(self.prime_data[i]['id'])
                self.data[self.id[i]] = self.prime_data[i]


    def vacancies_del(self):
        pass
    def vacancies_add(self):
        pass

    def vacancies_salary(self, salary_wont):
        salary = salary_wont.split('-')
        print(salary)
        salary_list = []
        if len(salary) < 3 and salary[0] != '':
            salary_list.append(int(salary[0]))
            return salary_list
        elif len(salary) > 2 and salary[0] != '':
            print(2)
            salary_list.append(int(salary[0]))
            salary_list.append(int(salary[2]))
            return salary_list
        else:
            salary_list.append(int(salary[2]))
            return salary_list

    def vacancies_sort_value(self, value):
        data_sort_value = {}
        id_sort_value = []
        for i in range(len(self.data)):
            if self.data[self.id[i]]['salary']['currency'] == None:
                continue
            elif self.data[self.id[i]]['salary']['currency'] == 'RUR':
                id_sort_value.append(self.id[i])
                data_sort_value[self.id[i]] = self.data[self.id[i]]
            elif self.data[self.id[i]]['salary']['currency'] == 'KZT':
                id_sort_value.append(self.id[i])
                data_sort_value[self.id[i]] = self.data[self.id[i]]
            elif self.data[self.id[i]]['salary']['currency'] == 'USD':
                id_sort_value.append(self.id[i])
                data_sort_value[self.id[i]] = self.data[self.id[i]]
        self.id = id_sort_value
        self.data = data_sort_value

    def vacancies_sort_salary(self, salary):
        data_sort_salery = {}
        id_sort_salery = []
        for i in range(len(self.data)):
            if self.data[self.id[i]]['salary'] == None:
                continue
            elif int(self.data[self.id[i]]['salary']['from']) ==0 and int(self.data[self.id[i]]['salary']['to']) == 0:
                id_sort_salery.append(self.id[i])
                data_sort_salery[self.id[i]] = 0
            elif int(self.data[self.id[i]]['salary']['from']) >= min(salary) and int(self.data[self.id[i]]['salary']['from']) != 0:
                id_sort_salery.append(self.id[i])
                data_sort_salery[self.id[i]] = self.data[self.id[i]]
        self.id = id_sort_salery
        self.data = data_sort_salery
        print(len(self.data))

    def vacancies_sort_city(self,city_find):
        """
        метод выполняет сортировку вакансий по запросу пользователя
        :param city_find: город, который исчет пользователь
        """
        data_sort_city = {}
        id_sort_city =[]
        for i in range(len(self.data)):
            city = self.data[self.id[i]]['address'].split(',')[0]
            if city_find == city:
                data_sort_city[self.id[i]] = self.data[self.id[i]]
                id_sort_city.append(self.id[i])
        self.id = id_sort_city
        self.data = data_sort_city







r = HH()
HH.vac_import(r,'Python', 20)
test_save = HH_save(r.vacancies)
e = HH_save.save_vacancies(test_save,'C:/ProgramData/corseOOP/data/vacancies.json')
work = HH_work('C:/ProgramData/corseOOP/data/vacancies.json')
HH_work.vacancies_open(work)
w = '15 - 300000000'
#a = HH_work.vacancies_sort_city(work, 'Ташкент')

HH_work.vacancies_sort_salary(work,HH_work.vacancies_salary(work,w))
print(work.data)


