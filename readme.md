## Guane-intern-fastapi

### Interpretación del problema

El software fue desarrollado bajo la interpretación de que las funcionalidades corresponden a una aplicación web
utilizada en servicios de adopción de mascotas, específicamente perros. Las funcionalidades implementadas son:

- Consultar información de todos los perros registrados.
- Consultar información de un perro en específico.
- Consultar información de todos los perros adoptados.
- Un usuario puede registrar un nuevo canino.
- Un usuario puede asignar un adoptante a que este mismo registró.
- Un usuario puede eliminar un perro de los que este mismo registró.
- Un usuario puede cambiar su información personal.
- Realizar registro de nuevos usuarios.

**Nota:** Las operaciones de "críticas" sobre los caninos, tales como :registrar, cambiar el estado a adoptado y
eliminar están protegidas por políticas de acceso basadas en JWT donde además se verifica si el usuario si operar sobre
la entidad.

### Esquema de base de datos

![V Gowin - Página 2](https://user-images.githubusercontent.com/33033057/113798313-8caba300-9718-11eb-9117-42e32007d747.png)

### Requisitos de desarrollo

- PostgreSQL
- Python 3.8
- Pipenv
- Docker
- Docker-compose

### Environments:

La aplicación contiene dos archivos con ejemplo de las variables de entorno ".env.example" y "composer.example.env" que
deben ser cambiados a conveniencia y cambiar el nombre ".env" para ejecutar la aplicación en un entorno local y "
composer.env" para un entorno dockerizado.
**NOTA:** No olvide borrar los comentarios en los environments para evitar problemas.

```shell
APP_NAME="Guane intern fastapi"
HOST=rapidog-db #is a service db !!DONT CHANGE!!
DATABASE=rapidog #the same as in the DB/create.sql file
USER_DB=rapi #USER for postgres database
PASSWORD_DB=root # PASSWORD for postgres
PORT_DB= 5432
Jwt_TOKEN=d33e53e30ee37e5b550b8a87b84542fcd471c188447f4cea2cf1eac040ca2e3b
API_IMAGE=https://dog.ceo/api/breeds/image/random
DATABASE_TESTING=rapidog_testing #the other database in the DB/create.sql file
POSTGRES_USER=rapi #same name in USER_DB
POSTGRES_PASSWORD=root #same password that PASSWORD_DB
```

### Docker-compose

La aplicación se ejecuta en el puerto 3000 por defecto, además para asegurar un correcto funcionamiento es necesario
levantar los servicios en el siguiente orden

1. Servicio de base de datos

```shell
docker-compose up -d rapidog-db
```

2. Servicio de aplicación

```shell
docker-compose up -d web-app
```

### Pruebas

Se desarrollaron pruebas con datos "dummys" para verificar el correcto funcionamieto de la aplicación que pueden ser
ejecutadas con el siguiente comando

1. Aplicación en local

```shell
pytest 
```

2. Aplicación en docker

```shell
docker-compose exec web-app pytest tests --cov "."
```

![Screenshot from 2021-04-09 17-53-43](https://user-images.githubusercontent.com/33033057/114248179-96254d00-995c-11eb-9328-c72e3e16e282.png)

### Despliegue

La aplicación se encuentra desplegada en una máquina virtual EC2 y puede ser consultada en el siguiente enlace:
http://3.236.125.125:3000/docs
