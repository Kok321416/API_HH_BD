import sqlite3
from typing import List, Tuple, Optional


class DBManager:
    """
    Класс для управления базой данных вакансий и компаний.
    """

    def __init__(self, db_name: str = "vacancies.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_tables()

    def create_tables(self):
        """
        Создает таблицы компаний и вакансий, если их нет.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                hh_id INTEGER UNIQUE
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS vacancies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                salary INTEGER,
                description TEXT,
                requirements TEXT,
                company_id INTEGER,
                FOREIGN KEY(company_id) REFERENCES companies(id)
            )
        """
        )
        self.conn.commit()

    def close(self):
        self.conn.close()

    def insert_companies(self, companies: List[Tuple[str, int]]):
        """
        Заполняет таблицу компаний (name, hh_id).
        """
        cursor = self.conn.cursor()
        for name, hh_id in companies:
            cursor.execute(
                """
                INSERT OR IGNORE INTO companies (name, hh_id) VALUES (?, ?)
            """,
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
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM companies WHERE hh_id = ?", (company_hh_id,))
        company = cursor.fetchone()
        if not company:
            return False
        company_id = company[0]
        cursor.execute(
            """
            INSERT INTO vacancies (title, url, salary, description, requirements, company_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (title, url, salary, description, requirements, company_id),
        )
        self.conn.commit()
        return True

    def get_companies_and_vacancy_counts(self) -> List[Tuple[str, int]]:
        """
        Получить список всех компаний и количества вакансий у каждой компании.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT companies.name, COUNT(vacancies.id) as vacancy_count
            FROM companies
            LEFT JOIN vacancies ON companies.id = vacancies.company_id
            GROUP BY companies.id
        """
        )
        return cursor.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, Optional[int], str]]:
        """
        Получить список всех вакансий с названием компании, вакансии, зарплатой и ссылкой.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT companies.name, vacancies.title, vacancies.salary, vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id
        """
        )
        return cursor.fetchall()

    def get_avg_salary(self) -> Optional[float]:
        """
        Получить среднюю зарплату по всем вакансиям.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL AND salary > 0"
        )
        result = cursor.fetchone()
        return result[0] if result and result[0] is not None else None

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, int, str]]:
        """
        Получить вакансии с зарплатой выше средней.
        """
        avg_salary = self.get_avg_salary()
        if avg_salary is None:
            return []
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT companies.name, vacancies.title, vacancies.salary, vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id
            WHERE vacancies.salary > ?
        """,
            (avg_salary,),
        )
        return cursor.fetchall()

    def get_vacancies_with_keyword(
        self, keyword: str
    ) -> List[Tuple[str, str, Optional[int], str]]:
        """
        Получить вакансии, в названии которых содержится keyword.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT companies.name, vacancies.title, vacancies.salary, vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id
            WHERE vacancies.title LIKE ?
            """,
            (f"%{keyword}%",),
        )
        return cursor.fetchall()
