import json
import os
from typing import List, Dict, Any
from .base_storage import BaseStorage
from models.vacancy import Vacancy


class JSONSaver(BaseStorage):
    """
    Класс для сохранения вакансий в JSON-файл.
    Реализует интерфейс BaseStorage для работы с файловым хранилищем.
    """
    
    def __init__(self, filename: str = "vacancies.json"):
        """
        Инициализация JSON-хранилища.
        
        Args:
            filename (str): Имя файла для сохранения вакансий
        """
        self.filename = filename
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Создать файл, если он не существует."""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def _load_vacancies(self) -> List[Dict[str, Any]]:
        """Загрузить вакансии из файла."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_vacancies(self, vacancies_data: List[Dict[str, Any]]):
        """Сохранить вакансии в файл."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(vacancies_data, f, ensure_ascii=False, indent=2)
    
    def _vacancy_to_dict(self, vacancy: Vacancy) -> Dict[str, Any]:
        """Преобразовать объект Vacancy в словарь."""
        return {
            "title": vacancy.title,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "description": vacancy.description,
            "requirements": vacancy.requirements,
            "company": vacancy.company
        }
    
    def _dict_to_vacancy(self, vacancy_dict: Dict[str, Any]) -> Vacancy:
        """Преобразовать словарь в объект Vacancy."""
        return Vacancy(
            title=vacancy_dict.get("title", ""),
            url=vacancy_dict.get("url", ""),
            salary=vacancy_dict.get("salary", 0),
            description=vacancy_dict.get("description", ""),
            requirements=vacancy_dict.get("requirements", ""),
            company=vacancy_dict.get("company", "")
        )
    
    def add_vacancy(self, vacancy: Vacancy) -> bool:
        """
        Добавить вакансию в JSON-файл.
        
        Args:
            vacancy (Vacancy): Объект вакансии для добавления
            
        Returns:
            bool: True если вакансия успешно добавлена
        """
        try:
            vacancies_data = self._load_vacancies()
            
            # Проверяем, не существует ли уже такая вакансия
            vacancy_dict = self._vacancy_to_dict(vacancy)
            for existing_vacancy in vacancies_data:
                if (existing_vacancy.get("url") == vacancy.url and 
                    existing_vacancy.get("title") == vacancy.title):
                    return False  # Вакансия уже существует
            
            vacancies_data.append(vacancy_dict)
            self._save_vacancies(vacancies_data)
            return True
            
        except Exception as e:
            print(f"Ошибка при добавлении вакансии: {e}")
            return False
    
    def get_vacancies(self, **kwargs) -> List[Vacancy]:
        """
        Получить вакансии из JSON-файла по указанным критериям.
        
        Args:
            **kwargs: Критерии для фильтрации:
                - keyword: ключевое слово для поиска в описании
                - min_salary: минимальная зарплата
                - max_salary: максимальная зарплата
                - company: название компании
            
        Returns:
            List[Vacancy]: Список вакансий, соответствующих критериям
        """
        try:
            vacancies_data = self._load_vacancies()
            vacancies = [self._dict_to_vacancy(v) for v in vacancies_data]
            
            # Применяем фильтры
            if kwargs.get("keyword"):
                keyword = kwargs["keyword"].lower()
                vacancies = [v for v in vacancies 
                           if keyword in v.description.lower() or 
                              keyword in v.title.lower()]
            
            if kwargs.get("min_salary"):
                min_salary = kwargs["min_salary"]
                vacancies = [v for v in vacancies if v.salary >= min_salary]
            
            if kwargs.get("max_salary"):
                max_salary = kwargs["max_salary"]
                vacancies = [v for v in vacancies if v.salary <= max_salary]
            
            if kwargs.get("company"):
                company = kwargs["company"].lower()
                vacancies = [v for v in vacancies 
                           if company in v.company.lower()]
            
            return vacancies
            
        except Exception as e:
            print(f"Ошибка при получении вакансий: {e}")
            return []
    
    def delete_vacancy(self, vacancy: Vacancy) -> bool:
        """
        Удалить вакансию из JSON-файла.
        
        Args:
            vacancy (Vacancy): Объект вакансии для удаления
            
        Returns:
            bool: True если вакансия успешно удалена
        """
        try:
            vacancies_data = self._load_vacancies()
            
            # Ищем вакансию для удаления
            for i, existing_vacancy in enumerate(vacancies_data):
                if (existing_vacancy.get("url") == vacancy.url and 
                    existing_vacancy.get("title") == vacancy.title):
                    del vacancies_data[i]
                    self._save_vacancies(vacancies_data)
                    return True
            
            return False  # Вакансия не найдена
            
        except Exception as e:
            print(f"Ошибка при удалении вакансии: {e}")
            return False
    
    def clear_all(self) -> bool:
        """
        Очистить все вакансии из JSON-файла.
        
        Returns:
            bool: True если файл успешно очищен
        """
        try:
            self._save_vacancies([])
            return True
        except Exception as e:
            print(f"Ошибка при очистке файла: {e}")
            return False
    
    def add_vacancies(self, vacancies: List[Vacancy]) -> int:
        """
        Добавить несколько вакансий в JSON-файл.
        
        Args:
            vacancies (List[Vacancy]): Список вакансий для добавления
            
        Returns:
            int: Количество успешно добавленных вакансий
        """
        added_count = 0
        for vacancy in vacancies:
            if self.add_vacancy(vacancy):
                added_count += 1
        return added_count 