```bash
python3 -m venv lab1
source lab1/bin/activate
```

### База данных
#### Структура
```
/web
|   app.py
|   database.py
|   models.py
|   Dockerfile
/postgres_data
|   init.sql
docker-compose.yml
README.md
requirements.txt
```
```bash
docker run --name db_patients -p 5432:5432    -e POSTGRES_USER=user    -e POSTGRES_PASSWORD=password   -e POSTGRES_DB=db_patients    -e PGDATA=/var/lib/postgresql/data/pgdata    -d -v "$(pwd)/postgres_data":/var/lib/postgresql/data postgres
```

```
CREATE SEQUENCE IF NOT EXISTS patientid_seq START WITH 1;
CREATE TABLE IF NOT EXISTS patients (
 patientid INT PRIMARY KEY DEFAULT nextval('patientid_seq'),
 name TEXT NOT NULL
);
```

web Dockerfile
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

docker-compose.yml