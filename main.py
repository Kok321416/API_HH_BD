from api.hh_api import HeadHunterAPI
from models.vacancy import Vacancy
from storage.json_saver import JSONSaver
from utils.filters import (
    filter_vacancies, 
    get_vacancies_by_salary, 
    sort_vacancies, 
    get_top_vacancies, 
    print_vacancies,
    print_statistics
)
from db.db_manager import DBManager


def user_interaction():
    """
    Функция для взаимодействия с пользователем через консоль.
    Предоставляет возможности поиска, фильтрации и работы с вакансиями и БД.
    """
    print("=" * 60)
    print("ПРОГРАММА ДЛЯ РАБОТЫ С ВАКАНСИЯМИ С HH.RU")
    print("=" * 60)
    
    # Инициализация компонентов
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()
    db_manager = DBManager()
    
    # Заполнение компаний (пример 10 компаний с hh_id)
    companies = [
        ("Яндекс", 1740),
        ("Сбер", 3529),
        ("Тинькофф", 78638),
        ("VK", 15478),
        ("Ozon", 2180),
        ("Mail.ru Group", 3776),
        ("Альфа-Банк", 80),
        ("Газпромбанк", 4642),
        ("Росатом", 907345),
        ("Ростелеком", 2748)
    ]
    db_manager.insert_companies(companies)
    
    while True:
        print("\nВыберите действие:")
        print("1. Поиск вакансий на hh.ru и сохранение в файл")
        print("2. Показать сохраненные вакансии (файл)")
        print("3. Фильтровать вакансии по ключевым словам (файл)")
        print("4. Получить топ N вакансий по зарплате (файл)")
        print("5. Фильтровать по диапазону зарплат (файл)")
        print("6. Показать статистику (файл)")
        print("7. Очистить все сохраненные вакансии (файл)")
        print("8. Загрузить вакансии компаний в БД (hh.ru → БД)")
        print("9. Показать компании и количество вакансий (БД)")
        print("10. Показать все вакансии (БД)")
        print("11. Показать среднюю зарплату (БД)")
        print("12. Показать вакансии с зарплатой выше средней (БД)")
        print("13. Поиск вакансий по ключевому слову (БД)")
        print("0. Выход")
        
        choice = input("\nВведите номер действия: ").strip()
        
        if choice == "1":
            search_vacancies(hh_api, json_saver)
        elif choice == "2":
            show_saved_vacancies(json_saver)
        elif choice == "3":
            filter_by_keywords(json_saver)
        elif choice == "4":
            get_top_vacancies_by_salary(json_saver)
        elif choice == "5":
            filter_by_salary_range(json_saver)
        elif choice == "6":
            show_statistics(json_saver)
        elif choice == "7":
            clear_vacancies(json_saver)
        elif choice == "8":
            load_vacancies_to_db(hh_api, db_manager, companies)
        elif choice == "9":
            show_companies_and_vacancy_counts(db_manager)
        elif choice == "10":
            show_all_vacancies_db(db_manager)
        elif choice == "11":
            show_avg_salary_db(db_manager)
        elif choice == "12":
            show_vacancies_higher_salary_db(db_manager)
        elif choice == "13":
            search_vacancies_by_keyword_db(db_manager)
        elif choice == "0":
            db_manager.close()
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def search_vacancies(hh_api: HeadHunterAPI, json_saver: JSONSaver):
    """Поиск вакансий на hh.ru и сохранение результатов."""
    search_query = input("Введите поисковый запрос: ").strip()
    
    if not search_query:
        print("Поисковый запрос не может быть пустым.")
        return
    
    print(f"Поиск вакансий по запросу: '{search_query}'...")
    
    # Получение вакансий с hh.ru
    hh_vacancies = hh_api.get_vacancies(search_query)
    
    if not hh_vacancies:
        print("Вакансии не найдены.")
        return
    
    # Преобразование в объекты Vacancy
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
    
    print(f"Найдено {len(vacancies_list)} вакансий.")
    
    # Сохранение в файл
    added_count = json_saver.add_vacancies(vacancies_list)
    print(f"Сохранено {added_count} новых вакансий.")
    
    # Показ первых 5 вакансий
    print("\nПервые 5 найденных вакансий:")
    print_vacancies(vacancies_list[:5])


def show_saved_vacancies(json_saver: JSONSaver):
    """Показать все сохраненные вакансии."""
    vacancies = json_saver.get_vacancies()
    
    if not vacancies:
        print("Сохраненных вакансий нет.")
        return
    
    print_vacancies(vacancies)


def filter_by_keywords(json_saver: JSONSaver):
    """Фильтрация вакансий по ключевым словам."""
    filter_words_input = input("Введите ключевые слова через пробел: ").strip()
    
    if not filter_words_input:
        print("Ключевые слова не указаны.")
        return
    
    filter_words = filter_words_input.split()
    vacancies = json_saver.get_vacancies()
    
    if not vacancies:
        print("Сохраненных вакансий нет.")
        return
    
    filtered_vacancies = filter_vacancies(vacancies, filter_words)
    print_vacancies(filtered_vacancies)


def get_top_vacancies_by_salary(json_saver: JSONSaver):
    """Получить топ N вакансий по зарплате."""
    try:
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
        if top_n <= 0:
            print("Количество должно быть положительным числом.")
            return
    except ValueError:
        print("Неверный формат числа.")
        return
    
    vacancies = json_saver.get_vacancies()
    
    if not vacancies:
        print("Сохраненных вакансий нет.")
        return
    
    top_vacancies = get_top_vacancies(vacancies, top_n)
    print_vacancies(top_vacancies)


def filter_by_salary_range(json_saver: JSONSaver):
    """Фильтрация вакансий по диапазону зарплат."""
    salary_range = input("Введите диапазон зарплат (например: 50000-150000 или 100000): ").strip()
    
    if not salary_range:
        print("Диапазон зарплат не указан.")
        return
    
    vacancies = json_saver.get_vacancies()
    
    if not vacancies:
        print("Сохраненных вакансий нет.")
        return
    
    filtered_vacancies = get_vacancies_by_salary(vacancies, salary_range)
    print_vacancies(filtered_vacancies)


def show_statistics(json_saver: JSONSaver):
    """Показать статистику по сохраненным вакансиям."""
    vacancies = json_saver.get_vacancies()
    
    if not vacancies:
        print("Сохраненных вакансий нет.")
        return
    
    print_statistics(vacancies)


def clear_vacancies(json_saver: JSONSaver):
    """Очистить все сохраненные вакансии."""
    confirm = input("Вы уверены, что хотите удалить все вакансии? (да/нет): ").strip().lower()
    
    if confirm in ['да', 'yes', 'y']:
        if json_saver.clear_all():
            print("Все вакансии удалены.")
        else:
            print("Ошибка при удалении вакансий.")
    else:
        print("Операция отменена.")


def load_vacancies_to_db(hh_api, db_manager, companies):
    print("Загрузка вакансий для 10 компаний...")
    for name, hh_id in companies:
        print(f"\nКомпания: {name}")
        vacancies = hh_api.get_vacancies(name)
        if not vacancies:
            print("  Нет вакансий.")
            continue
        for v in vacancies:
            title = v.get("name", "")
            url = v.get("alternate_url", "")
            salary = v.get("salary")
            # Вытаскиваем максимальную зарплату, если есть
            if isinstance(salary, dict):
                if salary.get("to") is not None:
                    salary_val = salary["to"]
                elif salary.get("from") is not None:
                    salary_val = salary["from"]
                else:
                    salary_val = None
            else:
                salary_val = None
            description = v.get("snippet", {}).get("requirement", "")
            requirements = v.get("snippet", {}).get("requirement", "")
            db_manager.insert_vacancy(title, url, salary_val, description, requirements, hh_id)
        print(f"  Загружено: {len(vacancies)} вакансий.")
    print("\nЗагрузка завершена!")


def show_companies_and_vacancy_counts(db_manager):
    data = db_manager.get_companies_and_vacancy_counts()
    print("\nКомпании и количество вакансий:")
    for name, count in data:
        print(f"  {name}: {count}")


def show_all_vacancies_db(db_manager):
    data = db_manager.get_all_vacancies()
    print("\nВакансии:")
    for name, title, salary, url in data:
        salary_str = f"{salary:,} руб." if salary else "Зарплата не указана"
        print(f"  {name} | {title} | {salary_str} | {url}")


def show_avg_salary_db(db_manager):
    avg = db_manager.get_avg_salary()
    if avg:
        print(f"\nСредняя зарплата по вакансиям: {int(avg):,} руб.")
    else:
        print("\nНет данных о зарплатах.")


def show_vacancies_higher_salary_db(db_manager):
    data = db_manager.get_vacancies_with_higher_salary()
    print("\nВакансии с зарплатой выше средней:")
    for name, title, salary, url in data:
        print(f"  {name} | {title} | {salary:,} руб. | {url}")


def search_vacancies_by_keyword_db(db_manager):
    keyword = input("Введите ключевое слово для поиска в названии вакансии: ").strip()
    if not keyword:
        print("Ключевое слово не указано.")
        return
    data = db_manager.get_vacancies_with_keyword(keyword)
    print(f"\nВакансии с ключевым словом '{keyword}':")
    for name, title, salary, url in data:
        salary_str = f"{salary:,} руб." if salary else "Зарплата не указана"
        print(f"  {name} | {title} | {salary_str} | {url}")


def main():
    """Главная функция программы."""
    try:
        user_interaction()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")


if __name__ == "__main__":
    main() 