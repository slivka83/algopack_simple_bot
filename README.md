# Алгоритмический бот

Пример реализации алгоритмического бота для торговли на Московоской фондовой бирже с использованием данных платформаы [AlgoPack](https://www.moex.com/ru/algopack).

## Инструкция
Для запуска решения выполните следующие шаги:
1. git clone [url]
2. cd [folder]
3. pip install -r requirements.txt
4. Загрузить исторические данные:
- Поправить в файле get_history.py период, за который нужно выполнить загрузку.
- Выполнить файл get_history.py
5. Изменить в файле predict_model.py фнукцию, чтобы отправляла результат предсказания брокеру.
6. Настройте планировщик на выполнение следующих команд:
- pypyr src/pipeline/train_dvc </br>
Отвечает за загрузку данных за прошедший день.</br>
Запуск ежедневно в 1 час ночи.
- pypyr src/pipeline/predict </br>
Выполняет предсказание и отправялет запрос брокеру.</br>
Запуск с 11 до 19 каждые 5 минут.


## Архитектура решения
Технически решение состоит из двух частей:
<img src="https://github.com/slivka83/algopack_simple_bot/blob/main/docs/img/pipeline.png?raw=tru" alt="Архитектура решения" align="center" width="500"/>

Датасет:
<img src="https://github.com/slivka83/algopack_simple_bot/blob/main/docs/img/dataset.png?raw=true" alt="Датасет" align="center" width="500"/>

Таргет:
<img src="https://github.com/slivka83/algopack_simple_bot/blob/main/docs/img/target.png?raw=true" alt="Таргет"/>



## Статьи
Статьи:
- _
- _

## Ноутбуки
В ноутбуках вы найдете наглядный пример воспроизведения:
- _
- _