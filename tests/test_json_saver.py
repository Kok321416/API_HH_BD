import pytest
import json
import os
import tempfile
from models.vacancy import Vacancy
from storage.json_saver import JSONSaver


class TestJSONSaver:
    """Тесты для класса JSONSaver."""
    
    def setup_method(self):
        """Настройка перед каждым тестом."""
        # Создаем временный файл для тестов
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_filename = self.temp_file.name
        self.temp_file.close()
        
        # Создаем экземпляр JSONSaver с временным файлом
        self.json_saver = JSONSaver(self.temp_filename)
    
    def teardown_method(self):
        """Очистка после каждого теста."""
        # Удаляем временный файл
        if os.path.exists(self.temp_filename):
            os.unlink(self.temp_filename)
    
    def test_init_creates_file(self):
        """Тест создания файла при инициализации."""
        assert os.path.exists(self.temp_filename)
        
        with open(self.temp_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert data == []
    
    def test_add_vacancy(self):
        """Тест добавления вакансии."""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123456",
            salary={"from": 100000, "to": 150000},
            description="Разработка на Python",
            company="TechCorp"
        )
        
        result = self.json_saver.add_vacancy(vacancy)
        assert result is True
        
        # Проверяем, что вакансия сохранена в файле
        with open(self.temp_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert len(data) == 1
            assert data[0]["title"] == "Python Developer"
            assert data[0]["salary"] == 150000
    
    def test_add_duplicate_vacancy(self):
        """Тест добавления дублирующейся вакансии."""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123456",
            salary={"from": 100000, "to": 150000},
            description="Разработка на Python"
        )
        
        # Добавляем вакансию первый раз
        result1 = self.json_saver.add_vacancy(vacancy)
        assert result1 is True
        
        # Пытаемся добавить ту же вакансию второй раз
        result2 = self.json_saver.add_vacancy(vacancy)
        assert result2 is False
        
        # Проверяем, что в файле только одна вакансия
        with open(self.temp_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert len(data) == 1
    
    def test_get_vacancies(self):
        """Тест получения вакансий."""
        # Добавляем несколько вакансий
        vacancy1 = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/1",
            salary={"from": 100000, "to": 150000},
            description="Python разработка",
            company="TechCorp"
        )
        
        vacancy2 = Vacancy(
            title="Java Developer",
            url="https://hh.ru/vacancy/2",
            salary={"from": 80000, "to": 120000},
            description="Java разработка",
            company="JavaCorp"
        )
        
        self.json_saver.add_vacancy(vacancy1)
        self.json_saver.add_vacancy(vacancy2)
        
        # Получаем все вакансии
        vacancies = self.json_saver.get_vacancies()
        assert len(vacancies) == 2
        assert vacancies[0].title == "Python Developer"
        assert vacancies[1].title == "Java Developer"
    
    def test_get_vacancies_with_keyword_filter(self):
        """Тест получения вакансий с фильтром по ключевому слову."""
        vacancy1 = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/1",
            salary={"from": 100000, "to": 150000},
            description="Python разработка",
            company="TechCorp"
        )
        
        vacancy2 = Vacancy(
            title="Java Developer",
            url="https://hh.ru/vacancy/2",
            salary={"from": 80000, "to": 120000},
            description="Java разработка",
            company="JavaCorp"
        )
        
        self.json_saver.add_vacancy(vacancy1)
        self.json_saver.add_vacancy(vacancy2)
        
        # Фильтруем по ключевому слову "Python"
        vacancies = self.json_saver.get_vacancies(keyword="Python")
        assert len(vacancies) == 1
        assert vacancies[0].title == "Python Developer"
    
    def test_get_vacancies_with_salary_filter(self):
        """Тест получения вакансий с фильтром по зарплате."""
        vacancy1 = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/1",
            salary={"from": 100000, "to": 150000},
            description="Python разработка"
        )
        
        vacancy2 = Vacancy(
            title="Java Developer",
            url="https://hh.ru/vacancy/2",
            salary={"from": 80000, "to": 120000},
            description="Java разработка"
        )
        
        self.json_saver.add_vacancy(vacancy1)
        self.json_saver.add_vacancy(vacancy2)
        
        # Фильтруем по минимальной зарплате
        vacancies = self.json_saver.get_vacancies(min_salary=110000)
        assert len(vacancies) == 1
        assert vacancies[0].title == "Python Developer"
        
        # Фильтруем по максимальной зарплате
        vacancies = self.json_saver.get_vacancies(max_salary=90000)
        assert len(vacancies) == 1
        assert vacancies[0].title == "Java Developer"
    
    def test_delete_vacancy(self):
        """Тест удаления вакансии."""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123456",
            salary={"from": 100000, "to": 150000},
            description="Разработка на Python"
        )
        
        # Добавляем вакансию
        self.json_saver.add_vacancy(vacancy)
        
        # Удаляем вакансию
        result = self.json_saver.delete_vacancy(vacancy)
        assert result is True
        
        # Проверяем, что вакансия удалена
        vacancies = self.json_saver.get_vacancies()
        assert len(vacancies) == 0
    
    def test_delete_nonexistent_vacancy(self):
        """Тест удаления несуществующей вакансии."""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123456",
            salary={"from": 100000, "to": 150000},
            description="Разработка на Python"
        )
        
        result = self.json_saver.delete_vacancy(vacancy)
        assert result is False
    
    def test_clear_all(self):
        """Тест очистки всех вакансий."""
        # Добавляем несколько вакансий
        vacancy1 = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/1",
            salary={"from": 100000, "to": 150000},
            description="Python разработка"
        )
        
        vacancy2 = Vacancy(
            title="Java Developer",
            url="https://hh.ru/vacancy/2",
            salary={"from": 80000, "to": 120000},
            description="Java разработка"
        )
        
        self.json_saver.add_vacancy(vacancy1)
        self.json_saver.add_vacancy(vacancy2)
        
        # Очищаем все вакансии
        result = self.json_saver.clear_all()
        assert result is True
        
        # Проверяем, что все вакансии удалены
        vacancies = self.json_saver.get_vacancies()
        assert len(vacancies) == 0
    
    def test_add_vacancies(self):
        """Тест добавления нескольких вакансий."""
        vacancies = [
            Vacancy(
                title="Python Developer",
                url="https://hh.ru/vacancy/1",
                salary={"from": 100000, "to": 150000},
                description="Python разработка"
            ),
            Vacancy(
                title="Java Developer",
                url="https://hh.ru/vacancy/2",
                salary={"from": 80000, "to": 120000},
                description="Java разработка"
            )
        ]
        
        added_count = self.json_saver.add_vacancies(vacancies)
        assert added_count == 2
        
        # Проверяем, что вакансии сохранены
        saved_vacancies = self.json_saver.get_vacancies()
        assert len(saved_vacancies) == 2 