# FlavorFit

## Запуск через Docker

### 1. Создайте файл окружения

Скопируйте `.env.example` и настройте переменные:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example backend/.env
```
### 2. Запустите приложение

```bash
docker-compose up --build
```
