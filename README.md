# Алгоритмический бот

Пример реализации алгоритмического бота для торговли на Московоской фондовой бирже с использованием данных платформаы [AlgoPack](https://www.moex.com/ru/algopack).

Инструкция:
1. git clone [url]
2. cd [folder]
3. pip install -r requirements.txt
4. Загрузить исторические данные:
- Поправить в файле get_history.py период, за который нужно выполнить загрузку.
- Выполнить файл get_history.py
5. Изменить в файле predict_model.py фнукцию, чтобы отправляла результат предсказания брокеру.
6. Для ежедневной загрузки данных настройте планировщик на ежедневное выполнение 
pypyr src/pipeline/train_dvc
7. Настроить планировщик для запуска предсказания каждые 5 минут.
pypyr src/pipeline/predict

Архитектура решения:

Статьи:


В ноутбуках вы найдете наглядный пример воспроизведения: