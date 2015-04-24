#Lab2
Лабораторная работа №2 по дисциплине РСОИ, студент Аринкин Никита

Production: http://45.55.236.237/lab2

##Последовательность действий

Для получения данных необходимо:

1. Зарегистрировать/авторизовать пользователя на главной странице;

2. Зарегистрировать приложение;

3. Получить access_token;

4. Получить данные;

##Получение access_token

Вначале необходимо получить code, для этого нужно сделать GET запрос на /lab2/auth с обязательными параметрами:

client_id - должен совпадать с идентификатором, выданном приложению при его регистрации
redirect_uri - адрес, на который будет перенаправлен code
response_type - необходимое значение - 'code'

Пример запроса: http://http://45.55.236.237/lab2/auth/?client_id=62MMQWB7TUZQRBJR13IMKOR4BX5BSE0C&redirect_uri=http://localhost:8000/lab2/&response_type=code

При успешном запросе и подтверждении приложения будет произведен редирект: http://localhost:8000/lab2/?code=393e8c60b62f666222424695e0949207c40db665

Если неверно указан client_id:

``` json
 {
   "error":"invalid_request",
   "info":"client_id is not correct"
 }
```

Если неверно указан response_type:

``` json
 {
   "error":"invalid_request",
   "info":"value of response_type must be code"
 }
```

После получения code необходимо сделать POST запрос на /lab2/token с обязательными параметрами:

code - был получен на предыдущем шаге
client_id - должен соответствовать client_id, который использовался для получения code
client_secret - выдавался в паре с client_id при регистрации приложения
redirect_uri - адрес на который будет перенаправлен ответ
grant_type - необходимое значение - 'authorization_code'

Пример запроса: http://45.55.236.237/lab2/auth/token?client_id=fcfc3d7224ee0e13be2032dd1dc188828a62&redirect_uri=http://localhost&grant_type=grant_type&code=688ad5315bb79b9c9dd60ea4d853e29125e07dd7&client_secret=a4db93fcc214cd99bf46a53236012f8d53b9b016cbf3258dbaa6351531f0b3002ba8f839fb89eeac74f796068c5728e5e5e5

Ответ:

``` json
{       
  "refresh_token":"4fff521a9751de5fd5dd4e2ad342226c4e730cbda210990e7f01c8f2", 
  "token_type":"Bearer", 
  "access_token":"19a91b60de7d8062d3b9542548213ff07a2652854e9391b6e1b7dc42", 
  "expires":"2015-04-24 17:47:17"
}
```

Если неверно указан code :

``` json
{
  "error":"invalid_request",
  "info":"code is incorrect"
}
```

Если неверно указан client_id :

``` json
{
  "error":"invalid_request",
  "info":"client_id is invalid"
}
```

Если неверно указан grant_type :

``` json
{
  "error":"invalid_request",
  "info":"grant_type is invalid"
}
```

Если неверно указан client_secret :

``` json
{
  "error":"invalid_request",
  "info":"client_secret is invalid"
}
```

##Получение refresh_token

Для получения refresh_token необходимо сделать POST запрос на /myoauth/token/refresh с обязательными параметрами:

refresh_token - должен совпадать с refresh_token, который был выдан при получении access_token
grant_type - необходимое значение - 'refresh_token'

Пример запроса: http://45.55.236.237/lab2/auth/token?client_id=fcfc3d7224ee0e13be2032dd1dc188828a62&redirect_uri=http://localhost&grant_type=refresh_token&refresh_token=4fff521a9751de5fd5dd4e2ad342226c4e730cbda210990e7f01c8f2&client_secret=a4db93fcc214cd99bf46a53236012f8d53b9b016cbf3258dbaa6351531f0b3002ba8f839fb89eeac74f796068c5728e5e5e5

Ответ:

``` json
{
  "access_token":"66e743492a4ffa9fcea732c3c479c1f278d251ea",
  "expires_in":"120",
  "token_type":"Bearer",
  "refresh_token":"a72d727d34ec2986e4ff4bad7b4c351da35971f6"
}
```

Если неверно указан grant_type:

``` json
{
  "error":"invalid_request",
  "info": "grant_type is invalid"
}
```

Если неверно указан refresh_token:

``` json
{
  "error":"invalid_request",
  "info":"Invalid refresh token"
}
```

##Данные

В приложении для данных используются 2 сущности:

Производители /manufactures
Устройства /devices

Для получения данных необходимо сделать GET запрос с наличием в header'е параметра вида:

Authorization: Bearer $access_token 
, где $access_token - действительный access token

Если header содержит ошибочный параметр, то будет получен ответ:

``` json
{
  "error":"unauthorized"
}
```

Если действие access_token истекло, то будет получен ответ:

``` json
{
  "error":"token expired"
}
```

Примеры запросов для получения данных:

Запрос: http://45.55.236.237/lab2/manufacturers/1

Результат:

``` json
{ 
  "id": 1, 
  "name": "Apple", 
  "established": 1976, 
  "country": "USA" 
}
```

Запрос: http://45.55.236.237/lab2/manufacturers/?page=2&per_page=2 Результат:

``` json
{
  "current_page":2,
  "per_page":2,
  "total_entries":4,
  "entries":
  [{
      "id":3,
      "name": "LG", 
      "established": 1958, 
      "country": "South Korea" 
    },
    {
      "id":4,
      "name": "Sony", 
      "established": 1946, 
      "country": "Japan" 
    }]
}
```

Запрос: http://45.55.236.237/lab2/devices/1 Результат:

``` json
{ 
  "id": 1,
  "name": "Lada",
  "country": "Russia",
  "year": 1950 
}
```

Запрос: http://45.55.236.237/lab2/devices?page=1&per_page=3 Результат:

``` json
{
  "current_page":1, 
  "per_page":3,
  "total_entries":4,
  "entries":                                                                    
  [{
    "id":1,
    "name":"Lada",
    "country":"Russia",
    "year":1950
  },
  {
    "id":2,
    "name":"Nissan",
    "country":"Japan",
    "year":1890
  },
  {
    "id":3,
    "name":"Subaru",
    "country":"Japan",
    "year":1930
  }]
}
```