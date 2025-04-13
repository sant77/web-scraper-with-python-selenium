![Static Badge](https://img.shields.io/badge/Python-3.9-green?logo=python)
![Static Badge](https://img.shields.io/badge/Conteiner-Docker-blue?logo=docker)
![Static Badge](https://img.shields.io/badge/Scraper-Selenium-green?logo=selenium)
![Static Badge](https://img.shields.io/badge/Linux-bullseye-pink?logo=debian)

# DIAN scraper API  ✒️

This API is designed to put Python knowledge into practice by performing web scraping on the DIAN (Colombian Tax Authority) application to obtain electronic invoices using the CUFE code.go cufe.


# Project Structure 📁
The project is organized into the following folders:

- `backend`: Contains the web scraper and the Dockerfile for building the image.


- `docker_compose`:  Contains the docker-compose file to launch the service.


# Running the API with Docker 🐋

## Creating the image
To deploy the service, navigate to the backend folder and run the following command to build the image:
```bash
    docker build -t flask-dane-scraper:v1.0.0 .
```
## Launching the container 🐳

To start the docker-compose service, go to the docker_compose folder and run the following command

```bash
    docker-compose -f docker-compose-local.yml -p "my-scraper" up -d
```

# Possible Improvements📝

-To improve speed, you could avoid starting a new Google Chrome driver for each CUFE. However, to prevent potential errors and losing scraper progress, a different approach was chosen.


# Useful Links🔗
- [Selenium Documentation](https://www.selenium.dev/documentation/)

- [Forum post with solution for installing Chrome in Docker](https://gist.github.com/varyonic/dea40abcf3dd891d204ef235c6e8dd79)

- [2Captcha – Automated reCAPTCHA Solver](https://2captcha.com/)

