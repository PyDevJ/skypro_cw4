import json
import os

from src.api import HeadHunterAPI, SuperJobAPI
from src.check_json import JsonAgent
from src.vacancy import Vacancy, VacancyAgent


def load_vacancies_to_json():
    """
    Запрос у пользователя количества вакансий и ключевые слова.
    Добавление найденных вакансий в файл.
    """
    hh_vacancies_count = int(input('Введите количество вакансий для сайта hh.ru: '))
    sj_vacancies_count = int(input('Введите количество вакансий для сайта superjob.ru: '))
    search_words = input('Введите ключевые слова для поиска: ').split()

    # Инициализация JSON-файла, если он не существует
    if not os.path.exists("vacancies.json"):
        with open("vacancies.json", "w", encoding="utf-8") as file:
            json.dump([], file)

    hh_api = HeadHunterAPI(hh_vacancies_count)
    hh_vacancies = VacancyAgent.pars_hh_ru(hh_api.get_vacancies(search_words))
    sj_vacancies = []
    if sj_vacancies_count != 0:
        sj_api = SuperJobAPI(sj_vacancies_count)
        sj_vacancies = VacancyAgent.pars_super_job(sj_api.get_vacancies(search_words))

    counter = 0
    for vacancy in hh_vacancies + sj_vacancies:
        if JsonAgent.add_vacancy(vacancy):
            counter += 1
    print(f'Добавлено {counter} вакансий')


def show_vacancies_by_title():
    """
    Выводит в консоль названия вакансий
    """
    JsonAgent.show_vacancies_title()


def delete_vacancy_by_title():
    """
    Удаляет вакансию по названию
    """
    title = input('Введите название вакансии для удаления: ')
    if JsonAgent.delete_vacancy_by_title(title):
        print(f'Вакансия {title} удалена')
    else:
        print(f'Вакансия {title} не найдена')


def clear_json():
    """
    Очищает файл vacancies.json
    """
    JsonAgent.clear_json()


def show_info_by_title():
    """
    Выводит информацию о вакансии по её названию
    """
    title = input('Введите название вакансии для вывода информации: ')
    JsonAgent.show_info_by_title(title)


def get_vacancies_by_k_words():
    """
    Выводит названия вакансий в консоль по ключевым словам
    """
    k_words = input('Введите ключевые слова для поиска: ').split()
    vacancies = Vacancy.all_from_json()
    filtered = VacancyAgent.filter_vacancies_by_keywords(vacancies, k_words)
    if len(filtered) > 0:
        for title in filtered:
            print(title)
    else:
        print('Вакансий по таким словам не найдено')


def get_vacancies_by_salary():
    """
    Выводит названия вакансий в консоль по диапазону заработной платы
    """
    sfrom = int(input('Введите заработную плату от: '))
    sto = int(input('Введите заработную плату до: '))
    vacancies = Vacancy.all_from_json()
    filtered = VacancyAgent.filter_vacancies_by_salary(vacancies, sfrom, sto)
    if len(filtered) > 0:
        for title in filtered:
            print(title)
    else:
        print('Вакансий по такому диапазону зарплаты не найдено')


def sort_vacancies_by_salary():
    """
    Сортирует вакансии по заработной плате (от большего к меньшему)
    """
    vacancies = Vacancy.all_from_json()
    vacancies = sorted(vacancies, key=lambda x: int(x.pay), reverse=True)
    JsonAgent.clear_json()
    for vacancy in vacancies:
        JsonAgent.add_vacancy(vacancy)
    print('Файл отсортирован')


def show_top_n():
    """
    Выводит в консоль информацию о первых 'n' вакансиях
    """
    try:
        n = int(input('Введите количество вакансий для просмотра: '))
    except:
        print('Число введено некорректно')
        exit()
    vacancies = Vacancy.all_from_json()
    counter = 0
    if n > len(vacancies):
        n = len(vacancies)
    while counter < n:
        print(vacancies[counter].title)
        counter += 1


if __name__ == "__main__":

    clear_json()  #-создаём пустой файл vacancies.json для последующего наполнения данными
    load_vacancies_to_json()  #-запрашиваем количество вакансий и сохраняем данные в файл.
    show_vacancies_by_title()  #-выводим в консоль названия вакансий.
#    delete_vacancy_by_title()  #-удаляем вакансию по названию.
#    show_info_by_title()  #-выводим информацию о вакансии по её названию.
#    get_vacancies_by_k_words()  #-выводим названия вакансий в консоль по ключевым словам.
#    get_vacancies_by_salary()  #-выводим названия вакансий в консоль по диапазону заработной платы.
#    sort_vacancies_by_salary()  #-сортируем вакансии по заработной плате (от большего к меньшему).
#    show_top_n()  #-выводим в консоль информацию о первых 'n' вакансиях

#    print(Vacancy.all_from_json())
