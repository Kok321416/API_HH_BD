from typing import List, Optional
from models.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """
    Фильтровать вакансии по ключевым словам.
    
    Args:
        vacancies (List[Vacancy]): Список вакансий для фильтрации
        filter_words (List[str]): Список ключевых слов для поиска
        
    Returns:
        List[Vacancy]: Отфильтрованный список вакансий
    """
    if not filter_words:
        return vacancies
    
    filtered_vacancies = []
    for vacancy in vacancies:
        # Проверяем, содержит ли вакансия хотя бы одно ключевое слово
        vacancy_text = f"{vacancy.title} {vacancy.description} {vacancy.requirements}".lower()
        
        for word in filter_words:
            if word.lower() in vacancy_text:
                filtered_vacancies.append(vacancy)
                break
    
    return filtered_vacancies


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """
    Фильтровать вакансии по диапазону зарплат.
    
    Args:
        vacancies (List[Vacancy]): Список вакансий для фильтрации
        salary_range (str): Диапазон зарплат в формате "min-max" или "min"
        
    Returns:
        List[Vacancy]: Отфильтрованный список вакансий
    """
    if not salary_range:
        return vacancies
    
    try:
        # Парсим диапазон зарплат
        if "-" in salary_range:
            min_salary, max_salary = map(int, salary_range.split("-"))
        else:
            min_salary = int(salary_range)
            max_salary = float('inf')
        
        filtered_vacancies = []
        for vacancy in vacancies:
            if min_salary <= vacancy.salary <= max_salary:
                filtered_vacancies.append(vacancy)
        
        return filtered_vacancies
        
    except ValueError:
        print("Неверный формат диапазона зарплат. Используйте формат 'min-max' или 'min'")
        return vacancies


def sort_vacancies(vacancies: List[Vacancy], reverse: bool = True) -> List[Vacancy]:
    """
    Сортировать вакансии по зарплате.
    
    Args:
        vacancies (List[Vacancy]): Список вакансий для сортировки
        reverse (bool): True для сортировки по убыванию, False по возрастанию
        
    Returns:
        List[Vacancy]: Отсортированный список вакансий
    """
    return sorted(vacancies, reverse=reverse)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Получить топ N вакансий по зарплате.
    
    Args:
        vacancies (List[Vacancy]): Список вакансий
        top_n (int): Количество вакансий для вывода
        
    Returns:
        List[Vacancy]: Топ N вакансий
    """
    sorted_vacancies = sort_vacancies(vacancies)
    return sorted_vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]):
    """
    Вывести вакансии в консоль.
    
    Args:
        vacancies (List[Vacancy]): Список вакансий для вывода
    """
    if not vacancies:
        print("Вакансии не найдены.")
        return
    
    print(f"\nНайдено вакансий: {len(vacancies)}")
    print("=" * 80)
    
    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{i}. {vacancy.title}")
        print(f"   Компания: {vacancy.company}")
        print(f"   Зарплата: {vacancy.salary:,} руб." if vacancy.salary > 0 else "   Зарплата: Зарплата не указана")
        print(f"   Описание: {vacancy.description[:100]}..." if len(vacancy.description) > 100 else f"   Описание: {vacancy.description}")
        print(f"   Ссылка: {vacancy.url}")
        print("-" * 80)


def get_vacancies_statistics(vacancies: List[Vacancy]) -> dict:
    """
    Получить статистику по вакансиям.
    
    Args:
        vacancies (List[Vacancy]): Список вакансий
        
    Returns:
        dict: Статистика по вакансиям
    """
    if not vacancies:
        return {
            "total_count": 0,
            "with_salary_count": 0,
            "avg_salary": 0,
            "max_salary": 0,
            "min_salary": 0
        }
    
    with_salary = [v for v in vacancies if v.salary > 0]
    
    stats = {
        "total_count": len(vacancies),
        "with_salary_count": len(with_salary),
        "avg_salary": 0,
        "max_salary": 0,
        "min_salary": 0
    }
    
    if with_salary:
        salaries = [v.salary for v in with_salary]
        stats["avg_salary"] = sum(salaries) // len(salaries)
        stats["max_salary"] = max(salaries)
        stats["min_salary"] = min(salaries)
    
    return stats


def print_statistics(vacancies: List[Vacancy]):
    """
    Вывести статистику по вакансиям.
    
    Args:
        vacancies (List[Vacancy]): Список вакансий
    """
    stats = get_vacancies_statistics(vacancies)
    
    print("\n" + "=" * 50)
    print("СТАТИСТИКА ПО ВАКАНСИЯМ")
    print("=" * 50)
    print(f"Всего вакансий: {stats['total_count']}")
    print(f"С указанной зарплатой: {stats['with_salary_count']}")
    
    if stats['with_salary_count'] > 0:
        print(f"Средняя зарплата: {stats['avg_salary']:,} руб.")
        print(f"Максимальная зарплата: {stats['max_salary']:,} руб.")
        print(f"Минимальная зарплата: {stats['min_salary']:,} руб.")
    
    print("=" * 50) 