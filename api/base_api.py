from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseAPI(ABC):
    """
    Абстрактный класс для работы с API сервисов вакансий.
    Определяет интерфейс для получения вакансий с различных платформ.
    """
    
    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """
        Получить вакансии по поисковому запросу.
        """
        pass 