from src.api.hh_api import HHAPI
from src.db.db_creator import DBCreator
from src.db.db_manager import DBManager


def main():
    print("=== Курсовая работа. Работа с БД ===\n")

    print("Получаем данные с hh.ru...")
    api = HHAPI()
    employers, vacancies = api.get_all_employers_and_vacancies()
    print(employers[0])
    print(f"Получено работодателей: {len(employers)}")
    print(f"Получено вакансий: {len(vacancies)}\n")

    print("Создаём таблицы и заполняем данными...")
    creator = DBCreator()
    creator.drop_tables()
    creator.create_tables()
    creator.fill_employers(employers)
    creator.fill_vacancies(vacancies)
    creator.close()
    print()

    db = DBManager()

    while True:
        print("=== Меню ===")
        print("1 — Список компаний и количество вакансий")
        print("2 — Все вакансии")
        print("3 — Средняя зарплата")
        print("4 — Вакансии с зарплатой выше средней")
        print("5 — Поиск вакансий по ключевому слову")
        print("0 — Выход")

        choice = input("\nВыберите пункт: ").strip()

        if choice == "1":
            print("\n--- Компании и количество вакансий ---")
            results = db.get_companies_and_vacancies_count()
            for company, count in results:
                print(f"{company}: {count} вакансий")

        elif choice == "2":
            print("\n--- Все вакансии ---")
            results = db.get_all_vacancies()
            for company, title, salary_from, salary_to, currency, url in results:
                print(
                    f"{company} | {title} | от {salary_from} до {salary_to} {currency or ''} | {url}"
                )

        elif choice == "3":
            print("\n--- Средняя зарплата ---")
            avg = db.get_avg_salary()
            print(f"Средняя зарплата по всем вакансиям: {avg} руб.")

        elif choice == "4":
            print("\n--- Вакансии с зарплатой выше средней ---")
            results = db.get_vacancies_with_higher_salary()
            for company, title, salary_from, salary_to, currency, url in results:
                print(
                    f"{company} | {title} | от {salary_from} до {salary_to} {currency or ''} | {url}"
                )

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска: ").strip()
            print(f"\n--- Вакансии по запросу '{keyword}' ---")
            results = db.get_vacancies_with_keyword(keyword)
            if results:
                for company, title, salary_from, salary_to, currency, url in results:
                    print(
                        f"{company} | {title} | от {salary_from} до {salary_to} {currency or ''} | {url}"
                    )
            else:
                print("Вакансии не найдены.")

        elif choice == "0":
            print("Выход.")
            db.close()
            break

        else:
            print("Неверный пункт меню. Попробуй ещё раз.")

        print()


if __name__ == "__main__":
    main()
