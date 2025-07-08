from typing import List, Dict, Any, Optional


class Vacancy:
    """
    Класс для работы с вакансиями.
    Поддерживает методы сравнения по зарплате и валидацию данных.
    """
    
    def __init__(self, title: str, url: str, salary: Optional[Dict[str, Any]], 
                 description: str, requirements: str = "", company: str = ""):
        """
        Инициализация вакансии.
        
        Args:
            title (str): Название вакансии
            url (str): Ссылка на вакансию
            salary (Optional[Dict[str, Any]]): Информация о зарплате
            description (str): Описание вакансии
            requirements (str): Требования к кандидату
            company (str): Название компании
        """
        self.title = self._validate_title(title)
        self.url = self._validate_url(url)
        self.salary = self._validate_salary(salary)
        self.description = self._validate_description(description)
        self.requirements = requirements
        self.company = company
    
    def _validate_title(self, title: str) -> str:
        """Валидация названия вакансии."""
        if not title or not isinstance(title, str):
            raise ValueError("Название вакансии должно быть непустой строкой")
        return title.strip()
    
    def _validate_url(self, url: str) -> str:
        """Валидация URL вакансии."""
        if not url or not isinstance(url, str):
            raise ValueError("URL вакансии должен быть непустой строкой")
        return url.strip()
    
    def _validate_salary(self, salary: Optional[Dict[str, Any]]) -> int:
        """Валидация и обработка зарплаты."""
        if salary is None:
            return 0
        
        # Извлекаем зарплату из структуры hh.ru
        if isinstance(salary, dict):
            # Приоритет отдаем максимальной зарплате, если она указана
            if salary.get("to") is not None:
                return salary["to"]
            elif salary.get("from") is not None:
                return salary["from"]
            else:
                return 0
        
        # Если зарплата передана как число
        if isinstance(salary, (int, float)):
            return int(salary)
        
        return 0
    
    def _validate_description(self, description: str) -> str:
        """Валидация описания вакансии."""
        if not description or not isinstance(description, str):
            return "Описание не указано"
        return description.strip()
    
    def __lt__(self, other) -> bool:
        """Сравнение вакансий по зарплате (меньше)."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary < other.salary
    
    def __le__(self, other) -> bool:
        """Сравнение вакансий по зарплате (меньше или равно)."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary <= other.salary
    
    def __eq__(self, other) -> bool:
        """Сравнение вакансий по зарплате (равно)."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary == other.salary
    
    def __ne__(self, other) -> bool:
        """Сравнение вакансий по зарплате (не равно)."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary != other.salary
    
    def __gt__(self, other) -> bool:
        """Сравнение вакансий по зарплате (больше)."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary > other.salary
    
    def __ge__(self, other) -> bool:
        """Сравнение вакансий по зарплате (больше или равно)."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary >= other.salary
    
    def __str__(self) -> str:
        """Строковое представление вакансии."""
        salary_str = f"{self.salary:,} руб." if self.salary > 0 else "Зарплата не указана"
        return f"{self.title} | {self.company} | {salary_str}"
    
    def __repr__(self) -> str:
        """Представление вакансии для отладки."""
        return f"Vacancy(title='{self.title}', salary={self.salary})"
    
    @staticmethod
    def cast_to_object_list(vacancies_json: List[Dict[str, Any]]) -> List['Vacancy']:
        """
        Преобразование JSON-данных в список объектов Vacancy.
        
        Args:
            vacancies_json (List[Dict[str, Any]]): Список вакансий в формате JSON
            
        Returns:
            List[Vacancy]: Список объектов Vacancy
        """
        vacancies = []
        
        for vacancy_data in vacancies_json:
            try:
                # Извлекаем данные из структуры hh.ru
                title = vacancy_data.get("name", "")
                url = vacancy_data.get("alternate_url", "")
                salary = vacancy_data.get("salary")
                description = vacancy_data.get("snippet", {}).get("requirement", "")
                requirements = vacancy_data.get("snippet", {}).get("requirement", "")
                company = vacancy_data.get("employer", {}).get("name", "")
                
                vacancy = Vacancy(
                    title=title,
                    url=url,
                    salary=salary,
                    description=description,
                    requirements=requirements,
                    company=company
                )
                vacancies.append(vacancy)
                
            except Exception as e:
                print(f"Ошибка при создании объекта вакансии: {e}")
                continue
        
        return vacancies 