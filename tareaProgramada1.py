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

def htmlContinente(infoPaises):
    # Preguntar al usuario por el continente de interés
    continenteElegido = input("Ingrese el nombre del continente del cual desea obtener información (Europe, North America, Asia, Antartica, Africa, Oceania ): ")##############CAMBIAR##############

    # Filtrar los países por continente
    filtrarPaises = [pais for pais in infoPaises if pais[5][0] == continenteElegido]

    if not filtrarPaises:
        print(f"No se encontraron países en el continente {continenteElegido}.")
        return

    # Crear el documento HTML
    html = BeautifulSoup("<html><head><title>Información de Países</title></head><body></body></html>", "html.parser")

    # Agregar encabezado con estilo
    encabezado = html.new_tag("h1", style="color: blue; text-align: center;")
    encabezado.string = f"Información de Países en el Continente {continenteElegido}"
    html.body.append(encabezado)

    # Agregar tabla de países con estilo
    tabla = html.new_tag("table", style="width: 100%; border-collapse: collapse;")
    html.body.append(tabla)

    # Agregar encabezados de tabla con estilo
    encabezados = html.new_tag("tr")
    tabla.append(encabezados)
    tags = ["Nombre", "Código", "Población", "Capital", "Área"]
    for tags in  tags:
        th = html.new_tag("th", style="background-color: lightgray; padding: 10px; text-align: left;")
        th.string =  tags
        encabezados.append(th)

    # Contador para alternar colores de filas
    color = 0

    # Agregar filas de datos de países con estilo alternado
    for pais in filtrarPaises:
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if color % 2 == 0 else '#99C2FF'};")
        color += 1
        tabla.append(fila)
        nombre, codigos, poblacion, capital, area = pais[0], pais[1], pais[3], pais[4], pais[7]
        for dato in [nombre, codigos[0], poblacion, capital, area]:
            td = html.new_tag("td", style="padding: 5px;")
            td.string = str(dato)
            fila.append(td)

    # Guardar el archivo HTML
    with open(f"informacion_{continenteElegido}.html", "w", encoding="utf-8") as file:
        file.write(str(html))
# Llama a la función para generar el HTML basado en la información de países
infoPaises = crearPaisesLista(paises)  # Reemplaza datos_paises con tu lista de países
htmlContinente(infoPaises)

def poblacionMayorMenor(infoPaises):
    # Implementar ordenación personalizada por población de mayor a menor
    poblacionMayorMenor= []

    while infoPaises:
        maximo = infoPaises[0]
        for pais in infoPaises:
            if pais[3] > maximo[3]:
                maximo = pais
        poblacionMayorMenor.append(maximo)
        infoPaises.remove(maximo)

    # Crear el documento HTML
    html = BeautifulSoup("<html><head><title>Información de Países por Población</title></head><body></body></html>", "html.parser")

    # Agregar encabezado con estilo
    encabezado = html.new_tag("h1", style="color: blue; text-align: center;")
    encabezado.string = "Información de Países por Población"
    html.body.append(encabezado)

    # Agregar tabla de países con estilo
    tabla = html.new_tag("table", style="width: 100%; border-collapse: collapse;")
    html.body.append(tabla)

    # Agregar encabezados de tabla con estilo
    encabezados = html.new_tag("tr")
    tabla.append(encabezados)
    encabezados_tags = ["Población", "isoAlpha3", "Nombre del país", "Área en metros cuadrados", "Nombre del continente"]
    for encabezado_tag in encabezados_tags:
        th = html.new_tag("th", style="background-color: lightgray; padding: 10px; text-align: left;")
        th.string = encabezado_tag
        encabezados.append(th)
    fila_color=0
    # Agregar filas de datos de países ordenados por población
    for pais in poblacionMayorMenor:
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if fila_color % 2 == 0 else '#99C2FF'};")
        fila_color += 1
        tabla.append(fila)
        poblacion, isoAlpha3, nombre_pais, area, continente = pais[3], pais[1][3], pais[0], pais[7], pais[5][0]
        for dato in [poblacion, isoAlpha3, nombre_pais, area, continente]:
            td = html.new_tag("td", style="padding: 5px;")
            td.string = str(dato)
            fila.append(td)

    # Guardar el archivo HTML
    with open("informacion_por_poblacion.html", "w", encoding="utf-8") as file:
        file.write(str(html))

# Llama a la función para mostrar la información de países ordenada por población
poblacionMayorMenor(infoPaises)
# Función para mostrar información de países ordenada por área en metros cuadrados sin sorted
infoPaises = crearPaisesLista(paises)
def territorioPaises(infoPaises):
    """
    """
    # Implementar ordenación personalizada por población de mayor a menor
    info_paises_ordenados = []

    while infoPaises:
        max_pais = infoPaises[0]
        for pais in infoPaises:
            if pais[6] > max_pais[6]:
                max_pais = pais
        info_paises_ordenados.append(max_pais)
        infoPaises.remove(max_pais)

    # Crear el documento HTML
    html = BeautifulSoup("<html><head><title>Información de Países por Población</title></head><body></body></html>", "html.parser")

    # Agregar encabezado con estilo
    encabezado = html.new_tag("h1", style="color: blue; text-align: center;")
    encabezado.string = "Información de Países por Población"
    html.body.append(encabezado)

    # Agregar tabla de países con estilo
    tabla = html.new_tag("table", style="width: 100%; border-collapse: collapse;")
    html.body.append(tabla)

    # Agregar encabezados de tabla con estilo
    encabezados = html.new_tag("tr")
    tabla.append(encabezados)
    encabezados_tags = ["Área en metros cuadrados", "fipsCode", "Nombre del país", "Nombre del continente"]
    for encabezado_tag in encabezados_tags:
        th = html.new_tag("th", style="background-color: lightgray; padding: 10px; text-align: left;")
        th.string = encabezado_tag
        encabezados.append(th)
    fila_color=0
    # Agregar filas de datos de países ordenados por población
    for pais in info_paises_ordenados:
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if fila_color % 2 == 0 else '#99C2FF'};")
        fila_color += 1
        tabla.append(fila)
        area, fipsCode, nombrePais, continente = pais[6], pais[1][1], pais[0], pais[5][1]
        for dato in [area, fipsCode, nombrePais, continente]:
            td = html.new_tag("td", style="padding: 5px;")
            td.string = str(dato)
            fila.append(td)

    # Guardar el archivo HTML
    with open("informacion_por_poblacion.html", "w", encoding="utf-8") as file:
        file.write(str(html))

# Llama a la función para mostrar la información de países ordenada por área
territorioPaises(infoPaises)

