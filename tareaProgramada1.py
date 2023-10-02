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

def generar_html_paises(info_paises):
    # Crear el documento HTML
    html = BeautifulSoup("<html><head><title>Información de Países</title></head><body></body></html>", "html.parser")

    # Agregar encabezado con estilo
    encabezado = html.new_tag("h1", style="color: blue; text-align: center;")
    encabezado.string = "Información de Países"
    html.body.append(encabezado)

    # Agregar tabla de países con estilo
    tabla = html.new_tag("table", style="width: 100%; border-collapse: collapse;")
    html.body.append(tabla)

    # Agregar encabezados de tabla con estilo
    encabezados = html.new_tag("tr")
    tabla.append(encabezados)
    encabezados_tags = ["Nombre", "Código", "Territorio", "Población", "Capital"]
    for encabezado_tag in encabezados_tags:
        th = html.new_tag("th", style="background-color: lightgray; padding: 10px; text-align: left;")
        th.string = encabezado_tag
        encabezados.append(th)

    # Contador para alternar colores de filas
    fila_color = 0

    # Agregar filas de datos de países con estilo alternado
    for pais in info_paises:
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if fila_color % 2 == 0 else '#99C2FF'};")
        fila_color += 1
        tabla.append(fila)
        nombre, codigos, poblacion, capital, area = pais[:5]
        for dato in [nombre, codigos[0], poblacion, capital, area[9]]:
            td = html.new_tag("td", style="padding: 5px;")
            td.string = str(dato)
            fila.append(td)

    # Guardar el archivo HTML
    with open("informacion_paises.html", "w", encoding="utf-8") as file:
        file.write(str(html))

# Llama a la función para generar el HTML basado en la información de países
infoPaises = crearPaisesLista(paises)  # Reemplaza datos_paises con tu lista de países
generar_html_paises(infoPaises)