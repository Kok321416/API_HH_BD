from abc import ABC, abstractmethod
from typing import List
from models.vacancy import Vacancy


class BaseStorage(ABC):
    """
    Абстрактный класс для работы с хранилищем вакансий.
    Определяет интерфейс для добавления, получения и удаления вакансий.
    """

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> bool:
        """
        Добавить вакансию в хранилище.
        """
        pass

    @abstractmethod
    def get_vacancies(self, **kwargs) -> List[Vacancy]:
        """
        Получить вакансии из хранилища по указанным критериям.

        Args:
            **kwargs: Критерии для фильтрации вакансий

        Returns:
            List[Vacancy]: Список вакансий, соответствующих критериям
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> bool:
        """
        Удалить вакансию из хранилища.

        Args:
            vacancy (Vacancy): Объект вакансии для удаления

        Returns:
            bool: True если вакансия успешно удалена, False в противном случае
        """
        pass

    @abstractmethod
    def clear_all(self) -> bool:
        """
        Очистить все вакансии из хранилища.

        Returns:
            bool: True если хранилище успешно очищено, False в противном случае
        """
        pass
