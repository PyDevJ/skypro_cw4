from src.api import HeadHunterAPI, SuperJobAPI


if __name__ == "__main__":
    hh_api = HeadHunterAPI(1)
    hh_vacancies = hh_api.get_vacancies("Python")
    print(hh_vacancies)

    superjob_api = SuperJobAPI(1)
    superjob_vacancies = superjob_api.get_vacancies("Python")
    print(superjob_vacancies)
    superjob_vacancies = superjob_api.get_vacancies("Java")
    print(superjob_vacancies)
