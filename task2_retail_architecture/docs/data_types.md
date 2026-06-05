# Основные типы данных в ХД

## Измерения

| Таблица | Основные поля | Типы данных | Обоснование |
|---|---|---|---|
| `dim_date` | `date_key`, `date`, `month`, `quarter`, `year` | `INTEGER`, `DATE` | Быстрая фильтрация по периодам и группировка отчетов. |
| `dim_product` | `product_key`, `sku`, `name`, `category`, `brand` | `INTEGER`, `VARCHAR/TEXT` | Справочник товаров нужен почти во всех отчетах. |
| `dim_customer` | `customer_key`, `external_customer_id`, `segment`, `region` | `INTEGER`, `VARCHAR/TEXT` | Сегментация клиентов и анализ повторных покупок. |
| `dim_store` | `store_key`, `store_name`, `city`, `format` | `INTEGER`, `VARCHAR/TEXT` | Анализ офлайн-продаж по магазинам и регионам. |
| `dim_channel` | `channel_key`, `channel_name` | `INTEGER`, `VARCHAR/TEXT` | Сравнение B2C web, mobile и offline. |
| `dim_supplier` | `supplier_key`, `supplier_name`, `contract_status` | `INTEGER`, `VARCHAR/TEXT` | Связь закупок, договоров и поставок. |

## Факты

| Таблица | Основные поля | Типы данных | Обоснование |
|---|---|---|---|
| `fact_sales` | `date_key`, `product_key`, `customer_key`, `channel_key`, `quantity`, `revenue`, `discount`, `margin` | `INTEGER`, `DECIMAL` | Центральный факт продаж. Денежные суммы лучше хранить как `DECIMAL`, чтобы избежать ошибок округления. |
| `fact_inventory` | `date_key`, `product_key`, `store_key`, `stock_qty`, `reserved_qty` | `INTEGER`, `DECIMAL` | Остатки могут быть дробными для весовых товаров. |
| `fact_orders` | `order_id`, `status`, `created_at`, `paid_at`, `delivery_type` | `VARCHAR/TEXT`, `TIMESTAMP` | Детализация клиентских заказов и воронки. |
| `fact_service_requests` | `request_id`, `customer_key`, `product_key`, `sla_hours`, `status` | `VARCHAR/TEXT`, `INTEGER`, `DECIMAL` | Анализ качества обслуживания и SLA. |
| `fact_social_mentions` | `mention_id`, `product_key`, `source`, `sentiment`, `topic`, `published_at` | `VARCHAR/TEXT`, `TIMESTAMP`, `DECIMAL` | Анализ отзывов, тональности и информационных поводов. |
| `fact_purchase_forecast` | `date_key`, `product_key`, `forecast_qty`, `recommended_purchase_qty`, `model_version` | `INTEGER`, `DECIMAL`, `VARCHAR/TEXT` | Хранение прогноза спроса и рекомендуемых закупок. |

## Почему такие типы

- `INTEGER` для ключей и счетчиков быстрее индексируется и занимает меньше места.
- `DECIMAL` для денег и количеств сохраняет точность.
- `DATE` и `TIMESTAMP` нужны для корректной аналитики по периодам и времени событий.
- `VARCHAR/TEXT` подходит для названий, статусов, категорий, тем и внешних идентификаторов.
- Для больших промышленных объемов ХД лучше строить в колоночной СУБД, например ClickHouse, потому что аналитические запросы читают большие объемы данных по ограниченному набору столбцов.
