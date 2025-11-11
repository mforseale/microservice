# Microservice Example

RESTful микросервис на Python с Flask и PostgreSQL

## Функциональность

- CRUD операции для пользователей
- 6 RESTful endpoints
- Docker контейнеризация
- Обработка ошибок и логирование

## API Endpoints

- `GET /health` - проверка здоровья
- `GET /users` - получить всех пользователей  
- `GET /users/{id}` - получить пользователя по ID
- `POST /users` - создать пользователя
- `PUT /users/{id}` - обновить пользователя
- `DELETE /users/{id}` - удалить пользователя

## Запуск

```bash
# Клонировать репозиторий
git clone <url-репозитория>
cd microservice

# Запустить сервисы
docker-compose up --build

# Проверить работу
curl http://localhost:5000/health