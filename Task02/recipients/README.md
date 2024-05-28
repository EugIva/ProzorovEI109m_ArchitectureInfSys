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
