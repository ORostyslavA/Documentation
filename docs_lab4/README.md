# Docs Lab 4

## Опис
Це лабораторна робота з запуску Redis, Kafka, Zookeeper та Kafka UI через Docker Compose.

## Не працює команда `docker exec -it docs_lab4-311_request_redis redis-cli`

У вашому `docker-compose.yml` контейнер Redis названий явно:

- `311_request_redis`

Тому правильна команда для підключення до Redis CLI:

```bash
docker exec -it 311_request_redis redis-cli
```

Якщо контейнер не запущено, спочатку запустіть Compose.

## Запуск сервісів

Перейдіть у каталог проекту та виконайте:

```bash
docker compose up -d
```

Перевірка стану:

```bash
docker compose ps
```

Або через `docker ps`:

```bash
docker ps
```

## Redis

Підключитися до Redis CLI:

```bash
docker exec -it 311_request_redis redis-cli
```

Якщо Redis працює, має повернутися:

```text
PONG
```

## Kafka та Kafka UI

Kafka UI доступний у браузері за адресою:

- `http://localhost:8080`

Kafka доступний на порту:

- `9092`

Zookeeper на порту:

- `2181`

## Kafka Console Producer / Consumer

Щоб запустити консольні утиліти Kafka, зайдіть у контейнер Kafka:

```bash
docker exec -it 311_request_kafka bash
```

### Producer

```bash
kafka-console-producer --broker-list localhost:9092 --topic test-topic
```

### Consumer

```bash
kafka-console-consumer --bootstrap-server localhost:9092 --topic test-topic --from-beginning
```

> У `docker-compose.yml` Kafka налаштована з `KAFKA_AUTO_CREATE_TOPICS_ENABLE=true`, тому тема створиться автоматично при першій відправці.

## Зупинка та видалення контейнерів

```bash
docker compose down
```

## Додатковий варіант для Redis через Compose

Якщо хочете використовувати `docker compose exec`, то команда буде такою:

```bash
docker compose exec redis redis-cli
```
