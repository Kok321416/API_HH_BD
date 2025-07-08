import requests
from typing import List, Dict, Any
from .base_api import BaseAPI


class HeadHunterAPI(BaseAPI):
    """
    Класс для работы с API HeadHunter.
    Реализует получение вакансий с платформы hh.ru.
    """

    def __init__(self):
        self.base_url = "https://api.hh.ru/vacancies"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """
        Получить вакансии с hh.ru по поисковому запросу.
        """
        params = {
            "text": search_query,
            "area": 113,  # Россия
            "per_page": 100,
            "page": 0,
        }

        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                return data.get("items", [])
            else:
                print(f"Ошибка при получении вакансий: {response.status_code}")
                return []

        except requests.RequestException as e:
            print(f"Ошибка сети при получении вакансий: {e}")
            return []
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return []
