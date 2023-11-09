import json

FILE = 'vacancies.json'


class Vacancy:
    """
    Класс для хранения и работы с информацией о вакансиях.
    Конструктор, принимает название, ссылку, заработную плату, требования.
    """

    def __init__(self, title, url, pay, requirement) -> None:
        self.title = title
        self.url = url
        self.pay = pay
        self.requirement = requirement

    def json(self):
        """
        Метод возвращает информацию о вакансии в виде словаря
        """
        return {
            'title': self.title,
            'url': self.url,
            'pay': self.pay,
            'requirement': self.requirement,
        }

    @classmethod
    def from_json(cls, params):
        """
        КлассМетод, который создает вакансию на основе словаря
        """
        return cls(params['title'], params['url'], params['pay'], params['requirement'])

    @classmethod
    def all_from_json(cls):
        """
        КлассМетод, который создает массив вакансий на основе информации из json файла
        """
        with open(FILE, 'r', encoding='utf-8') as f:
            vacancies = json.load(f)
        output = []
        for vacancy in vacancies:
            tmp = Vacancy.from_json(vacancy)
            output.append(tmp)
        return output

    def show_info(self):
        """
        Метод, который выводит в консоль информацию о вакансии
        """
        print(self.title)
        print(self.url)
        print(f'Заработная плата {self.pay}')
        print(self.requirement)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}\n({self.title}\n{self.url}\n{self.pay}\n{self.requirement})\n"

    def __eq__(self, other):
        return self.pay == other.pay

    def __ne__(self, other):
        return self.pay != other.pay

    def __lt__(self, other):
        return self.pay < other.pay

    def __gt__(self, other):
        return self.pay > other.pay


class VacancyAgent:
    """Класс для обработки вакансии"""
    @staticmethod
    def pars_super_job(vacancies):
        """
        Метод, который получает на вход словарь из superjob и возвращает массив Vacancy
        """
        output = []
        for vacancy in vacancies:
            if vacancy['payment_from'] is not None:
                tmp = Vacancy(vacancy['profession'], vacancy['link'], vacancy['payment_from'], vacancy['candidat'])
            elif vacancy['payment_to'] is not None:
                tmp = Vacancy(vacancy['profession'], vacancy['link'], vacancy['payment_to'], vacancy['candidat'])
            else:
                tmp = Vacancy(vacancy['profession'], vacancy['link'], 0, vacancy['candidat'])
            output.append(tmp)
        return output

    @staticmethod
    def pars_hh_ru(vacancies):
        """
        Метод, который получает на вход словарь из hh.ru и возвращает массив Vacancy
        """
        output = []
        url_hh_v = 'https://hh.ru/vacancy/'
        for vacancy in vacancies:
            if vacancy['salary'] is not None:
                if vacancy['salary']['from'] is not None:
                    tmp = Vacancy(vacancy['name'], f'{url_hh_v}{vacancy["id"]}', vacancy['salary']['from'],
                                  vacancy['snippet']['requirement'])
                else:
                    tmp = Vacancy(vacancy['name'], f'{url_hh_v}{vacancy["id"]}', vacancy['salary']['to'],
                                  vacancy['snippet']['requirement'])
            else:
                tmp = Vacancy(vacancy['name'], f'{url_hh_v}{vacancy["id"]}', 0,
                              vacancy['snippet']['requirement'])
            output.append(tmp)
        return output

    @staticmethod
    def filter_vacancies_by_keywords(vacancies: list, key_words=None):
        """
        Метод, который возвращает названия вакансий по заданным словам для поиска
        """
        if key_words is None:
            key_words = []
        output = []
        for vacancy in vacancies:
            title = [x.lower() for x in vacancy.title.split()]
            try:
                requirements = [x.lower() for x in vacancy.requirement.split()]
            except:
                requirements = []
            for key_word in key_words:
                if key_word.lower() in title or key_word.lower() in requirements:
                    output.append(vacancy.title)
                    break
        return output

    @staticmethod
    def filter_vacancies_by_salary(vacancies: list, sfrom, sto):
        """
        Метод, который возвращает названия вакансий по заданному диапазону заработной платы
        """
        output = []
        for vacancy in vacancies:
            try:
                if sfrom <= vacancy.pay <= sto:
                    output.append(vacancy.title)
            except:
                pass
        return output
