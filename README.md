# XakSpring2025

.env 

    #остальные настройки
    SECRET_KEY="YOUR_SEACKRET_KEY"
    DEBUG=True # на время разработки true на прод false

    # база данных
    DATABASE_NAME="YOUR_DATABASE_NAME"
    DATABASE_USER="YOUR_DATABASE_USER"
    DATABASE_PASSWORD="YOUR_DATABASE_PASSWORD"
    DATABASE_HOST=localhost # пока что не трогать для докера не нужно будет это менять 
    DATABASE_PORT=5432
# [T5 Модель](https://huggingface.co/RimasZzz/agriculture_text_transform_model)
## [Архитектура](model/agriculture_text_transform_model/config.json)
<p align="center">
  <img src="T5_model/assets/model_architecturejpg.jpg">
</p>

## [Обучение](model/train.py)
<p align="center">
  <img src="T5_model/assets/trainLoss.jpg">
</p>

## [Примеры работы](model/test.py)
Source: `Пахота зяби под мн тр`<br>
Result: `Пахота зяби под Многолетние травы`

Source: `Предп культ под оз пш`<br>
Result: `Предпосевная культивация под Пшеница озимая`

Source: `2-е диск сах св под пш`<br>
Result: `2-е Дискование Свекла сахарная под Пшеница озимая`

Source: `Внесение мин удобрений под оз пшеницу`<br>
Result: `Внесение минеральных удобрений под Пшеница озимая`

Source: `Прикат мн тр под оз пш`<br>
Result: `Прикатывание посевов Многолетние травы под Пшеница озимая`

# [ner Модель]()
## [Архитектура]()
<p align="center">
  <img src="ner_model/assets/model_architecturejpg.jpg">
</p>

## [Обучение]()
<p align="center">
  <img src="ner_model/assets/trainLoss.jpg">
</p>

## [Примеры работы]()
Source: <br>
```Дискование 2-е под Ячмень озимый По ПУ 61/352 Отд 11 32/32 Отд 12 29/219```<br>
Result:
```
- OPERATION: 'Дискование 2-е'
- CROP: 'Ячмень озимый'
- SUBUNIT: 'По ПУ 61/352'
- DEPARTMENT: 'Отд 11'
- DEPARTMENT: 'Отд 12'
```

Source: <br>
```16.11 Мир Пахота под Кукуруза товарная 30 га, 599 га, 89%, 73 га остаток. Пахота под Соя товарная 30 га, 879 га, 77%, 260 га остаток. Работало 2 агрегата.```<br>
Result:
```
- DATE: '16.11'
- DEPARTMENT: 'Мир'
- OPERATION: 'Пахота'
- CROP: 'Кукуруза товарная'
- HECTARE: '30 га'
- HECTARE: '599 га'
- OPERATION: 'Пахота'
- CROP: 'Соя товарная'
- HECTARE: '30 га'
- HECTARE: '260 га'
```

Source: <br>
```Пахота под Соя товарная: День - 295 га От начала - 6804 га (79%) Остаток- 1774 га```<br>
Result:
```
- OPERATION: 'Пахота'
- CROP: 'Соя товарная:'
- HECTARE: '295 га'
- HECTARE: '6804 га'
- HECTARE: '1774 га'
```

