Относительно лабораторной номер 2 добавлена базовая аутентифицкация, возвращающая jwt токен.
Для базовой авторизации нужно ввести логин/пароль пользователя используя пост метод '/login'
Вернется словарь, содержащий JWT токен.
Этот токен необходимо передавать в азпросах с аутентификацией под bearer token.
В лабораторной 4 авторзизация доступна для методов remove_recipient и update_recipient.

### `/create_recipient/`

- **Метод:** POST
- **Тело Запроса:**
  ```json
  {
    "recipient_login": "строка",
    "first_name": "строка",
    "second_name": "строка",
    "address": "строка",
    "password": "строка"
  }
  ```
- **Ответ:**
  ```json
  {
    "recipient_id": целое число
  }
  ```

### `/update_recipient/{recipient_id}`

- **Метод:** PUT
- **URL Параметры Запроса:**
  - `recipient_id`: целое число
- **Тело Запроса:**
  ```json
  {
    "recipient_login": "строка",
    "first_name": "строка",
    "second_name": "строка",
    "address": "строка",
    "password": "строка"
  }
  ```
- **Ответ:**
  ```json
  {
    "message": "Получатель успешно обновлен"
  }
  ```

### `/get_recipient_details/{recipient_id}`

- **Метод:** GET
- **URL Параметры Запроса:**
  - `recipient_id`: целое число
- **Ответ:**
  ```json
  {
    "recipient_id": целое число,
    "recipient_login": "строка",
    "first_name": "строка",
    "second_name": "строка",
    "address": "строка",
    "password": "строка"
  }
  ```

### `/search_by_name/`

- **Метод:** GET
- **Параметры Запроса:**
  - `first_name`: строка (обязательный)
  - `second_name`: строка (обязательный)
- **Ответ:**
  ```json
  [
    {
      "recipient_id": целое число,
      "recipient_login": "строка",
      "first_name": "строка",
      "second_name": "строка",
      "address": "строка",
      "password": "строка"
    }
  ]
  ```

### `/search_by_recipient_login/`

- **Метод:** GET
- **Параметры Запроса:**
  - `recipient_login`: строка (обязательный)
- **Ответ:**
  ```json
  [
    {
      "recipient_id": целое число,
      "recipient_login": "строка",
      "first_name": "строка",
      "second_name": "строка",
      "address": "строка",
      "password": "строка"
    }
  ]
  ```
