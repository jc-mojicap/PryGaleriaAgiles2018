# Galeria videos

Este es un proyecto de apropiación técnologica del framework Django realizado para el curso de procesos de metodologías ágiles MISO4101 en la universidad de los Andes. Consiste en una galeria de videos y audios de Youtube en el que los usuarios pueden añadir clips sobre secciones especificas del video.

## Getting Started

Sigue estas instrucciones para tener una copia del proyecto corriendo localmente en tu maquina. Ver la seccion de despliegue para mas información.

### Prerequisitos

Para este proyecto se usaron las siguientes tecnologias.
* Python ver. 2.7.10
* Django ver. 1.11.15
* PostgreSQL

- Nota: Al clonar el proyecto no olvidar correr el siguiente comando para instalar todas las depedencias.
```
pip install -r requirements.txt
```
- Nota2: El archivo settings no esta incluido en el repositorio para que cada persona pueda manejarlas como desee.
- Nota3: En caso de no tener la base de datos se debe crear y suministrar las credenciales apropiadas en el archivo settings. 
- Nota4: Eventualmente añadire un archivo settings de ejemplo ...
- Nota5: Las 2 ultimas lineas de settings son requeridas para el despliegue en Heroku y deben permanecer comentadas si se trabaja localmente. 

### Instalación y despliegue

Con python y el entorno virtual correctamente configurado nos dirigimos a la carpeta donde esta ubicado el archivo manage.py y ejecutamos los siguientes comandos.

Hacemos las migraciones de los modelos

```
python manage.py makemigrations polls
```
Creamos el script de la base de datos, 0001 se reemplaza por el script que se desee correr (este archivo se crea en la carpeta migrations)
```
python manage.py sqlmigrate polls 0001
```
Realizamos las migraciones

```
python manage.py migrate 
```
De este modo tendremos la base de datos necesaria para correr el proyecto. Finalmente ejecutamos el siguiente comando para ejecutar el servidor, el cual estara disponible para nosotros en http://127.0.0.1:8000/
```
python manage.py runserver 
```

## Problemas comúnes

* **Problemas con las migraciones:** La mejor alternativa es eliminar la base de datos en postgres, truncar la tabla django_migrations, eliminar el archivo 0001_initial.py de la carpeta migrations y ejecutar nuevamente los comandos de la seccion instalacion. (Tambien es posible eliminar toda la base de datos y ejecutar los pasos)

* **Problemas para acceder al administrador:** es importante asegurarse que se cuenta con un superusuario para acceder al administrador. Esto se puede lograr con el comando 
```
python manage.py createsuperuser
```
* **No se muestran los videos en el index:** No olvidar que Tipo corresponde unicamente a "VIDEO" o "AUDIO" mientras que categoría puede ser cualquier valor (ej. romantico, comedia, tutorial, etc) 



## Built With

* [Django](https://www.djangoproject.com/) - El framework de python que utilizamos

## Authors
Grupo 4
* **Jorge Martin** 
* **Camilo Mojica**
* **Huber Galvis**
* **William Ravelo**
* **Zulma Castañeda**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
