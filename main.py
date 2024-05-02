from src.API_HH import HH, HH_save, HH_work

def user_interaction():
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    work = HH()
    HH.vac_import(work,search_query,top_n)
    work_save = HH_save(work.vacancies)
    HH_save.save_vacancies(work_save,'C:/ProgramData/corseOOP/data/vacancies.json')
    data_work = HH_work('C:/ProgramData/corseOOP/data/vacancies.json')
    HH_work.vacancies_open(data_work)
    if data_work.data =={}:
        print('по вышему запросу нет вакансий')
    else:
        for i in  range(len(data_work.data)):
            print(f'''
            {i+1}
            Название вакансии: {data_work.data[data_work.id[i]]['name']}
            Зарплата: {data_work.data[data_work.id[i]]['salary']['from']} - {data_work.data[data_work.id[i]]['salary']['to']}
            Город: {data_work.data[data_work.id[i]]['address']}
            ''')
    filter_value = input("Введите желаему валюту зарплаты для фильтрации вакансий из следующего списка (RUR,USD,KZT): ")
    HH_work.vacancies_sort_value(data_work,filter_value)
    if data_work.data =={}:
        print('по вышему запросу нет вакансий')
    else:
        for i in  range(len(data_work.data)):
            print(f'''
            {i+1}
            Название вакансии: {data_work.data[data_work.id[i]]['name']}
            Зарплата: {data_work.data[data_work.id[i]]['salary']['from']} - {data_work.data[data_work.id[i]]['salary']['to']}
            Город: {data_work.data[data_work.id[i]]['address']}
            ''')
    filter_range = input("Введите желаемук зарплату в формате (х-х): ")
    HH_work.vacancies_sort_salary(data_work, HH_work.vacancies_salary(data_work,filter_range))
    if data_work.data =={}:
        print('по вышему запросу нет вакансий')
    else:
        for i in  range(len(data_work.data)):
            print(f'''
            {i+1}
            Название вакансии: {data_work.data[data_work.id[i]]['name']}
            Зарплата: {data_work.data[data_work.id[i]]['salary']['from']} - {data_work.data[data_work.id[i]]['salary']['to']}
            Город: {data_work.data[data_work.id[i]]['address']}
            ''')
    print('Города для работы')
    for i in range(len(data_work.data)):
        print(f"""{i+1}:{data_work.data[data_work.id[i]]['address'].split(',')[0]}""")
    filter_city = input("Введите город из списка для фильтрации вакансий: ")
    HH_work.vacancies_sort_city(data_work,filter_city)

    if data_work.data =={}:
        print('по вышему запросу нет вакансий')
    else:
        for i in  range(len(data_work.data)):
            print(f'''
            {i+1}
            Название вакансии: {data_work.data[data_work.id[i]]['name']}
            Зарплата: {data_work.data[data_work.id[i]]['salary']['from']} - {data_work.data[data_work.id[i]]['salary']['to']}
            Город: {data_work.data[data_work.id[i]]['address']}
            ''')

if __name__ == "__main__":
    user_interaction()