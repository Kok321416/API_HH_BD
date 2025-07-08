import pytest
from models.vacancy import Vacancy


class TestVacancy:
    """Тесты для класса Vacancy."""

    def test_vacancy_creation(self):
        """Тест создания вакансии с корректными данными."""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123456",
            salary={"from": 100000, "to": 150000},
            description="Разработка на Python",
            requirements="Опыт работы от 3 лет",
            company="TechCorp",
        )

        assert vacancy.title == "Python Developer"
        assert vacancy.url == "https://hh.ru/vacancy/123456"
        assert vacancy.salary == 150000  # Берется максимальная зарплата
        assert vacancy.description == "Разработка на Python"
        assert vacancy.requirements == "Опыт работы от 3 лет"
        assert vacancy.company == "TechCorp"

    def test_vacancy_without_salary(self):
        """Тест создания вакансии без зарплаты."""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123456",
            salary=None,
            description="Разработка на Python",
        )

        assert vacancy.salary == 0

    def test_vacancy_salary_from_only(self):
        """Тест создания вакансии только с минимальной зарплатой."""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123456",
            salary={"from": 100000},
            description="Разработка на Python",
        )

        assert vacancy.salary == 100000

    def test_vacancy_comparison(self):
        """Тест сравнения вакансий по зарплате."""
        vacancy1 = Vacancy(
            title="Junior Python Developer",
            url="https://hh.ru/vacancy/1",
            salary={"from": 50000, "to": 80000},
            description="Junior position",
        )

        vacancy2 = Vacancy(
            title="Senior Python Developer",
            url="https://hh.ru/vacancy/2",
            salary={"from": 150000, "to": 200000},
            description="Senior position",
        )

        vacancy3 = Vacancy(
            title="Middle Python Developer",
            url="https://hh.ru/vacancy/3",
            salary={"from": 100000, "to": 120000},
            description="Middle position",
        )

        # Тестируем операторы сравнения
        assert vacancy1 < vacancy2
        assert vacancy2 > vacancy1
        assert vacancy1 <= vacancy3
        assert vacancy2 >= vacancy3
        assert vacancy1 != vacancy2
        assert vacancy1 == vacancy1

    def test_vacancy_validation_title(self):
        """Тест валидации названия вакансии."""
        with pytest.raises(
            ValueError, match="Название вакансии должно быть непустой строкой"
        ):
            Vacancy(
                title="",
                url="https://hh.ru/vacancy/123456",
                salary=None,
                description="Description",
            )

        with pytest.raises(
            ValueError, match="Название вакансии должно быть непустой строкой"
        ):
            Vacancy(
                title=None,
                url="https://hh.ru/vacancy/123456",
                salary=None,
                description="Description",
            )

    def test_vacancy_validation_url(self):
        """Тест валидации URL вакансии."""
        with pytest.raises(
            ValueError, match="URL вакансии должен быть непустой строкой"
        ):
            Vacancy(
                title="Python Developer", url="", salary=None, description="Description"
            )

    def test_vacancy_string_representation(self):
        """Тест строкового представления вакансии."""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123456",
            salary={"from": 100000, "to": 150000},
            description="Разработка на Python",
            company="TechCorp",
        )

        expected = "Python Developer | TechCorp | 150,000 руб."
        assert str(vacancy) == expected

    def test_vacancy_without_salary_string_representation(self):
        """Тест строкового представления вакансии без зарплаты."""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123456",
            salary=None,
            description="Разработка на Python",
            company="TechCorp",
        )

        expected = "Python Developer | TechCorp | Зарплата не указана"
        assert str(vacancy) == expected

    def test_cast_to_object_list(self):
        """Тест преобразования JSON в список объектов Vacancy."""
        vacancies_json = [
            {
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/123456",
                "salary": {"from": 100000, "to": 150000},
                "snippet": {"requirement": "Опыт работы от 3 лет"},
                "employer": {"name": "TechCorp"},
            },
            {
                "name": "Java Developer",
                "alternate_url": "https://hh.ru/vacancy/789012",
                "salary": None,
                "snippet": {"requirement": "Опыт работы от 2 лет"},
                "employer": {"name": "JavaCorp"},
            },
        ]

        vacancies = Vacancy.cast_to_object_list(vacancies_json)

        assert len(vacancies) == 2
        assert vacancies[0].title == "Python Developer"
        assert vacancies[0].salary == 150000
        assert vacancies[1].title == "Java Developer"
        assert vacancies[1].salary == 0

    def test_cast_to_object_list_empty(self):
        """Тест преобразования пустого JSON в список объектов."""
        vacancies = Vacancy.cast_to_object_list([])
        assert len(vacancies) == 0

    def test_cast_to_object_list_invalid_data(self):
        """Тест обработки некорректных данных при преобразовании."""
        vacancies_json = [
            {
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/123456",
                "salary": {"from": 100000, "to": 150000},
                "snippet": {"requirement": "Опыт работы от 3 лет"},
                "employer": {"name": "TechCorp"},
            },
            {
                # Некорректные данные - отсутствует обязательное поле
                "salary": {"from": 50000}
            },
        ]

        vacancies = Vacancy.cast_to_object_list(vacancies_json)

        # Должна быть создана только одна вакансия
        assert len(vacancies) == 1
        assert vacancies[0].title == "Python Developer"
