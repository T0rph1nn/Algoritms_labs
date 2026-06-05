# Задание 2. Целевая архитектура

## Целевой контекст C4

Целевая архитектура сохраняет текущие системы и добавляет аналитический контур: ETL, ХД и BI.

```mermaid
flowchart LR
    Customer[Покупатель B2C]
    Analyst[Аналитик]
    Manager[Руководитель]

    Ecommerce[Интернет-магазин]
    Mobile[Мобильные приложения]
    CRM[CRM]
    WMS[WMS]
    OneCTrade[1C Торговля]
    OneCSD[1C SD]
    OneCDocs[1C Документооборот]
    System[Внутренняя система]
    BrandAnalytics[BrandAnalytics / мониторинг соцмедиа]

    ETL[ETL-процессы]
    DWH[Хранилище данных]
    BI[BI-система]

    Customer --> Ecommerce
    Customer --> Mobile

    Ecommerce --> ETL
    Mobile --> ETL
    CRM --> ETL
    WMS --> ETL
    OneCTrade --> ETL
    OneCSD --> ETL
    OneCDocs --> ETL
    System --> ETL
    BrandAnalytics --> ETL

    ETL --> DWH
    DWH --> BI
    BI --> Analyst
    BI --> Manager
```

## Контейнеры целевой архитектуры

```mermaid
flowchart TB
    subgraph Sources[Операционные источники]
        Ecommerce[Интернет-магазин]
        Mobile[Мобильные приложения]
        CRM[CRM]
        WMS[WMS]
        OneCTrade[1C Торговля]
        OneCSD[1C SD]
        OneCDocs[1C Документооборот]
        System[Внутренняя система]
        BrandAnalytics[BrandAnalytics]
    end

    subgraph DataPlatform[Платформа данных]
        Staging[Staging-слой]
        ETL[ETL: извлечение, очистка, объединение]
        DWH[ХД: факты и измерения]
        Marts[Витрины данных]
    end

    subgraph Analytics[Аналитика]
        BI[BI-дашборды]
        Forecast[Прогноз спроса и закупок]
        Reports[Регламентная отчетность]
    end

    Sources --> Staging
    Staging --> ETL
    ETL --> DWH
    DWH --> Marts
    Marts --> BI
    Marts --> Forecast
    Marts --> Reports
```

## Что появляется после внедрения

- Единое ХД для анализа продаж, клиентов, товаров, остатков, обращений и отзывов.
- BI-дашборды для руководителей и аналитиков.
- Прогнозирование закупок на основе спроса, остатков, сезонности и внешнего сигнала из соцмедиа.
- Снижение ручной подготовки отчетов.
