# Swagger з JWT Авторизацією - Інструкція

## 1️⃣ Запуск сервера

```bash
python app.py
```

Сервер запуститься на `http://127.0.0.1:5000`

---

## 2️⃣ Доступ до Swagger UI

Відкрий у браузері:

```
http://127.0.0.1:5000/apidocs
```

---

## 3️⃣ Отримання JWT токена

### Крок 1: Натисни на endpoint `/api/auth/login`

- Розкрий "Authentication" секцію
- Натисни "Try it out"

### Крок 2: Введи дані для логіну

```json
{
  "username": "testuser"
}
```

> ℹ️ Пароль не обов'язковий для демо. Можеш вписати будь-яке ім'я користувача.

### Крок 3: Натисни "Execute"

Ти отримаєш відповідь:

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "expires_in": 3600,
  "message": "Token generated for user: testuser"
}
```

**Скопіюй токен (значення поля `token`)**

---

## 4️⃣ Використання токена для доступу до захищених endpoint'ів

### На Swagger UI:

**Спосіб 1 (рекомендовано):**

1. Натисни кнопку **"Authorize"** (вгорі праворуч, замок)
2. В модальному вікні введи в поле "Value":
   ```
   Bearer YOUR_TOKEN_HERE
   ```
   (замість `YOUR_TOKEN_HERE` вставь скопійований токен)
3. Натисни "Authorize"
4. Тепер усі запити будуть містити цей токен автоматично

**Спосіб 2 (ручне введення):**

1. Для кожного endpoint'а натисни "Try it out"
2. Знайди поле "Authorization" в headers
3. Введи:
   ```
   Bearer YOUR_TOKEN_HERE
   ```

---

## 5️⃣ Приклади запитів

### Отримати всіх користувачів

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://127.0.0.1:5000/api/users
```

### Отримати статистику

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://127.0.0.1:5000/api/stats
```

### Отримати тест-результати

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" "http://127.0.0.1:5000/api/test-results?limit=5&offset=0"
```

---

## 6️⃣ Помилки авторизації

| Помилка                                     | Причина                         | Рішення                                     |
| ------------------------------------------- | ------------------------------- | ------------------------------------------- |
| `401 - Token is missing!`                   | Забув передати токен            | Натисни "Authorize" і введи токен           |
| `401 - Invalid or expired token`            | Токен невалідний або закінчився | Отримай новий токен через `/api/auth/login` |
| `401 - Invalid Authorization header format` | Неправильний формат             | Используй формат: `Bearer TOKEN`            |

---

## 7️⃣ Захищені endpoint'и

Всі ці endpoint'и потребують JWT токена:

- `GET /api/users` - Усі користувачі
- `GET /api/users/{id}` - Користувач за ID
- `GET /api/testers` - Усі тестувальники
- `GET /api/testers/{id}` - Тестувальник за ID
- `GET /api/test-plans` - Усі тест-плани
- `GET /api/test-plans/{id}` - Тест-план за ID
- `GET /api/test-cases` - Усі тест-кейси
- `GET /api/test-cases/{id}` - Тест-кейс за ID
- `GET /api/test-steps` - Усі тест-кроки
- `GET /api/test-steps/{id}` - Тест-крок за ID
- `GET /api/test-results` - Усі тест-результати (з пагінацією)
- `GET /api/test-results/{id}` - Тест-результат за ID
- `GET /api/stats` - Статистика БД

---

## 8️⃣ Публічні endpoint'и (без авторизації)

- `POST /api/auth/login` - Отримання токена
- `GET /api/health` - Перевірка здоров'я сервера

---

## ⚙️ Зміна SECRET_KEY (для продакшену)

У файлі `app.py` знайди:

```python
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
```

Змініть на щось більш безпечне:

```python
app.config['SECRET_KEY'] = 'ваш-дуже-довгий-секретний-ключ-змініть-це'
```

---

## ✅ Готово!

Тепер ваш Swagger має повну JWT авторизацію! 🔒
