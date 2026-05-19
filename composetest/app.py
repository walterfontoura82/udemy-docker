import os
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
)

@app.route("/")
def hello():
    count = cache.incr("hits")
    return f"Hello from Docker! I have been seen {count} time(s).\n"

@app.route("/about")
def about():
    return "<h1> Estoy Frito al estar sin trabajo </h1>"
# import time
# import redis
# from flask import Flask



# # uso de Flask para crear una aplicación web
# app = Flask(__name__)

# # Uso de Redis para conectarse a un servidor Redis
# cache = redis.Redis(host='redis', port=6379)

# #Funcion: Bucle básico que nos pérmite intentar  nuestra peticion  varias veces si el servicio de redis no esta disponible
# def get_hit_count():
#     retries = 5
#     while True:
#         try:
#             return cache.incr('hits')
#         except redis.exceptions.ConnectionError as exc:
#             if retries == 0:
#                 raise exc
#             retries -= 1
#             time.sleep(0.5)

# @app.route('/')
# def hello():
#     count = get_hit_count()
#     return f'Hello from Docker! I have been seen {count} time(s).\n'

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)