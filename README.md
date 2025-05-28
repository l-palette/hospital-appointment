**Активация venv**
```bash
python3 -m venv venv
source venv/bin/activate
```
**Структура проекта**
```bash
project/
|    /web
|    |   app.py
|    |   database.py
|    |   models.py
|    |   Dockerfile
|    |   templates/
|    |   |   index.html
|    |   requirements.txt
|    /postgres_data
|    |   init.sql
|    |   pgdata/
|    requirements.txt
|    .gitignore
|    docker-compose.yml
|    README.md
```
# 1. Dockerfile для web-приложения
```Dockerfile
FROM alpine

RUN apk add python3
RUN apk add curl
RUN curl -O https://bootstrap.pypa.io/get-pip.py
RUN python3.12 get-pip.py --break-system-packages
RUN rm get-pip.py
RUN pip install Flask --break-system-packages

WORKDIR /web

COPY . /web

CMD ["python3", "app.py"]
```
# 2. База данных
**Запуск docker-контейнера postgres
```bash
docker run --name db_patients -p 5432:5432    
-e POSTGRES_USER=user    
-e POSTGRES_PASSWORD=password   
-e POSTGRES_DB=db_patients    
-e PGDATA=/var/lib/postgresql/data/pgdata    
-d -v "$(pwd)/postgres_data":/var/lib/postgresql/data 
postgres
```
**Таблицы**
```
CREATE SEQUENCE IF NOT EXISTS patientid_seq START WITH 1;
CREATE TABLE IF NOT EXISTS patient (
    id INT PRIMARY KEY DEFAULT nextval('patientid_seq'),
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    telephone VARCHAR(20) NOT NULL
);

CREATE SEQUENCE IF NOT EXISTS doctor_id START WITH 1;
CREATE TABLE doctor (
    id INT PRIMARY KEY DEFAULT nextval('doctor_id'),
    name VARCHAR(255) NOT NULL
);

CREATE SEQUENCE IF NOT EXISTS specialization_id START WITH 1;
CREATE TABLE specialization (
    id INT PRIMARY KEY DEFAULT nextval('specialization_id'),
    name VARCHAR(255) NOT NULL
);

CREATE SEQUENCE IF NOT EXISTS doctor_specialization_id START WITH 1;
CREATE TABLE doctor_specialization (
    id INT PRIMARY KEY DEFAULT nextval('doctor_specialization_id'),
    doctor_id INT REFERENCES doctor(id),
    specialization_id INT REFERENCES specialization(id)
);

CREATE SEQUENCE IF NOT EXISTS room_id START WITH 1;
CREATE TABLE room (
    id INT PRIMARY KEY DEFAULT nextval('room_id'),
    name VARCHAR(20) NOT NULL
);

CREATE SEQUENCE IF NOT EXISTS appointment_id START WITH 1;
CREATE TABLE appointment ( 
    id INT PRIMARY KEY DEFAULT nextval('appointment_id'),
    patient_id INT REFERENCES patient(id),
    doctor_id INT REFERENCES doctor(id),
    time TIME NOT NULL,
    date DATE NOT NULL,
    room_id INT REFERENCES room(id),
    status VARCHAR NOT NULL
);
```
# 3. Docker-compose docker-контейнеров web и бд
```bash
services:
  db:
    image: postgres:latest
    container_name: db_patients
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: db_patients
      PGDATA: /var/lib/postgresql/data/pgdata
    ports:
      - 5432:5432
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
      - ./postgres_data/init.sql:/docker-entrypoint-initdb.d/init.sql  

  web:
    build:
      context: ./web
      dockerfile: Dockerfile
    container_name: web_app
    ports:
      - 5000:5000
    depends_on:
      - db
    environment:
      DATABASE_URL: postgres://user:password@db:5432/db_patients
```
# 4. Сервисы приложения

**Пациенты**
1. Список пациентов

2. Добавление нового пациента

3. Получение данных о пациенте по id

4. Обновление данных о пациенте по id

5. Удаление пациента по id

**Доктора**

6. Список докторов

7. Добавление нового доктора + специализации

8. Получение данных о докторе по id + специализация

9. Обновление данных о докторе по id + специализация

10. Удаление доктора по id + специализация

**Специализации**

11. Список специализаций

12. Добавление новой специализации

13. Получение данных о специализации по id

14. Обновление данных о специализации по id

15. Удаление специализации по id

**Комнаты**

16. Список комнат

17. Добавление новой комнаты

18. Получение данных о комнате по id

19. Обновление данных о комнате по id

20. Удаление комнаты по id

**Записи**

21. Список записей 

22. Добавление новой записи

23. Получение данных о записи по id

24. Обновление данных о записи по id

25. Удаление записи по id

# 5. CI/CD

# 6. Скрипты миграции
Воспользуемся alembic:
### 1. Инициализация Alembic
В корне проекта выполните:

```bash
alembic init alembic
```

Это создаст структуру:

```
/alembic
    /versions
    env.py
    script.py.mako
alembic.ini
```
### 2. Настройка Alembic

Измените alembic.ini:

```ini
sqlalchemy.url = postgresql://user:password@localhost:5432/db_patients
```

    Измените alembic/env.py:

python

from models import Base  # Импортируйте ваши модели
target_metadata = Base.metadata

# Также обновите конфигурацию для работы с Docker
def run_migrations_online():
    config = context.config
    connectable = config.attributes.get("connection", None)
    
    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

    Добавьте в database.py или создайте новый файл models.py с определением всех моделей SQLAlchemy.
