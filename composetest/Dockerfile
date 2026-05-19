#Que es un Dockerfile?
# El Dockerfile es un archivo de texto donde se escriben las instrucciones que Docker va a seguir para construir una imagen.
# Esa imagen después se usa para crear contenedores con la aplicación, sus dependencias y su configuración.


FROM python:3.7-alpine

# Creacion de un directotrop de trabajo
WORKDIR /code

#Variables de entorno de Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0


#Ejecuciuon de comandos para instalar dependencias del sistema operativo
RUN apk add --no-cache gcc musl-dev linux-headers

# Insstalacion de dependencias
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#  Exponer puerto
EXPOSE 5000

# Copiar el codigo dentro de la imagen
# Copia todo el contenido del directorio actual a la imagen
COPY . . 


# Ejecucion del codio
CMD ["flask", "run"]