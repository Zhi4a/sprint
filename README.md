<h2>Проект Виртуальной стажировки по разработке мобильного приложения для ФСТР (Федерация Спортивного Туризма России).</h2>

<h3>С какой проблемой к нам обратился заказчик:</h3>
<a>
На <a href="https://pereval.online/">сайте ФСТР</a> ведётся база горных перевалов, которая пополняется туристами.
После преодоления очередного перевала, турист заполняет отчёт в формате PDF и отправляет его на электронную почту федерации.
Экспертная группа ФСТР получает эту информацию, верифицирует, а затем вносит её в базу, которая ведётся в Google-таблице.
Весь процесс очень неудобный и долгий и занимает в среднем от 3 до 6 месяцев.
</a>
<h3>Как заказчик хочет решить эту проблему</h3>
<a>
Разработать мобильное приложение для Android и IOS, которое упростило бы туристам задачу по отправке данных о перевале и сократило время обработки запроса до трёх дней.
Пользоваться мобильным приложением будут туристы. В горах они будут вносить данные о перевале в приложение и отправлять их в ФСТР, как только появится доступ в Интернет.
Модератор из федерации будет верифицировать и вносить в базу данных информацию, полученную от пользователей, а те в свою очередь смогут увидеть в мобильном приложении статус модерации и просматривать базу с объектами, внесёнными другими.
</a>
<h4>Для пользователя в мобильном приложении будут доступны следующие действия:</h4>
<p>- Внесение информации о новом объекте (перевале) в карточку объекта.</p>
<p>- Редактирование в приложении неотправленных на сервер ФСТР данных об объектах. На перевале не всегда работает Интернет.</p>
<p>- Заполнение ФИО и контактных данных (телефон и электронная почта) с последующим их автозаполнением при внесении данных о новых объектах.</p>
<p> Отправка данных на сервер ФСТР.</p>
<p>- Получение уведомления о статусе отправки (успешно/неуспешно).</p>
<p>- Согласие пользователя с политикой обработки персональных данных в случае нажатия на кнопку «Отправить» при отправке данных на сервер.</p>
<h4>Пользователь с помощью мобильного приложения также будет передавать в ФСТР следующие данные о перевале:</h4>
<p>- координаты перевала и его высота;</p>
<p>- имя пользователя;</p>
<p>- почта и телефон пользователя;</p>
<p>- название перевала;</p>
<p>- несколько фотографий перевала.</p>

<p>Допустимые значения поля status:

```
'new' - новая заявка(default-значение);
'pending' — на рассмотрении;
'accepted' — заявка принята;
'rejected' — заявка отклонена.
```

</p>
<h2>Описание методов API</h2>
<h4>Метод <i>POST</i> API/submitData/</h4>
Этот метод принимает JSON в теле запроса с информацией о перевале.
<h4>Пример JSON:</h4>

```JSON
{
"beauty_title": "пер.",
"title": "Дятлова",
"other_titles": "седл.",
"connect": "0",
"add_time": "2023-04-15 19:13:14",
"user": {
    "email": "sohuga5656@gmail.com",
    "fam": "Михайлов",
    "name": "Михаил",
    "otc": "Михайлович",
    "phone": "89997777777"
    },
    "coordinates": {
        "latitude": "77.7777",
        "longitude": "11.1111",
        "height": "2727"
    },
    "level": {
        "winter": "2А",
        "summer": "1А*",
        "autumn": "1А",
        "spring": "2A*"
    },
    "images": [
        {
        "data": "image1",
        "title": "Основание"
        },
        {
        "data": "image2",
        "title": "Седло"
        },
        {
        "data": "image3",
        "title": "Обрыв"
        }
    ]
}
```

Результатом выполнения метода является JSON-ответ содержащий следующие данные:
`'status'` + код HTTP, целое число:

```
 200 — запрос успешно обработан;
 400 — Bad Request (при нехватке полей);
 500 — ошибка при выполнении операции.
```

<p>
`message` — строка +
</p>
<a>
`Success` - если отправлено успешно
</a>
<a>или `Причина ошибки` - если она была
</a>
<p>
`id` —  идентификатор, который был присвоен объекту при добавлении в базу данных (если "status":200).
</p>
<h4>Примеры JSON-ответов:</h4>

```
{ "status": 200, "message": "Success", "id": 42}
{ "status": 400, "message": "Empty request", "id": null}
{ "status": 500, "message": "Ошибка подключения к базе данных", "id": null}
```

<h3>Метод <i>GET</i> API/submitData/<id></h3>
Этот метод получает одну запись (перевал) по её id с выведением всей информацию об перевале, в том числе статус модерации.
<h4>Пример JSON: </h4>

```JSON
{
"id": 7,
"user": {
    "email": "sohuga5656@gmail.com",
    "fam": "Михайлов",
    "name": "Михаил",
    "otc": "Михайлович",
    "phone": "89997777777"
    },
    "coordinates": {
        "id": 1,
        "latitude": 777.77,
        "longitude": 77.77,
        "height": 1111
    },
    "levels": {
        "id": 2,
        "winter": "1С",
        "summer": "1А*",
        "autumn": "1А",
        "spring": "1С*"
    },
    "images": [
        {
        "id": 3,
        "created": "2023-04-15T10:44:29.555124",
        "title": "Основание",
        "data": "",
        "pass": 7
        },
        {
        "id": 4,
        "created": "2023-04-15T10:46:29.777144",
        "title": "Седло",
        "data": "",
        "pass": 7
        }
        ],
    "created": "2023-04-15T10:41:38.631576",
    "beauty_title": "пер.",
    "title": "Дятлова",
    "other_titles": "пере.",
    "connect": "0",
    "add_time": "2023-04-15T19:10:11",
    "status": "new"
}
```

<h4>Примеры JSON-ответов:</h4>

```
{ "status": 200, "message": "Success", "id": 42 }
{ "status": 400, "message": "There's no such record", "id": null}
```

<h3>Метод <i>PATCH</i> API/submitData/<id></h3>
Позволяет отредактировать существующую запись (замена), если она в статусе `new`. При этом редактировать можно все поля, кроме ФИО, адреса почты и номера телефона.
В качестве результата изменения приходит ответ содержащий следующие данные:

`state`:

```
1 — если успешно удалось отредактировать запись в базе данных.
0 — отредактировать запись не удалось.
```

`message`:
<a>- сообщение об успешном редактировании при `state=1`)</a>
<a>- сообщение о причине неудачного обновления записи при `state=0`)</a>

<h4>Примеры JSON-ответов:</h4>

```
{ "status": 200, "message": "Success", "state": 1 }
{ "status": 400, "message": "It's not a NEW status of the record", "state": 0}
```

<h3>Метод <i>GET+email</i> API/submitData/?user_email=email</h3>

Возвращает данные всех объектов, отправленных на сервер пользователем с почтой email.
Пример запроса:

```
GET API/submitData/?user_email=sohuga5656@gmail.com
```