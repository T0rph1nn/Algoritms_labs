# Учебный проект: ХД, ETL, C4 и BPMN

Проект содержит две независимые части для демонстрации преподавателю.

## Задание 1. Сбор и объединение данных из двух БД в ХД

Папка: `task1_data_warehouse_demo`

Что внутри:

- `etl_demo.py` - программа на Python, которая создает 3 SQLite-БД:
  - `source_projects.db` - источник с ФИО, ролями и проектами;
  - `source_hr.db` - источник с ФИО, компетенциями, зарплатой и премиями;
  - `warehouse.db` - хранилище данных.
- `docs/database_design.md` - проектирование БД, ER-диаграмма и обоснование выбора СУБД/типов данных.
- `docs/etl_algorithm.md` - алгоритм ETL, нормализация ФИО и логика объединения.
- `bpmn/task1_etl_collection.bpmn` - BPMN XML для открытия в Camunda Modeler.

Запуск:

```bash
cd task1_data_warehouse_demo
python etl_demo.py
```

После запуска БД появятся в папке `task1_data_warehouse_demo/data`.

## Задание 2. Архитектура розничного предприятия

Папка: `task2_retail_architecture`

Что внутри:

- `docs/current_architecture.md` - текущая функциональная архитектура в C4.
- `docs/target_architecture.md` - целевая архитектура после внедрения ETL, ХД и BI.
- `docs/data_flows.md` - диаграмма потоков данных в ХД.
- `docs/analytics_algorithm.md` - алгоритм сбора и анализа данных, включая BrandAnalytics.
- `docs/data_types.md` - основные типы данных ХД и обоснование.
- `bpmn/current_sales_process.bpmn` - BPMN текущего процесса обработки продаж.
- `bpmn/target_data_collection_and_analysis.bpmn` - BPMN XML для Camunda Modeler.

Диаграммы C4/ER/потоков данных записаны в Mermaid, чтобы их можно было быстро отобразить в Markdown-редакторах, GitHub или вставить в отчет.
