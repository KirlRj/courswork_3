# import requests
import json
from pathlib import Path


class HHAPI:
    # BASE_URL = "https://api.hh.ru"
    # EMPLOYER_IDS = [
    #     "1740",  # Яндекс
    #     "3529",  # Сбер
    #     "15478",  # VK
    #     "78638",  # Тинькофф
    #     "3776",  # МТС
    #     "84585",  # Авито
    #     "2180",  # Ozon
    #     "643473",  # Lamoda
    #     "39305",  # Газпром
    #     "2748",  # X5 Group
    # ]
    DATA_FILE = Path(__file__).parent.parent.parent / "data" / "hh_vacancies.json"
    # def get_employer(self, employer_id: str) -> dict:
    #     """формирование URL для запроса по конкретному работодателю"""
    #     url = f"{self.BASE_URL}/employers/{employer_id}"
    #     headers = {"User-Agent": "coursework/1.0"}
    #     response = requests.get(url, headers=headers)
    #     return response.json()
    #
    # def get_vacancies(self, employer_id: str) -> list:
    #     """Получение списка вакансий"""
    #     url = f"{self.BASE_URL}/vacancies"
    #     headers = {"User-Agent": "coursework/1.0"}
    #     params = {
    #         "employer_id": employer_id,
    #         "per_page": 100,
    #         "page": 0,
    #     }
    #     response = requests.get(url, params=params, headers=headers)
    #     return response.json().get("items", [])

    def get_all_employers_and_vacancies(self) -> tuple:
        """Получение всех работодателей и вакансии"""
        with open(self.DATA_FILE, encoding="utf-8") as f:
            data = json.load(f)
        all_vacancies = data.get("items", [])
        employers_dict = {}
        for vacancy in all_vacancies:
            employer = vacancy.get("employer", {})
            employer_id = str(employer.get("id"))
            if employer_id not in employers_dict:
                employers_dict[employer_id] = employer
        # for employer_id in self.EMPLOYER_IDS:
        #     employer = self.get_employer(employer_id)
        #     employers.append(employer)
        #     employer_vacancies = self.get_vacancies(employer_id)
        #     vacancies.extend(employer_vacancies)
        employers = list(employers_dict.values())

        return employers, all_vacancies
