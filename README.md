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


## Решение
Технически архитектура решение состоит из двух контуров:
- Обучение - запускается ночью и выполняет две задачи: готовит датасет и обучает ML-модель
- Предсказание - запускается каждыйе 5 минут и выполняет предсказание (покупать, продавать, ничего не делать).
<p align="center" width="100%">
<img src="https://github.com/slivka83/algopack_simple_bot/blob/main/docs/img/pipeline.png?raw=tru" alt="Архитектура решения" width="500"/>
</p>

Для обучения подготовили датасет, который состоит из фичей AlgoPack и лагов, созданных из фичей временного ряда.
<p align="center" width="100%">
<img src="https://github.com/slivka83/algopack_simple_bot/blob/main/docs/img/dataset.png?raw=true" alt="Датасет" align="center" width="500"/>
</p>

Метки для обучения получили путем детекции пиков и впадин на временном ряду (цены акции):
<p align="center" width="100%">
<img src="https://github.com/slivka83/algopack_simple_bot/blob/main/docs/img/target.png?raw=true" alt="Таргет"/>
</p>

## Статьи
Весь ход разработки решения описали в цикле статей:
- Введение
- EDA
- Модель
- Бот

## Ноутбуки
Также офрмили ряд ноутбуков, которые в ручном режиме воспроизводят функционал бота:
- [EDA](https://github.com/slivka83/algopack_simple_bot/blob/main/notebooks/EDA.ipynb)
- [Model](https://github.com/slivka83/algopack_simple_bot/blob/main/notebooks/Model.ipynb)
- [Bot](https://github.com/slivka83/algopack_simple_bot/blob/main/notebooks/Bot.ipynb)