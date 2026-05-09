import requests

class HHAPI:
    BASE_URL = "https://api.hh.ru"
    EMPLOYER_IDS = [
        "1740",  # Яндекс
        "3529",  # Сбер
        "15478",  # VK
        "78638",  # Тинькофф
        "3776",  # МТС
        "84585",  # Авито
        "2180",  # Ozon
        "643473",  # Lamoda
        "39305",  # Газпром
        "2748",  # X5 Group
    ]

    def get_employer(self, employer_id: str) -> dict:
        """формирование URL для запроса по конкретному работодателю"""
        url = f"{self.BASE_URL}/employers/{employer_id}"
        response = requests.get(url)
        return response.json()

    def get_vacancies(self, employer_id: str) -> list:
        """Получение списка вакансий"""
        url = f"{self.BASE_URL}/vacancies"
        params = {
            "employer_id": employer_id,
            "per_page": 100,
            "page": 0,
        }
        response = requests.get(url, params=params)
        return response.json().get("items", [])

    def get_all_employers_and_vacancies(self) -> tuple:
        """Получение всех работодателей и вакансии"""
        employers = []
        vacancies = []

        for employer_id in self.EMPLOYER_IDS:
            employer = self.get_employer(employer_id)
            employers.append(employer)
            employer_vacancies = self.get_vacancies(employer_id)
            vacancies.extend(employer_vacancies)
        return employers, vacancies