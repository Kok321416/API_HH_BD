from models.vacancy import Vacancy
from utils.filters import (
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
    get_vacancies_statistics,
)


class TestFilters:
    """Тесты для функций фильтрации и работы с вакансиями."""

    def setup_method(self):
        """Настройка перед каждым тестом."""
        self.vacancies = [
            Vacancy(
                title="Python Developer",
                url="https://hh.ru/vacancy/1",
                salary={"from": 100000, "to": 150000},
                description="Разработка на Python, Django, Flask",
                requirements="Опыт работы от 3 лет, знание Python",
                company="TechCorp",
            ),
            Vacancy(
                title="Java Developer",
                url="https://hh.ru/vacancy/2",
                salary={"from": 80000, "to": 120000},
                description="Разработка на Java, Spring",
                requirements="Опыт работы от 2 лет, знание Java",
                company="JavaCorp",
            ),
            Vacancy(
                title="Frontend Developer",
                url="https://hh.ru/vacancy/3",
                salary={"from": 60000, "to": 100000},
                description="Разработка на JavaScript, React",
                requirements="Опыт работы от 1 года, знание JavaScript",
                company="WebCorp",
            ),
            Vacancy(
                title="DevOps Engineer",
                url="https://hh.ru/vacancy/4",
                salary=None,
                description="Настройка CI/CD, Docker, Kubernetes",
                requirements="Опыт работы с Docker, Kubernetes",
                company="DevOpsCorp",
            ),
        ]

    def test_filter_vacancies_with_keywords(self):
        """Тест фильтрации вакансий по ключевым словам."""
        filter_words = ["Python", "Django"]
        filtered = filter_vacancies(self.vacancies, filter_words)

        assert len(filtered) == 1
        assert filtered[0].title == "Python Developer"

    def test_filter_vacancies_with_multiple_keywords(self):
        """Тест фильтрации вакансий по нескольким ключевым словам."""
        filter_words = ["Java", "Spring"]
        filtered = filter_vacancies(self.vacancies, filter_words)

        assert len(filtered) == 1
        assert filtered[0].title == "Java Developer"

    def test_filter_vacancies_no_matches(self):
        """Тест фильтрации вакансий без совпадений."""
        filter_words = ["C++", "Qt"]
        filtered = filter_vacancies(self.vacancies, filter_words)

        assert len(filtered) == 0

    def test_filter_vacancies_empty_keywords(self):
        """Тест фильтрации вакансий с пустыми ключевыми словами."""
        filter_words = []
        filtered = filter_vacancies(self.vacancies, filter_words)

        assert len(filtered) == len(self.vacancies)

    def test_get_vacancies_by_salary_range(self):
        """Тест фильтрации вакансий по диапазону зарплат."""
        salary_range = "80000-120000"
        filtered = get_vacancies_by_salary(self.vacancies, salary_range)

        assert len(filtered) == 2
        assert filtered[0].title == "Python Developer"
        assert filtered[1].title == "Java Developer"

    def test_get_vacancies_by_min_salary(self):
        """Тест фильтрации вакансий по минимальной зарплате."""
        salary_range = "100000"
        filtered = get_vacancies_by_salary(self.vacancies, salary_range)

        assert len(filtered) == 1
        assert filtered[0].title == "Python Developer"

    def test_get_vacancies_by_salary_no_matches(self):
        """Тест фильтрации вакансий по зарплате без совпадений."""
        salary_range = "200000-300000"
        filtered = get_vacancies_by_salary(self.vacancies, salary_range)

        assert len(filtered) == 0

    def test_get_vacancies_by_salary_invalid_format(self):
        """Тест фильтрации вакансий по некорректному формату зарплаты."""
        salary_range = "invalid"
        filtered = get_vacancies_by_salary(self.vacancies, salary_range)

        # Должны вернуться все вакансии при некорректном формате
        assert len(filtered) == len(self.vacancies)

    def test_sort_vacancies_descending(self):
        """Тест сортировки вакансий по убыванию зарплаты."""
        sorted_vacancies = sort_vacancies(self.vacancies, reverse=True)

        assert len(sorted_vacancies) == 4
        assert sorted_vacancies[0].title == "Python Developer"  # 150000
        assert sorted_vacancies[1].title == "Java Developer"  # 120000
        assert sorted_vacancies[2].title == "Frontend Developer"  # 100000
        assert sorted_vacancies[3].title == "DevOps Engineer"  # 0

    def test_sort_vacancies_ascending(self):
        """Тест сортировки вакансий по возрастанию зарплаты."""
        sorted_vacancies = sort_vacancies(self.vacancies, reverse=False)

        assert len(sorted_vacancies) == 4
        assert sorted_vacancies[0].title == "DevOps Engineer"  # 0
        assert sorted_vacancies[1].title == "Frontend Developer"  # 100000
        assert sorted_vacancies[2].title == "Java Developer"  # 120000
        assert sorted_vacancies[3].title == "Python Developer"  # 150000

    def test_get_top_vacancies(self):
        """Тест получения топ N вакансий по зарплате."""
        top_vacancies = get_top_vacancies(self.vacancies, 2)

        assert len(top_vacancies) == 2
        assert top_vacancies[0].title == "Python Developer"  # 150000
        assert top_vacancies[1].title == "Java Developer"  # 120000

    def test_get_top_vacancies_more_than_available(self):
        """Тест получения топ N вакансий, где N больше количества вакансий."""
        top_vacancies = get_top_vacancies(self.vacancies, 10)

        assert len(top_vacancies) == 4

    def test_get_top_vacancies_zero(self):
        """Тест получения топ 0 вакансий."""
        top_vacancies = get_top_vacancies(self.vacancies, 0)

        assert len(top_vacancies) == 0

    def test_get_vacancies_statistics(self):
        """Тест получения статистики по вакансиям."""
        stats = get_vacancies_statistics(self.vacancies)

        assert stats["total_count"] == 4
        assert stats["with_salary_count"] == 3
        assert stats["avg_salary"] == 123333  # (150000 + 120000 + 100000) / 3
        assert stats["max_salary"] == 150000
        assert stats["min_salary"] == 100000

    def test_get_vacancies_statistics_empty(self):
        """Тест получения статистики по пустому списку вакансий."""
        stats = get_vacancies_statistics([])

        assert stats["total_count"] == 0
        assert stats["with_salary_count"] == 0
        assert stats["avg_salary"] == 0
        assert stats["max_salary"] == 0
        assert stats["min_salary"] == 0

    def test_get_vacancies_statistics_no_salary(self):
        """Тест получения статистики по вакансиям без зарплат."""
        vacancies_no_salary = [
            Vacancy(
                title="Intern",
                url="https://hh.ru/vacancy/5",
                salary=None,
                description="Стажировка",
            )
        ]

        stats = get_vacancies_statistics(vacancies_no_salary)

        assert stats["total_count"] == 1
        assert stats["with_salary_count"] == 0
        assert stats["avg_salary"] == 0
        assert stats["max_salary"] == 0
        assert stats["min_salary"] == 0
