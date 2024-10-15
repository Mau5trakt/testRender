import os
import pathlib
import unittest

from selenium import webdriver

# Encuentra el Identificador Uniforme de Recursos de un archivo
def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()

# Configura el controlador web utilizando Google Chrome
driver = webdriver.Chrome()
# Encuentra el URI de nuestro archivo recién creado
uri = file_uri("counter.html")

# Usa el URI para abrir la página web
driver.get(uri)

# Accede al título de la página actual
print(driver.title)
