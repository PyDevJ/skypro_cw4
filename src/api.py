import json
import os
import requests
from abc import ABC, abstractmethod
from dotenv import load_dotenv


class Api(ABC):
    """Абстрактный класс для работы с API сайтов."""

    @abstractmethod
    def get_vacancies(self, words):
        pass


class HeadHunterAPI(Api):
    """Класс для работы с API на hh.ru."""

    def __init__(self, count) -> None:
        """
        Конструктор с входным параметром количества вакансий.
        """
        self.url = 'https://api.hh.ru/vacancies/'
        self.params = {
            'per_page': count,
            'area': 1,
            'page': 1
        }

    def get_vacancies(self, words):
        """
        Метод получения списка с вакансиями по ключевым словам.
        """
        self.params['text'] = words
        r = requests.get(self.url, params=self.params)
        vacancies = json.loads(r.text)['items']
        return vacancies


class SuperJobAPI(Api):
    """Класс для работы с API на superjob.ru."""

    def __init__(self, count):
        """
        Конструктор с входным параметром количества вакансий.
        """
        load_dotenv()
        __api_token: str = os.environ.get("SJ_API_KEY")
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        self.headers = {"X-Api-App-Id": __api_token}
        self.params = {
            'count': count,
            'page': 1,
            'town': 'Moscow',
        }

    def get_vacancies(self, words):
        """
        Метод получения списка с вакансиями по ключевым словам.
        """
        self.params['keywords'] = words
        r = requests.get(self.url, params=self.params, headers=self.headers)
        vacancies = json.loads(r.text)['objects']
        return vacancies
