# Docker: Guia de estudio y referencia practica

## 1. Que es Docker

Docker es una plataforma que permite empaquetar una aplicacion junto con sus dependencias, configuracion y entorno de ejecucion dentro de una **imagen**.

Esa imagen luego se ejecuta como un **contenedor**.

Idea central:

- una **imagen** es la plantilla
- un **contenedor** es la instancia en ejecucion de esa plantilla

Esto evita el clasico problema de desarrollo:

> "En mi maquina funciona"

---

## 2. Conceptos clave

### Imagen

Una imagen es un paquete inmutable que contiene:

- sistema base
- runtime
- librerias
- dependencias
- codigo fuente
- configuracion

Ejemplo:

```bash
docker pull python:3.12-alpine
```

### Contenedor

Un contenedor es una instancia en ejecucion de una imagen.

```bash
docker run python:3.12-alpine python --version
```

### Dockerfile

Es el archivo donde definis como construir una imagen.

### Volumen

Permite persistir datos o montar carpetas entre tu maquina y el contenedor.

### Red

Permite que los contenedores se comuniquen entre si.

### Docker Compose

Permite definir y levantar varios servicios con un solo archivo YAML.

---

## 3. Flujo de trabajo mental

1. Escribis un `Dockerfile`
2. Construis una imagen
3. Ejecutas un contenedor
4. Si tenes varios servicios, usas `docker compose`
5. Si necesitas persistencia, agregas volumenes
6. Si necesitas comunicacion entre servicios, usas la red de Compose

---

## 4. Dockerfile explicado

Un `Dockerfile` define paso a paso como construir una imagen.

### Estructura tipica

```dockerfile
FROM python:3.12-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Instrucciones importantes

#### `FROM`

Define la imagen base.

```dockerfile
FROM python:3.12-alpine
```

Buenas practicas:

- usar imagenes oficiales
- elegir versiones explicitas
- evitar `latest` en proyectos serios

#### `WORKDIR`

Define el directorio de trabajo dentro del contenedor.

```dockerfile
WORKDIR /app
```

#### `COPY`

Copia archivos desde tu maquina a la imagen.

```dockerfile
COPY requirements.txt .
COPY . .
```

#### `RUN`

Ejecuta comandos durante el build.

```dockerfile
RUN pip install -r requirements.txt
```

#### `ENV`

Define variables de entorno.

```dockerfile
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
```

#### `EXPOSE`

Documenta el puerto interno de la aplicacion.

```dockerfile
EXPOSE 5000
```

#### `CMD`

Define el comando por defecto al arrancar el contenedor.

```dockerfile
CMD ["flask", "run"]
```

---

## 5. Tu Dockerfile actual explicado

Tu archivo actual sigue esta estructura:

```dockerfile
FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
```

### Que hace cada linea

- `FROM python:3.7-alpine`: usa Python 3.7 sobre Alpine
- `WORKDIR /code`: define `/code` como carpeta de trabajo
- `ENV ...`: configura Flask
- `RUN apk add ...`: instala paquetes del sistema necesarios
- `COPY requirements.txt requirements.txt`: copia dependencias
- `RUN pip install -r requirements.txt`: instala Flask y Redis
- `EXPOSE 5000`: documenta el puerto usado por Flask
- `COPY . .`: copia el codigo fuente
- `CMD ["flask", "run"]`: inicia la app

### Mejoras recomendadas

- usar una version mas moderna de Python
- agregar `.dockerignore`
- fijar versiones en `requirements.txt`
- mantener la imagen lo mas liviana posible

---

## 6. Build de imagenes

### Construir una imagen

```bash
docker build -t mi-app .
```

### Construir con tag especifico

```bash
docker build -t mi-app:1.0 .
```

### Ver imagenes disponibles

```bash
docker images
```

### Eliminar una imagen

```bash
docker rmi mi-app
```

---

## 7. Contenedores: comandos mas usados

### Ejecutar un contenedor

```bash
docker run mi-app
```

### Ejecutarlo publicando puerto

```bash
docker run -p 5000:5000 mi-app
```

### Ejecutarlo en background

```bash
docker run -d -p 5000:5000 mi-app
```

### Ponerle nombre

```bash
docker run -d -p 5000:5000 --name web mi-app
```

### Ver contenedores corriendo

```bash
docker ps
```

### Ver todos

```bash
docker ps -a
```

### Ver logs

```bash
docker logs web
```

### Seguir logs

```bash
docker logs -f web
```

### Entrar al contenedor

```bash
docker exec -it web sh
```

### Detener contenedor

```bash
docker stop web
```

### Iniciar contenedor detenido

```bash
docker start web
```

### Reiniciar contenedor

```bash
docker restart web
```

### Eliminar contenedor

```bash
docker rm web
```

### Eliminar contenedor a la fuerza

```bash
docker rm -f web
```

---

## 8. Puertos

Cuando haces esto:

```bash
docker run -p 5000:5000 mi-app
```

el formato es:

```bash
HOST:CONTENEDOR
```

Ejemplo:

```bash
docker run -p 8080:5000 mi-app
```

La app escucha en `5000` dentro del contenedor, pero vos la abris desde `http://localhost:8080`.

---

## 9. Variables de entorno

### En `docker run`

```bash
docker run -e FLASK_ENV=development -p 5000:5000 mi-app
```

### En Compose

```yaml
environment:
  FLASK_ENV: development
  REDIS_HOST: redis
```

Buenas practicas:

- no hardcodear secretos
- usar `.env` cuando tenga sentido
- separar configuracion de codigo

---

## 10. Volumenes

Los volumenes resuelven dos problemas:

- persistir datos
- reflejar cambios locales dentro del contenedor

### Bind mount

```bash
docker run -v ${PWD}:/app mi-app
```

### Named volume

```bash
docker volume create datos_app
docker run -v datos_app:/data mi-app
```

### Ver volumenes

```bash
docker volume ls
```

### Inspeccionar un volumen

```bash
docker volume inspect datos_app
```

### Eliminar un volumen

```bash
docker volume rm datos_app
```

### Cuando usar cada uno

- bind mount: desarrollo
- named volume: persistencia real

---

## 11. Docker Compose

Docker Compose sirve para definir y ejecutar multiples servicios con un solo archivo.

### Ejemplo simple

```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
  redis:
    image: redis:alpine
```

### Comandos principales

#### Levantar servicios

```bash
docker compose up
```

#### Levantar y reconstruir

```bash
docker compose up --build
```

#### En segundo plano

```bash
docker compose up -d
```

#### Ver logs

```bash
docker compose logs
```

#### Seguir logs

```bash
docker compose logs -f
```

#### Ver servicios activos

```bash
docker compose ps
```

#### Detener y eliminar

```bash
docker compose down
```

#### Eliminar incluyendo volumenes

```bash
docker compose down -v
```

#### Ejecutar un comando en un servicio

```bash
docker compose exec web sh
```

#### Reconstruir imagenes

```bash
docker compose build
```

---

## 12. Tu `docker-compose.yaml` explicado

Tu archivo define dos servicios:

- `web`
- `redis`

```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - redis
    volumes:
      - .:/code
    environment:
      FLASK_ENV: development

  redis:
    image: "redis:alpine"
```

### Que significa cada parte

#### `build: .`

Construye la imagen de `web` usando el `Dockerfile` de la carpeta actual.

#### `ports`

```yaml
ports:
  - "5000:5000"
```

Mapea el puerto `5000` del host al `5000` del contenedor.

#### `depends_on`

```yaml
depends_on:
  - redis
```

Define que `web` depende de `redis`.

Importante:

- controla el orden de inicio
- no garantiza que Redis este listo para recibir conexiones

#### `volumes`

```yaml
volumes:
  - .:/code
```

Monta tu carpeta local dentro del contenedor en `/code`.

Ventaja:

- si cambias el codigo, el contenedor lo ve al instante

#### `environment`

```yaml
environment:
  FLASK_ENV: development
```

Inyecta variables de entorno al contenedor.

#### `image: redis:alpine`

Redis usa una imagen oficial ya preparada.

---

## 13. Comunicacion entre contenedores

En Compose, los servicios se comunican por nombre.

Tu app usa:

```python
host=os.getenv("REDIS_HOST", "redis")
```

Eso funciona porque el servicio se llama `redis` y Compose crea una red interna donde ese nombre es resoluble.

---

## 14. Redes en Docker

### Ver redes

```bash
docker network ls
```

### Inspeccionar una red

```bash
docker network inspect bridge
```

### Crear una red propia

```bash
docker network create mi-red
```

### Ejecutar un contenedor en una red

```bash
docker run --network mi-red nginx
```

Con Compose normalmente no hace falta crear la red manualmente.

---

## 15. `.dockerignore`

Muy importante para evitar copiar archivos innecesarios al build context.

Ejemplo:

```gitignore
__pycache__
.git
.venv
env
node_modules
.pytest_cache
*.log
```

Ventajas:

- builds mas rapidos
- imagenes mas livianas
- menos riesgo de copiar basura o secretos

---

## 16. Buenas practicas de Dockerfile

### 1. Usar imagenes base especificas

Mejor:

```dockerfile
FROM python:3.12-alpine
```

Peor:

```dockerfile
FROM python:latest
```

### 2. Aprovechar la cache

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

### 3. Mantener imagenes chicas

- usar imagenes livianas
- limpiar temporales
- instalar solo lo necesario

### 4. No meter secretos en la imagen

Nunca hardcodear:

- passwords
- tokens
- API keys

### 5. Un proceso principal por contenedor

Es una regla muy util.

### 6. Fijar versiones de dependencias

Mejor:

```txt
flask==3.0.3
redis==5.0.4
```

Peor:

```txt
flask
redis
```

---

## 17. Buenas practicas con Compose

- usar Compose para desarrollo local
- separar servicios claramente
- usar variables de entorno
- usar volumenes para hot reload en desarrollo
- usar named volumes para bases de datos
- no confiar solo en `depends_on` para readiness

---

## 18. Comandos de limpieza

### Ver espacio usado por Docker

```bash
docker system df
```

### Limpiar contenedores detenidos, redes no usadas e imagenes dangling

```bash
docker system prune
```

### Limpiar todo lo no usado, incluyendo imagenes

```bash
docker system prune -a
```

### Eliminar volumenes no usados

```bash
docker volume prune
```

Usalos con criterio.

---

## 19. Debugging

### Caso 1: el contenedor arranca y se apaga

```bash
docker ps -a
docker logs <container_id>
```

### Caso 2: la app no responde

Revisar:

- si el puerto esta publicado
- si la app escucha en `0.0.0.0`
- si el contenedor sigue corriendo

### Caso 3: un servicio no se conecta a otro

Revisar:

- nombre del servicio
- variables de entorno
- puerto interno
- red de Compose

### Caso 4: los cambios no se reflejan

Revisar:

- si hay un volumen montado
- si hace falta rebuild
- si el proceso recarga cambios

### Caso 5: error durante el build

Revisar:

- nombres de archivos
- dependencias del sistema
- contexto de build

---

## 20. Diferencia entre `RUN` y `CMD`

### `RUN`

Se ejecuta al construir la imagen.

```dockerfile
RUN pip install -r requirements.txt
```

### `CMD`

Se ejecuta al arrancar el contenedor.

```dockerfile
CMD ["flask", "run"]
```

Regla rapida:

- `RUN` construye
- `CMD` ejecuta

---

## 21. Diferencia entre imagen y contenedor

Analogias utiles:

- imagen = plantilla
- contenedor = ejecucion real

Podes crear muchos contenedores desde una misma imagen.

---

## 22. Diferencia entre bind mount y named volume

### Bind mount

```yaml
volumes:
  - .:/code
```

Ideal para:

- desarrollo
- editar codigo en vivo

### Named volume

```yaml
volumes:
  - datos_redis:/data
```

Ideal para:

- persistencia de base de datos
- datos administrados por Docker

---

## 23. Como levantar tu ejemplo `composetest`

Ubicate en la carpeta del proyecto:

```bash
cd /f/DocumentosN/Dockert-Udemy-2026/composetest
```

### Levantar el proyecto

```bash
docker compose up --build
```

### En segundo plano

```bash
docker compose up -d --build
```

### Ver logs

```bash
docker compose logs -f
```

### Probar la app

Abrir:

```text
http://localhost:5000
http://localhost:5000/about
```

### Bajar todo

```bash
docker compose down
```

---

## 24. Posibles mejoras para tu ejemplo

### Mejorar `requirements.txt`

```txt
flask==3.0.3
redis==5.0.4
```

### Mejorar `app.py`

Agregar reintentos cuando Redis todavia no esta listo.

### Mejorar el `Dockerfile`

- actualizar Python
- agregar `.dockerignore`
- reducir dependencias si no son necesarias

### Mejorar Compose

```yaml
environment:
  FLASK_ENV: development
  REDIS_HOST: redis
  REDIS_PORT: 6379
```

---

## 25. Cheatsheet de comandos mas usados

### Imagenes

```bash
docker build -t mi-app .
docker images
docker rmi mi-app
docker pull nginx
```

### Contenedores

```bash
docker run -p 5000:5000 mi-app
docker run -d --name web mi-app
docker ps
docker ps -a
docker stop web
docker start web
docker restart web
docker rm web
docker logs web
docker logs -f web
docker exec -it web sh
```

### Compose

```bash
docker compose up
docker compose up --build
docker compose up -d
docker compose ps
docker compose logs
docker compose logs -f
docker compose build
docker compose exec web sh
docker compose down
docker compose down -v
```

### Volumenes y redes

```bash
docker volume ls
docker volume inspect nombre_volumen
docker volume prune
docker network ls
docker network inspect bridge
```

### Limpieza

```bash
docker system df
docker system prune
docker system prune -a
```

---

## 26. Errores comunes de principiante

### 1. Usar `localhost` dentro del contenedor

Si un contenedor quiere hablar con otro, normalmente debe usar el nombre del servicio, no `localhost`.

### 2. No publicar puertos

Si no publicas puertos, no podes acceder desde tu maquina.

### 3. Escuchar en `127.0.0.1`

Dentro de contenedores, muchas apps deben escuchar en `0.0.0.0`.

### 4. Copiar demasiados archivos al build

Se soluciona con `.dockerignore`.

### 5. No entender cuando reconstruir

Si cambia el codigo y usas volumen, puede no hacer falta rebuild.

Si cambia el `Dockerfile` o una dependencia, normalmente si hace falta.

### 6. Confiar demasiado en `depends_on`

El contenedor puede arrancar antes de que el servicio dependiente este listo.

---

## 27. Ruta sugerida para volverte fuerte en Docker

### Nivel 1: base

Dominar:

- imagenes
- contenedores
- puertos
- logs
- `Dockerfile`
- `docker run`

### Nivel 2: productividad

Dominar:

- `docker compose`
- volumenes
- redes
- variables de entorno
- debugging

### Nivel 3: nivel profesional

Aprender:

- multi-stage builds
- optimizacion de imagenes
- healthchecks
- CI/CD con Docker
- registries
- seguridad de imagenes
- Docker en produccion

---

## 28. Recomendaciones para seguir

Temas que te conviene estudiar despues:

- multi-stage builds
- Docker Hub y registries privados
- healthcheck
- Nginx como reverse proxy
- persistencia con Postgres y MySQL
- imagenes slim vs alpine
- Docker en GitHub Actions
- Kubernetes como siguiente paso

---

## 29. Resumen final

Si queres volverte fuerte en Docker, tenes que dominar estas ideas:

- construir imagenes con `Dockerfile`
- ejecutar contenedores correctamente
- mapear puertos
- usar variables de entorno
- persistir datos con volumenes
- conectar servicios con Compose
- leer logs y depurar errores rapido

Docker no se aprende solo leyendo.

La forma correcta es:

1. levantar ejemplos
2. romper cosas
3. leer logs
4. corregir
5. repetir

Ese ciclo es el que realmente te vuelve bueno.

---

## 30. Nivel avanzado

Esta seccion ya entra en practicas mas cercanas a proyectos reales.

Los temas mas importantes para dar el siguiente salto son:

- `multi-stage builds`
- `healthcheck`
- `.dockerignore`
- separar Docker de desarrollo y produccion
- usar bases de datos con persistencia real

---

## 31. Multi-stage builds

Un multi-stage build permite usar varias etapas dentro de un mismo `Dockerfile`.

La idea es simple:

- en una etapa compilas o preparas archivos
- en la etapa final copias solo lo necesario

Ventajas:

- imagenes mas chicas
- menos superficie de ataque
- builds mas limpios
- menos herramientas innecesarias en produccion

### Ejemplo basico

```dockerfile
FROM python:3.12-alpine AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

FROM python:3.12-alpine

WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Que esta pasando

- primera etapa: instala dependencias
- segunda etapa: arranca desde una imagen limpia
- solo copia lo necesario desde `builder`

### Cuando conviene usarlo

- apps compiladas
- proyectos grandes
- imagenes para produccion
- cuando queres reducir peso final

---

## 32. Healthcheck

`healthcheck` sirve para que Docker pueda saber si el contenedor esta realmente sano, no solo iniciado.

Eso es importante porque un contenedor puede estar corriendo pero la app igual puede estar rota.

### Ejemplo en Dockerfile

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:5000/ || exit 1
```

### Ejemplo en Compose

```yaml
services:
  web:
    build: .
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:5000/"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
```

### Para que sirve en la practica

- detectar apps colgadas
- mejorar monitoreo
- coordinar servicios dependientes
- dar mejor visibilidad en entornos mas serios

### Ver estado de salud

```bash
docker ps
docker inspect <container_id>
```

En `inspect` vas a encontrar el bloque `Health`.

---

## 33. `.dockerignore` en serio

`.dockerignore` evita que Docker envie archivos innecesarios al contexto de build.

Eso afecta:

- velocidad de build
- tamano del contexto
- riesgo de copiar secretos
- orden y limpieza del proyecto

### Ejemplo recomendado para Python

```gitignore
__pycache__
*.pyc
.pytest_cache
.mypy_cache
.venv
venv
env
.git
.gitignore
*.log
.DS_Store
node_modules
.env
```

### Regla practica

Todo lo que no necesite entrar en la imagen, deberia evaluarse para quedar fuera del contexto.

---

## 34. Dockerfile de desarrollo vs produccion

Uno de los errores mas comunes es usar el mismo `Dockerfile` para todo.

En proyectos chicos puede servir al principio, pero en entornos reales conviene separar.

### Objetivo de desarrollo

- rapidez para iterar
- volumen montado
- herramientas de debug
- recarga automatica

### Objetivo de produccion

- imagen chica
- seguridad
- reproducibilidad
- menos dependencias
- arranque estable

### Ejemplo de Dockerfile para desarrollo

```dockerfile
FROM python:3.12-alpine

WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["flask", "run", "--debug"]
```

### Ejemplo de Dockerfile para produccion

```dockerfile
FROM python:3.12-alpine

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

### Diferencias clave

- en desarrollo suele haber volumenes montados
- en desarrollo suele haber debug
- en produccion conviene usar `gunicorn` u otro servidor serio
- en produccion conviene reducir al minimo dependencias y herramientas

---

## 35. Compose de desarrollo vs produccion

Tambien conviene pensar Compose de forma separada.

### Desarrollo

```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      FLASK_ENV: development
```

### Produccion

```yaml
services:
  web:
    image: mi-app:1.0
    ports:
      - "5000:5000"
    restart: always
```

Idea central:

- desarrollo: mas flexible
- produccion: mas estable y predecible

---

## 36. Ejemplo con PostgreSQL y persistencia real

Este ejemplo ya se parece mas a un entorno util de backend real.

### Objetivo

Levantar:

- una app
- una base PostgreSQL
- un volumen persistente para la base

### Ejemplo de `docker-compose.yaml`

```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db
    environment:
      DB_HOST: db
      DB_PORT: 5432
      DB_NAME: appdb
      DB_USER: appuser
      DB_PASSWORD: secret123

  db:
    image: postgres:16-alpine
    restart: always
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: secret123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Que hace este Compose

- `web` levanta tu aplicacion
- `db` levanta PostgreSQL
- `postgres_data` guarda la data aunque el contenedor se elimine

### Por que el volumen importa

Sin volumen:

- borras el contenedor
- perdes la base

Con volumen:

- borras el contenedor
- los datos siguen existiendo

---

## 37. Como conectarte a PostgreSQL desde Python

Si despues migras tu ejemplo de Redis a Postgres, el patron general es este:

```python
import os
import psycopg2

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "db"),
    port=os.getenv("DB_PORT", "5432"),
    dbname=os.getenv("DB_NAME", "appdb"),
    user=os.getenv("DB_USER", "appuser"),
    password=os.getenv("DB_PASSWORD", "secret123"),
)
```

La clave conceptual es la misma que en Redis:

- el host no suele ser `localhost`
- el host es el nombre del servicio: `db`

---

## 38. Persistencia real: que tenes que entender

En Docker hay una diferencia enorme entre:

- filesystem del contenedor
- volumen persistente

### Filesystem del contenedor

Si el contenedor desaparece, esos datos pueden perderse.

### Volumen persistente

Los datos quedan fuera del ciclo de vida del contenedor.

Por eso:

- apps stateless pueden vivir sin volumen
- bases de datos casi siempre necesitan volumen

---

## 39. Ejemplo de healthcheck para PostgreSQL

En Compose podes agregar algo asi:

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: secret123
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5
```

Esto mejora bastante la observabilidad del servicio.

---

## 40. Estructura recomendada de archivos para un proyecto Docker serio

```text
mi-proyecto/
├── app.py
├── requirements.txt
├── Dockerfile
├── Dockerfile.dev
├── docker-compose.yaml
├── docker-compose.prod.yaml
├── .dockerignore
├── .env
└── README.md
```

### Idea de esta estructura

- `Dockerfile`: build principal
- `Dockerfile.dev`: entorno de desarrollo
- `docker-compose.yaml`: base local
- `docker-compose.prod.yaml`: ajustes de produccion
- `.dockerignore`: limpieza del contexto
- `.env`: configuracion

---

## 41. Comandos utiles para este nivel

### Ver detalles de un contenedor

```bash
docker inspect web
```

### Ver uso de recursos

```bash
docker stats
```

### Ver volumenes

```bash
docker volume ls
```

### Ver redes

```bash
docker network ls
```

### Reconstruir sin cache

```bash
docker build --no-cache -t mi-app .
```

### Levantar un override de Compose

```bash
docker compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d
```

---

## 42. Errores avanzados comunes

### 1. Imagen demasiado grande

Causas comunes:

- copiar demasiados archivos
- no usar `.dockerignore`
- instalar herramientas innecesarias

### 2. Base de datos sin persistencia

Si no definis volumen, tarde o temprano vas a perder datos.

### 3. Usar Flask de desarrollo en produccion

Para produccion conviene usar `gunicorn`, `uvicorn` u otro servidor preparado.

### 4. No separar configuracion por entorno

Desarrollo y produccion tienen necesidades distintas.

### 5. Creer que `depends_on` resuelve todo

No reemplaza readiness checks ni retry logic.

---

## 43. Recomendacion final de aprendizaje

Si queres pasar de principiante a alguien realmente solido, te conviene practicar este recorrido:

1. Dockerfile simple con una app Flask
2. Compose con Flask + Redis
3. Compose con Flask + PostgreSQL + volumen
4. agregar `.dockerignore`
5. separar dev y prod
6. agregar `healthcheck`
7. probar multi-stage build

Si haces esos siete pasos de verdad, ya no vas a estar estudiando Docker de memoria. Lo vas a estar entendiendo.
