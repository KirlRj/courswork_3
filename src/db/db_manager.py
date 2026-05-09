import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")


class DBManager:
    def __init__(self):
        """Определение переменных для подключения к БД"""
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> list:
        """Функция Получения списка всех компаний и количество вакансий у каждой"""
        self.cur.execute("""
            SELECT e.name, COUNT(v.id) AS vacancies_count
            FROM employers e
            LEFT JOIN vacancies v ON e.id = v.employer_id
            GROUP BY e.name
            ORDER BY vacancies_count DESC
        """)
        return self.cur.fetchall()

    def get_all_vacancies(self) -> list:
        """Функция получения всех вакансий с названием компании, зарплатой и ссылкой"""
        self.cur.execute("""
            SELECT 
                e.name AS company,
                v.title AS vacancy,
                COALESCE(v.salary_from, 0) AS salary_from,
                COALESCE(v.salary_to, 0) AS salary_to,
                v.currency,
                v.url
            FROM vacancies v
            JOIN employers e ON e.id = v.employer_id
            ORDER BY e.name
        """)
        return self.cur.fetchall()

    def get_avg_salary(self) -> float:
        """Функция получения средней зарплаты по всем вакансиям"""

        self.cur.execute("""
            SELECT ROUND(AVG(
                COALESCE(salary_from, salary_to, 0)
            ), 2)
            FROM vacancies
            WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
        """)
        result = self.cur.fetchone()
        return result[0] if result else 0

    def get_vacancies_with_higher_salary(self) -> list:
        """Функция получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        self.cur.execute("""
            SELECT
                e.name AS company,
                v.title AS vacancy,
                COALESCE(v.salary_from, 0) AS salary_from,
                COALESCE(v.salary_to, 0) AS salary_to,
                v.currency,
                v.url
            FROM vacancies v
            JOIN employers e ON e.id = v.employer_id
            WHERE COALESCE(v.salary_from, v.salary_to, 0) > (
                SELECT AVG(COALESCE(salary_from, salary_to, 0))
                FROM vacancies
                WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
            )
            ORDER BY salary_from DESC
        """)
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> list:
        """Функция получения списка всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        self.cur.execute(
            """
            SELECT
                e.name AS company,
                v.title AS vacancy,
                COALESCE(v.salary_from, 0) AS salary_from,
                COALESCE(v.salary_to, 0) AS salary_to,
                v.currency,
                v.url
            FROM vacancies v
            JOIN employers e ON e.id = v.employer_id
            WHERE v.title ILIKE %s
            ORDER BY e.name
        """,
            (f"%{keyword}%",),
        )
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
