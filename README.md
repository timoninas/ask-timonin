# Web-технологии; Технопарк; 1 семестр

# Цель работы:
Создать веб-приложение, в котором можно задать интересующий вас вопрос и получить на него ответ. Ответить на вопросы, ответы на которые вы знаете. Получить базовые знания веб-программирования

# Функциональные требования:
* Регистрация
* Вход / выход из приложения
* Просмотр и изменение информации о себе
* Просмотр списка вопросов
* Просмотр одного вопроса с ответами к нему
* Создание вопроса с тегами
* Создание ответа к вопросу
* Просмотр существующих вопросов и ответов

# ER-model

<p align="center">
  <img class = "er-diagram" src = "media/er.png" >
</p>

# Use-case diagram

<p align="center">
  <img class = "use-case-diagram" src = "media/use_case.png" >
</p>

# Apache HTTP server benchmarking tool - ab

Тестирование производительности web-приложения. Для этой цели можно использовать Apache HTTP server benchmarking tool

Результаты тестирования на введенных ниже параметрах:

`ab -c 100 -n 10000 http://127.0.0.1:80/api/v2/questions &> out_ab_1.txt`
 
`-c concurrency` - Количество нескольких запросов, выполняемых одновременно

`-n requests` - Количество запросов на выполнение сеанса бенчмаркинга


# 10000 запросов без балансировки
```Console
ab -c 100 -n 10000 http://127.0.0.1:80/api/v2/questions
This is ApacheBench, Version 2.3 <$Revision: 1843412 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 1000 requests
Completed 2000 requests
Completed 3000 requests
Completed 4000 requests
Completed 5000 requests
Completed 6000 requests
Completed 7000 requests
Completed 8000 requests
Completed 9000 requests
Completed 10000 requests
Finished 10000 requests


Server Software:        nginx/1.18.0
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /api/v2/questions
Document Length:        1161 bytes

Concurrency Level:      100
Time taken for tests:   237.241 seconds
Complete requests:      10000
Failed requests:        55
   (Connect: 0, Receive: 0, Length: 55, Exceptions: 0)
Non-2xx responses:      55
Total transferred:      19384897 bytes
HTML transferred:       16438791 bytes
Requests per second:    42.15 [#/sec] (mean)
Time per request:       2372.411 [ms] (mean)
Time per request:       23.724 [ms] (mean, across all concurrent requests)
Transfer rate:          79.79 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.6      0       7
Processing:    49 2352 4001.0   2149   61024
Waiting:       43 2352 4001.0   2149   61023
Total:         49 2352 4001.5   2149   61030

Percentage of the requests served within a certain time (ms)
  50%   2149
  66%   2451
  75%   2627
  80%   2737
  90%   3026
  95%   3307
  98%   3692
  99%   4158
 100%  61030 (longest request)
```

# 10000 запросов с балансировкой
```Console
ab -c 100 -n 10000 http://127.0.0.1:80/api/v2/questions
This is ApacheBench, Version 2.3 <$Revision: 1843412 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 1000 requests
Completed 2000 requests
Completed 3000 requests
Completed 4000 requests
Completed 5000 requests
Completed 6000 requests
Completed 7000 requests
Completed 8000 requests
Completed 9000 requests
Completed 10000 requests
Finished 10000 requests


Server Software:        nginx/1.18.0
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /api/v2/questions
Document Length:        1161 bytes

Concurrency Level:      100
Time taken for tests:   219.405 seconds
Complete requests:      10000
Failed requests:        0
Total transferred:      14560000 bytes
HTML transferred:       11610000 bytes
Requests per second:    45.58 [#/sec] (mean)
Time per request:       2194.053 [ms] (mean)
Time per request:       21.941 [ms] (mean, across all concurrent requests)
Transfer rate:          64.81 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.2      0       6
Processing:    23 1933 5973.2    682   83194
Waiting:       23 1933 5973.2    682   83194
Total:         23 1933 5973.2    682   83194

Percentage of the requests served within a certain time (ms)
  50%    682
  66%    952
  75%   1608
  80%   1754
  90%   3718
  95%   7751
  98%  16109
  99%  31643
 100%  83194 (longest request)
```
____

# Пользовательские сценарии

## Конкретные сценарии

| Целевая аудитория | Описание | Роль |
| --- | --- | --- |
| Начинащие программисты | К этой категории можно отнести людей, которые только начали осваивать программирование, поэтому они задают много вопрос и мало отвечают на другие вопросы | Активные генераторы потока: вопросов. От них идет основная активность. Помимо того, что они постоянно снабжают приложение новыми вопросами. Так они еще пишут много комментариев, получая таким образом также ответы на свои вопросы.  |
| Программисты с небольшим опытом | К этой категории относятся люди, освоившие некоторые аспекты программирования. Они продолжают задавать вопросы, но не редко отвечают менее опытным программистам | Такие же активные генераторы потока: вопросов и ответов |
| Опытные программисты | Менее активные пользователи. Имеющий большой опыт в области программирования. Большинство их ответов избирается, как решение проблемы программистов, задающих вопросы | Неактивные генераторы потока |

## Сценарии использования

**Сценарий 1**
| UCO1 | Просмотр ответов |
| --- | --- |
| Краткое описание | Просмотр ответов |
| № Шага | Действие |
| 1 | Пользователь открывает страницу вопроса |
| 2 | Система открывает конкретный вопрос с подгруженным для него ответами |
| 3 | Пользователь просматривает ответы |

**Сценарий 2**
| UCO3 | Написание вопроса |
| --- | --- |
| Краткое описание | Написание вопроса |
| № Шага | Действие |
| 1 | Пользователь открывает главную страницу сайта |
| 2 | Система подгружает списки новых вопросов |
| 3 | Авторизированный пользователь нажимает на кнопку "Ask" - для создания вопроса |
| 4 | Авторизированный формирует вопрос и задает его |
| 5 | Система добавляет к себе сформированный вопрос с последующей выгрузкой для всех пользователей |

**Сценарий 3**
| UCO3 | Написание ответа |
| --- | --- |
| Краткое описание | Написание ответа |
| № Шага | Действие |
| 1 | Пользователь открывает список новых вопросов |
| 2 | Система подгружает списки вопросов |
| 3 | Пользователь выбирает интересный ему вопрос |
| 4 | Авторизированный пользователь оставляет ответ под конкретным вопросом |

# Figma animation

<p align="center">
  <img class = "figma-animation" src = "media/prototype-animation.gif" >
</p>

# Figma scroll

<p align="center">
  <img class = "figma-animation" src = "media/prototype-scroll.gif" >
</p>





