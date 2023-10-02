#####################################################################
#Elaborado por: Alejandro Madrigal y Daniel Campos
#Fecha de creación: 21-09-2023 Hora: 10:00pm
#Fecha de finalización:
#Versión: 3.11.5
####################################################################
#importacion de librerias
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import sys
sys.setrecursionlimit(5000)
from lxml import etree
from bs4 import BeautifulSoup
#informacion de la tabla de paises convertida a matriz
df = pd.read_excel("paises.xlsx", sheet_name=0)
paises = df.to_numpy()


# se tuvo que cambiar NA porque retornaban valores sin informacion (nan)
def crearPaisesLista(paises):
    infoPaises=[]
    for pais in paises:
        countryCode = pais[0]
        countryName = pais[1]
        currencyCode = pais[2]
        population = pais[3]
        fipsCode = pais[4] if len(pais) > 4 else None
        isoNumeric = pais[5] if len(pais) > 5 else None
        capital = pais[6] if len(pais) > 6 else None
        continentName = pais[7] if len(pais) > 7 else None
        continentCode = pais[8] if len(pais) > 8 else None
        areaInSqKm = pais[9] if len(pais) > 9 else None
        languages = pais[10] if len(pais) > 10 else None
        isoAlpha3 = pais[11] if len(pais) > 11 else None
        geonameId = pais[12] if len(pais) > 12 else None
        infoPais=[countryName,[countryCode,fipsCode,isoNumeric,isoAlpha3,geonameId],currencyCode,population,capital,[continentName,continentCode],areaInSqKm,languages]
        infoPaises.append(infoPais)
    return infoPaises

# crear el archivo xml
root = ET.Element("paises")

def listaPaises(infoPaises):
    """
    """
    for paisData in infoPaises:
        pais = ET.SubElement(root, "pais")
        nombre = ET.SubElement(pais, "nombre")
        nombre.text = paisData[0]
        codigo = ET.SubElement(pais, "codigo")
        codigo.text = paisData[1][0]
        fips = ET.SubElement(pais, "fips")
        fips.text = str(paisData[1][1])
        iso = ET.SubElement(pais, "iso")
        iso.text = str(paisData[1][2])
        isoAlpha = ET.SubElement(pais, "isoAlpha")
        isoAlpha.text = paisData[1][3]
        geoname = ET.SubElement(pais, "geoname")
        geoname.text = str(paisData[1][4])
        moneda = ET.SubElement(pais, "moneda")
        moneda.text = paisData[2]
        poblacion = ET.SubElement(pais, "poblacion")
        poblacion.text = str(paisData[3])
        capital = ET.SubElement(pais, "capital")
        capital.text = paisData[4]
        continente = ET.SubElement(pais, "continente")
        continente.text = paisData[5][0]
        continenteCodigo = ET.SubElement(pais, "continenteCodigo")
        continenteCodigo.text = paisData[5][1]
        area = ET.SubElement(pais, "area")
        area.text = str(paisData[6])
        idiomas = ET.SubElement(pais, "idiomas")
        idiomas.text = paisData[7]
        tree = ET.ElementTree(root)
        tree.write("paises.xml", encoding="utf-8", xml_declaration=True)

# call the function to create the infoPaises list
infoPaises = crearPaisesLista(paises)

# call the function to create the XML file
listaPaises(infoPaises)

def crear_tabla_paises_por_continente(infoPaises):
    # Crear un diccionario para agrupar los países por continente
    paises_por_continente = {}
    for paisData in infoPaises:
        continente = paisData[5][0]
        if continente not in paises_por_continente:
            paises_por_continente[continente] = []
        paises_por_continente[continente].append(paisData)

    # Crear un objeto BeautifulSoup
    html = BeautifulSoup("<html><body></body></html>", "html.parser")

    # Crear una tabla HTML
    tabla = html.new_tag("table")

    # Agregar encabezados de la tabla
    encabezado = html.new_tag("tr")
    encabezado.append(html.new_tag("th", text="Continente"))
    encabezado.append(html.new_tag("th", text="Países"))
    tabla.append(encabezado)

    # Agregar filas para cada continente y sus países
    for continente, paises in paises_por_continente.items():
        fila_continente = html.new_tag("tr")
        # Columna de Continente
        fila_continente.append(html.new_tag("td", text=continente))
        # Columna de Países
        td_paises = html.new_tag("td")
        for pais in paises:
            paises_lista = pais[0].split("<br>")
            for nombre_pais in paises_lista:
                td_paises.append(nombre_pais)
                td_paises.append(html.new_tag("br"))
        fila_continente.append(td_paises)
        tabla.append(fila_continente)

    # Agregar la tabla al cuerpo del HTML
    html.body.append(tabla)

    # Guardar el HTML en un archivo
    with open("paises_por_continente.html", "w", encoding="utf-8") as file:
        file.write(str(html))

infoPaises = crearPaisesLista(paises)

# Crear el archivo XML
listaPaises(infoPaises)

# Crear la tabla HTML por continente
crear_tabla_paises_por_continente(infoPaises)