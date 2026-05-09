import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


class DBCreator:
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

    def create_tables(self):
        """Создание таблиц """
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                id SERIAL PRIMARY KEY,        -- уникальный ID, заполняется автоматически
                hh_id VARCHAR(20) UNIQUE,     -- ID работодателя на hh.ru
                name VARCHAR(255) NOT NULL,   -- название компании
                url VARCHAR(255),             -- ссылка на страницу компании
                description TEXT              -- описание компании
            )
        """)

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,           -- уникальный ID
                employer_id INT REFERENCES employers(id) ON DELETE CASCADE, -- внешний ключ — ссылка на работодателя
                title VARCHAR(255) NOT NULL,     -- название вакансии
                salary_from INT,                 -- зарплата от
                salary_to INT,                   -- зарплата до
                currency VARCHAR(10),            -- валюта (RUR, USD и т.д.)
                url VARCHAR(255)                 -- ссылка на вакансию
            )
        """)

        self.conn.commit()
        print("Таблицы успешно созданы.")

    def drop_tables(self):
        """Функция удаления таблицы, если необходимо"""
        self.cur.execute("DROP TABLE IF EXISTS vacancies CASCADE")
        self.cur.execute("DROP TABLE IF EXISTS employers CASCADE")
        self.conn.commit()
        print("Таблицы удалены.")

    def fill_employers(self, employers: list):
        """Функция заполнения таблицы работодателей"""
        for employer in employers:
            self.cur.execute("""
                INSERT INTO employers (hh_id, name, url, description)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (hh_id) DO NOTHING
            """,
            (
                str(employer.get("id")),           # ID на hh.ru
                employer.get("name"),              # название компании
                employer.get("alternate_url"),     # ссылка на страницу
                employer.get("description", ""),   # описание
            ))

        self.conn.commit()
        print(f"Добавлено работодателей: {len(employers)}")

    def fill_vacancies(self, vacancies: list):
        """Функция заполнения таблицы вакансий"""
        for vacancy in vacancies:

            employer_hh_id = str(vacancy.get("employer", {}).get("id"))
            self.cur.execute(
                "SELECT id FROM employers WHERE hh_id = %s",
                (employer_hh_id,)
            )
            result = self.cur.fetchone()

            if not result:
                continue

            employer_id = result[0]

            salary = vacancy.get("salary") or {}

            self.cur.execute("""
                INSERT INTO vacancies (employer_id, title, salary_from, salary_to, currency, url)
                VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                employer_id,
                vacancy.get("name"),               # название вакансии
                salary.get("from"),                # зарплата от
                salary.get("to"),                  # зарплата до
                salary.get("currency"),            # валюта
                vacancy.get("alternate_url"),      # ссылка на вакансию
            ))

        self.conn.commit()
        print(f"Добавлено вакансий: {len(vacancies)}")

    def close(self):
        self.cur.close()
        self.conn.close()