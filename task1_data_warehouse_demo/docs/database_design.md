# Задание 1. Проектирование БД

## Выбор СУБД

Для демонстрационной реализации выбрана SQLite.

Обоснование:

- SQLite не требует отдельного сервера, поэтому проект легко показать преподавателю на любом компьютере.
- Для учебного набора данных скорость чтения и соединения таблиц достаточна с большим запасом.
- Поддерживаются реляционные таблицы, первичные ключи, внешние ключи, ограничения `CHECK`, индексы и транзакции.
- В реальной промышленной системе вместо SQLite логично использовать PostgreSQL для источников и ClickHouse/PostgreSQL для ХД, если объемы данных возрастают.

## Типы данных

- `INTEGER` используется для суррогатных ключей, зарплаты, премии и итоговой компенсации. Целые числа быстрее и безопаснее для денежных сумм в рублях, чем `REAL`, потому что нет ошибок округления с плавающей точкой.
- `TEXT` используется для ФИО, ролей, описаний проектов, компетенций и технологического стека.
- `normalized_name TEXT` используется как технический ключ сопоставления сотрудников между источниками.
- Индексы по `normalized_name` ускоряют объединение данных по ФИО.

## ER-диаграмма источников и ХД

```mermaid
erDiagram
    PROJECT_ASSIGNMENTS {
        INTEGER assignment_id PK
        TEXT full_name
        TEXT normalized_name
        TEXT role_name
        TEXT project_name
        TEXT project_description
        TEXT tech_stack
    }

    EMPLOYEE_PROFILES {
        INTEGER profile_id PK
        TEXT full_name
        TEXT normalized_name
        TEXT competencies
        INTEGER salary_rub
        INTEGER bonus_rub
    }

    DIM_EMPLOYEE {
        INTEGER employee_key PK
        TEXT normalized_name UK
        TEXT source_project_full_name
        TEXT source_hr_full_name
    }

    DIM_PROJECT {
        INTEGER project_key PK
        TEXT project_name UK
        TEXT project_description
        TEXT tech_stack
    }

    FACT_EMPLOYEE_PROJECT {
        INTEGER fact_key PK
        INTEGER employee_key FK
        INTEGER project_key FK
        TEXT role_name
        TEXT competencies
        INTEGER salary_rub
        INTEGER bonus_rub
        INTEGER total_compensation_rub
    }

    DIM_EMPLOYEE ||--o{ FACT_EMPLOYEE_PROJECT : "employee_key"
    DIM_PROJECT ||--o{ FACT_EMPLOYEE_PROJECT : "project_key"
```

## Структура ХД

Хранилище использует простую звездообразную схему:

- `dim_employee` - измерение сотрудников.
- `dim_project` - измерение проектов.
- `fact_employee_project` - факт участия сотрудника в проекте с финансовыми показателями.

Такой подход удобен для аналитики: можно группировать затраты по проектам, ролям, компетенциям и сотрудникам.
