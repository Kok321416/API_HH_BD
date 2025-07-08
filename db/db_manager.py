import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Tuple, Optional
from dotenv import load_dotenv

load_dotenv()

class DBManager:
    """
    Класс для управления базой данных вакансий и компаний (PostgreSQL).
    """
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("PG_HOST", "localhost"),
            port=os.getenv("PG_PORT", 5432),
            dbname=os.getenv("PG_DATABASE"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
        )
        self.create_tables()

    def create_tables(self):
        """
        Создает таблицы компаний и вакансий, если их нет.
        """
        with self.conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS companies (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    hh_id INTEGER UNIQUE
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    salary INTEGER,
                    description TEXT,
                    requirements TEXT,
                    company_id INTEGER REFERENCES companies(id)
                )
            ''')
            self.conn.commit()

    def close(self):
        self.conn.close()

    def insert_companies(self, companies: List[Tuple[str, int]]):
        """
        Заполняет таблицу компаний (name, hh_id).
        """
        with self.conn.cursor() as cursor:
            for name, hh_id in companies:
                cursor.execute(
                    '''INSERT INTO companies (name, hh_id) VALUES (%s, %s) ON CONFLICT (hh_id) DO NOTHING''',
                    (name, hh_id),
                )
            self.conn.commit()

    def insert_vacancy(
        self,
        title: str,
        url: str,
        salary: Optional[int],
        description: str,
        requirements: str,
        company_hh_id: int,
    ):
        """
        Добавляет вакансию, связывая с компанией по hh_id.
        """
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT id FROM companies WHERE hh_id = %s', (company_hh_id,))
            company = cursor.fetchone()
            if not company:
                return False
            company_id = company[0]
            cursor.execute(
                '''INSERT INTO vacancies (title, url, salary, description, requirements, company_id)
                   VALUES (%s, %s, %s, %s, %s, %s)''',
                (title, url, salary, description, requirements, company_id),
            )
            self.conn.commit()
            return True

    def get_companies_and_vacancy_counts(self) -> List[Tuple[str, int]]:
        """
        Получить список всех компаний и количества вакансий у каждой компании.
        """
        with self.conn.cursor() as cursor:
            cursor.execute('''
                SELECT companies.name, COUNT(vacancies.id) as vacancy_count
                FROM companies
                LEFT JOIN vacancies ON companies.id = vacancies.company_id
                GROUP BY companies.id
            ''')
            return cursor.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, Optional[int], str]]:
        """
        Получить список всех вакансий с названием компании, вакансии, зарплатой и ссылкой.
        """
        with self.conn.cursor() as cursor:
            cursor.execute('''
                SELECT companies.name, vacancies.title, vacancies.salary, vacancies.url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.id
            ''')
            return cursor.fetchall()

    def get_avg_salary(self) -> Optional[float]:
        """
        Получить среднюю зарплату по всем вакансиям.
        """
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL AND salary > 0')
            result = cursor.fetchone()
            return result[0] if result and result[0] is not None else None

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, int, str]]:
        """
        Получить вакансии с зарплатой выше средней.
        """
        avg_salary = self.get_avg_salary()
        if avg_salary is None:
            return []
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''
                SELECT companies.name, vacancies.title, vacancies.salary, vacancies.url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.id
                WHERE vacancies.salary > %s
                ''',
                (avg_salary,),
            )
            return cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, Optional[int], str]]:
        """
        Получить вакансии, в названии которых содержится keyword.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''
                SELECT companies.name, vacancies.title, vacancies.salary, vacancies.url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.id
                WHERE vacancies.title ILIKE %s
                ''',
                (f'%{keyword}%',),
            )
            return cursor.fetchall()
