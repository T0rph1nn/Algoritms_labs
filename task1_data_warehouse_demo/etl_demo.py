"""
Демонстрационная ETL-программа для задания 1.

Программа создает две БД-источника и одну БД-хранилище данных (ХД),
заполняет источники тестовыми данными и объединяет записи о сотрудниках,
несмотря на разный порядок слов и регистр в ФИО.
"""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PROJECTS_DB = DATA_DIR / "source_projects.db"
HR_DB = DATA_DIR / "source_hr.db"
WAREHOUSE_DB = DATA_DIR / "warehouse.db"


@dataclass(frozen=True)
class ProjectSourceRow:
    full_name: str
    role_name: str
    project_name: str
    project_description: str
    tech_stack: str


@dataclass(frozen=True)
class HrSourceRow:
    full_name: str
    competencies: str
    salary_rub: int
    bonus_rub: int


PROJECT_ROWS = [
    ProjectSourceRow(
        "Иванов Иван Петрович",
        "Backend-разработчик",
        "Платформа лояльности",
        "Сервис начисления баллов, купонов и персональных предложений.",
        "Python, FastAPI, PostgreSQL, Redis, Docker",
    ),
    ProjectSourceRow(
        "петрова анна сергеевна",
        "Аналитик данных",
        "Витрина продаж",
        "Подготовка витрин для анализа онлайн- и офлайн-продаж.",
        "SQL, Python, Pandas, Airflow, ClickHouse",
    ),
    ProjectSourceRow(
        "Сидоров Алексей Игоревич",
        "DevOps-инженер",
        "Контур CI/CD",
        "Автоматизация сборки, тестирования и доставки приложений.",
        "GitLab CI, Kubernetes, Helm, Prometheus",
    ),
    ProjectSourceRow(
        "Мария Андреевна Кузнецова",
        "Product owner",
        "Мобильное приложение",
        "Развитие B2C-приложения для заказов и программы лояльности.",
        "Mobile, REST API, Firebase, A/B testing",
    ),
]

HR_ROWS = [
    HrSourceRow(
        "ИВАН ПЕТРОВИЧ ИВАНОВ",
        "Python; REST API; SQL; unit-тестирование",
        210000,
        45000,
    ),
    HrSourceRow(
        "Анна Сергеевна Петрова",
        "SQL; BI; ETL; продуктовая аналитика",
        190000,
        40000,
    ),
    HrSourceRow(
        "игоревич сидоров алексей",
        "Linux; Kubernetes; мониторинг; CI/CD",
        230000,
        50000,
    ),
    HrSourceRow(
        "КУЗНЕЦОВА МАРИЯ АНДРЕЕВНА",
        "Управление бэклогом; UX; финансы продукта",
        240000,
        60000,
    ),
]


def normalize_full_name(full_name: str) -> str:
    """
    Приводим ФИО к стабильному ключу сопоставления.

    В источниках ФИО может быть записано как "Фамилия Имя Отчество",
    "Имя Отчество Фамилия", в верхнем/нижнем регистре. Для учебного
    примера достаточно привести строку к нижнему регистру, удалить лишние
    символы и отсортировать слова. Получается одинаковый ключ для разных
    порядков слов.
    """
    words = re.findall(r"[а-яёa-z]+", full_name.lower())
    return " ".join(sorted(words))


def reset_database(path: Path) -> sqlite3.Connection:
    if path.exists():
        path.unlink()
    return sqlite3.connect(path)


def create_source_projects() -> None:
    with reset_database(PROJECTS_DB) as conn:
        conn.execute(
            """
            CREATE TABLE project_assignments (
                assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                normalized_name TEXT NOT NULL,
                role_name TEXT NOT NULL,
                project_name TEXT NOT NULL,
                project_description TEXT NOT NULL,
                tech_stack TEXT NOT NULL
            )
            """
        )
        conn.executemany(
            """
            INSERT INTO project_assignments (
                full_name, normalized_name, role_name, project_name,
                project_description, tech_stack
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    row.full_name,
                    normalize_full_name(row.full_name),
                    row.role_name,
                    row.project_name,
                    row.project_description,
                    row.tech_stack,
                )
                for row in PROJECT_ROWS
            ],
        )
        conn.execute(
            "CREATE INDEX idx_project_assignments_normalized_name "
            "ON project_assignments(normalized_name)"
        )


def create_source_hr() -> None:
    with reset_database(HR_DB) as conn:
        conn.execute(
            """
            CREATE TABLE employee_profiles (
                profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                normalized_name TEXT NOT NULL,
                competencies TEXT NOT NULL,
                salary_rub INTEGER NOT NULL CHECK (salary_rub >= 0),
                bonus_rub INTEGER NOT NULL CHECK (bonus_rub >= 0)
            )
            """
        )
        conn.executemany(
            """
            INSERT INTO employee_profiles (
                full_name, normalized_name, competencies, salary_rub, bonus_rub
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    row.full_name,
                    normalize_full_name(row.full_name),
                    row.competencies,
                    row.salary_rub,
                    row.bonus_rub,
                )
                for row in HR_ROWS
            ],
        )
        conn.execute(
            "CREATE INDEX idx_employee_profiles_normalized_name "
            "ON employee_profiles(normalized_name)"
        )


def create_warehouse_schema() -> None:
    with reset_database(WAREHOUSE_DB) as conn:
        conn.execute(
            """
            CREATE TABLE dim_employee (
                employee_key INTEGER PRIMARY KEY AUTOINCREMENT,
                normalized_name TEXT NOT NULL UNIQUE,
                source_project_full_name TEXT NOT NULL,
                source_hr_full_name TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE dim_project (
                project_key INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL UNIQUE,
                project_description TEXT NOT NULL,
                tech_stack TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE fact_employee_project (
                fact_key INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_key INTEGER NOT NULL,
                project_key INTEGER NOT NULL,
                role_name TEXT NOT NULL,
                competencies TEXT NOT NULL,
                salary_rub INTEGER NOT NULL,
                bonus_rub INTEGER NOT NULL,
                total_compensation_rub INTEGER NOT NULL,
                FOREIGN KEY (employee_key) REFERENCES dim_employee(employee_key),
                FOREIGN KEY (project_key) REFERENCES dim_project(project_key)
            )
            """
        )
        conn.execute(
            "CREATE INDEX idx_fact_employee_project_employee "
            "ON fact_employee_project(employee_key)"
        )


def load_source_rows(db_path: Path, table_name: str) -> list[sqlite3.Row]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        return list(conn.execute(f"SELECT * FROM {table_name}"))
    finally:
        conn.close()


def run_etl() -> None:
    project_rows = load_source_rows(PROJECTS_DB, "project_assignments")
    hr_rows = load_source_rows(HR_DB, "employee_profiles")

    # HR-данные кладем в словарь по нормализованному ФИО, чтобы объединение
    # работало за O(n), а не через вложенные циклы O(n*m).
    hr_by_name = {row["normalized_name"]: row for row in hr_rows}

    with sqlite3.connect(WAREHOUSE_DB) as wh:
        for project_row in project_rows:
            normalized_name = project_row["normalized_name"]
            hr_row = hr_by_name.get(normalized_name)
            if hr_row is None:
                print(f"Пропуск: не найден HR-профиль для {project_row['full_name']}")
                continue

            cursor = wh.execute(
                """
                INSERT INTO dim_employee (
                    normalized_name, source_project_full_name, source_hr_full_name
                )
                VALUES (?, ?, ?)
                ON CONFLICT(normalized_name) DO UPDATE SET
                    source_project_full_name = excluded.source_project_full_name,
                    source_hr_full_name = excluded.source_hr_full_name
                RETURNING employee_key
                """,
                (
                    normalized_name,
                    project_row["full_name"],
                    hr_row["full_name"],
                ),
            )
            employee_key = cursor.fetchone()[0]

            cursor = wh.execute(
                """
                INSERT INTO dim_project (
                    project_name, project_description, tech_stack
                )
                VALUES (?, ?, ?)
                ON CONFLICT(project_name) DO UPDATE SET
                    project_description = excluded.project_description,
                    tech_stack = excluded.tech_stack
                RETURNING project_key
                """,
                (
                    project_row["project_name"],
                    project_row["project_description"],
                    project_row["tech_stack"],
                ),
            )
            project_key = cursor.fetchone()[0]

            salary = int(hr_row["salary_rub"])
            bonus = int(hr_row["bonus_rub"])
            wh.execute(
                """
                INSERT INTO fact_employee_project (
                    employee_key, project_key, role_name, competencies,
                    salary_rub, bonus_rub, total_compensation_rub
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    employee_key,
                    project_key,
                    project_row["role_name"],
                    hr_row["competencies"],
                    salary,
                    bonus,
                    salary + bonus,
                ),
            )


def print_warehouse_report() -> None:
    query = """
        SELECT
            e.source_project_full_name AS project_db_name,
            e.source_hr_full_name AS hr_db_name,
            p.project_name,
            f.role_name,
            f.competencies,
            f.salary_rub,
            f.bonus_rub,
            f.total_compensation_rub
        FROM fact_employee_project f
        JOIN dim_employee e ON e.employee_key = f.employee_key
        JOIN dim_project p ON p.project_key = f.project_key
        ORDER BY p.project_name
    """
    with sqlite3.connect(WAREHOUSE_DB) as conn:
        conn.row_factory = sqlite3.Row
        rows = list(conn.execute(query))

    print("\nИтоговая витрина ХД")
    print("-" * 100)
    for row in rows:
        print(
            f"{row['project_db_name']} | {row['hr_db_name']} | "
            f"{row['project_name']} | {row['role_name']} | "
            f"{row['total_compensation_rub']} руб."
        )


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    create_source_projects()
    create_source_hr()
    create_warehouse_schema()
    run_etl()
    print_warehouse_report()
    print(f"\nБазы данных созданы в папке: {DATA_DIR}")


if __name__ == "__main__":
    main()
