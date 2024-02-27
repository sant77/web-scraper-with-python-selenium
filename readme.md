![Static Badge](https://img.shields.io/badge/Python-3.9-green?logo=python)
![Static Badge](https://img.shields.io/badge/Conteiner-Docker-blue?logo=docker)
![Static Badge](https://img.shields.io/badge/Scraper-Selenium-green?logo=selenium)
![Static Badge](https://img.shields.io/badge/Linux-bullseye-pink?logo=debian)

# DIAN scraper API  ✒️

Esta API tiene como objetivo poner el practica los conocimientos en python, realizando un raspado web a la aplicación de la DIAN para obtener facturas electrónicas por medios del código cufe.


# Estructura del proyecto 📁
El proyecto se compone en las siguientes carpetas:

- `backend`: Contiene el webscraper y el archivo docker para crear la imagen.


- `docker_compose`:  Contiene el docker-compose para lanzar el servicio.


# Iniciando la API en docker 🐋

## Creando imagen
Para poder desplegar el servicio se debe ir a la carpeta de `backend` e insetar el siguiente comando con el fin de crear la imagen:

```bash
    docker build -t flask-dane-scraper:v1.0.0 .
```
## Lanzado contenedor 🐳
Para iniciar el docker compose se debe ingrasar a la carpeta `docker_compose` y escribir el siguiente comando:

```bash
    docker-compose -f docker-compose-local.yml -p "my-scraper" up -d
```

# Posibles mejoras📝

- Para optimizar en velocidad se podría probar no iniciar un dirver de google por cada Cufe, sin embargo para evitar posibles errores y perder el progreso de cada scraper mejor se optó por otra aproximación

- Se necesita un método mejor para vencer el recaptcha. Por ahora se hace a fuerza bruta, sin embargo para volumenes de datos grandes esto no es viable.

# Links de interés 🔗
- [Documentanción de Selenium](https://www.selenium.dev/documentation/)

- [Foro con la solución para instalar chrome en docker](https://gist.github.com/varyonic/dea40abcf3dd891d204ef235c6e8dd79)