# Задание 2. Текущая функциональная архитектура

## Контекст C4

```mermaid
flowchart LR
    Customer[Покупатель B2C]
    Manager[Менеджер офиса]
    WarehouseUser[Сотрудник склада]
    StoreUser[Продавец офлайн-магазина]

    Ecommerce[Интернет-магазин B2C]
    Mobile[Мобильные приложения B2C]
    CRM[CRM]
    WMS[WMS]
    OneCTrade[1C Торговля]
    OneCSD[1C SD]
    OneCDocs[1C Документооборот]
    System[Внутренняя система]

    Customer --> Ecommerce
    Customer --> Mobile
    Manager --> CRM
    Manager --> OneCTrade
    Manager --> OneCDocs
    WarehouseUser --> WMS
    StoreUser --> OneCTrade
    StoreUser --> CRM

    Ecommerce --> CRM
    Mobile --> CRM
    CRM --> OneCTrade
    OneCTrade --> WMS
    OneCSD --> OneCDocs
    System --> CRM
    System --> OneCTrade
```

## Контейнеры текущей архитектуры

```mermaid
flowchart TB
    subgraph SalesChannels[Каналы продаж]
        Ecommerce[Интернет-магазин]
        Mobile[Мобильные приложения]
        Offline[Офлайн-магазин]
    end

    subgraph BackOffice[Офис и учет]
        CRM[CRM: клиенты, лиды, обращения]
        OneCTrade[1C Торговля: заказы, товары, цены]
        OneCSD[1C SD: сервисные заявки]
        OneCDocs[1C Документооборот: договоры и документы]
        System[Внутренняя система]
    end

    subgraph Warehouse[Склад]
        WMS[WMS: остатки, приемка, отгрузка]
    end

    Ecommerce --> CRM
    Mobile --> CRM
    Offline --> OneCTrade
    CRM --> OneCTrade
    OneCTrade --> WMS
    OneCSD --> OneCDocs
    System --> CRM
    System --> OneCTrade
```

## Проблемы текущего состояния

- Данные распределены по системам и анализируются фрагментами.
- Нет единого места для анализа онлайн-продаж, офлайн-продаж, складских остатков, обращений и отзывов.
- Прогнозирование закупок осложнено: спрос, остатки, сезонность и отзывы находятся в разных контурах.
- Руководство получает отчеты с задержкой, потому что выгрузки часто собираются вручную.

## BPMN текущего процесса

BPMN-файл текущего процесса обработки продаж находится здесь:

```text
task2_retail_architecture/bpmn/current_sales_process.bpmn
```

Диаграмма показывает, что заказ обрабатывается операционными системами, а управленческий отчет в текущем состоянии формируется вручную из разных выгрузок.
