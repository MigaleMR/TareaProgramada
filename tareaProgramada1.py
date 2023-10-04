####################################################################
#Elaborado por: Alejandro Madrigal y Daniel Campos
#Fecha de creación: 21-09-2023 Hora: 10:00pm
#Fecha de finalización:
#Versión: 3.11.5
####################################################################
#importacion de librerias
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from lxml import etree
from bs4 import BeautifulSoup
import os
import sys
sys.setrecursionlimit(5000)
# se tuvo que cambiar NA porque retornaban valores sin informacion (nan)
df = pd.read_excel("paises.xlsx", sheet_name=0)
paises = df.to_numpy()
def crearPaisesLista(paises):
    """
    Función: 
    Entradas:
    Salidas:
    """
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
infoPaises = crearPaisesLista(paises) 
def listaPaises(infoPaises):
    """
    Función: 
    Entradas:
    Salidas:
    """
    root = ET.Element("paises")
    tree = ET.ElementTree(root)
    for paisData in infoPaises:
        pais = ET.SubElement(root, "pais")
        nombre = ET.SubElement(pais, "nombre")
        nombre.text = paisData[0]
        codigo = ET.SubElement(pais, "codigo")
        codigo.text = paisData[1][0] if paisData[1][0] else ""
        fips = ET.SubElement(pais, "fips")
        fips.text = str(paisData[1][1]) if paisData[1][1] else ""
        iso = ET.SubElement(pais, "iso")
        iso.text = str(paisData[1][2]) if paisData[1][2] else ""
        isoAlpha = ET.SubElement(pais, "isoAlpha")
        isoAlpha.text = paisData[1][3] if paisData[1][3] else ""
        geoname = ET.SubElement(pais, "geoname")
        geoname.text = str(paisData[1][4]) if paisData[1][4] else ""
        moneda = ET.SubElement(pais, "moneda")
        moneda.text = paisData[2] if paisData[2] else ""
        poblacion = ET.SubElement(pais, "poblacion")
        poblacion.text = str(paisData[3]) if paisData[3] else ""
        capital = ET.SubElement(pais, "capital")
        capital.text = paisData[4] if paisData[4] else ""
        continente = ET.SubElement(pais, "continente")
        continente.text = paisData[5][0] if paisData[5][0] else ""
        continenteCodigo = ET.SubElement(pais, "continenteCodigo")
        continenteCodigo.text = paisData[5][1] if paisData[5][1] else ""
        area = ET.SubElement(pais, "area")
        area.text = str(paisData[6]) if paisData[6] else ""
        idiomas = ET.SubElement(pais, "idiomas")
        idiomas.text = paisData[7] if paisData[7] else ""
    tree.write("paises.xml", encoding="utf-8", xml_declaration=True)

#a. Países por continentes.
def htmlContinente(infoPaises):
    """
    Función: 
    Entradas:
    Salidas:
    """
    continenteElegido = input("Ingrese el nombre del continente del cual desea obtener información (Europe, North America, Asia, Antartica, Africa, Oceania, South America ): ")##############CAMBIAR##############
    filtrarPaises = [pais for pais in infoPaises if pais[5][0] == continenteElegido]
    if not filtrarPaises:
        print("No se encontraron países en el continente",continenteElegido)
        return
    html = BeautifulSoup("<html><head><title>Información de Países</title></head><body></body></html>", "html.parser")
    encabezado = html.new_tag("h1", style="color: blue; text-align: center;")
    encabezado.string = "Información de Países en el Continente",continenteElegido
    html.body.append(encabezado)
    tabla = html.new_tag("table", style="width: 100%; border-collapse: collapse;")
    html.body.append(tabla)
    encabezados = html.new_tag("tr")
    tabla.append(encabezados)
    tags = ["Nombre", "Código", "Población", "Capital", "Área"]
    for tags in  tags:
        th = html.new_tag("th", style="background-color: lightgray; padding: 10px; text-align: left;")
        th.string =  tags
        encabezados.append(th)
    colorFila = 0
    for pais in filtrarPaises:
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if colorFila % 2 == 0 else '#99C2FF'};")
        colorFila += 1
        tabla.append(fila)
        nombre, codigos, poblacion, capital, area = pais[0], pais[1], pais[3], pais[4], pais[6]
        for dato in [nombre, codigos[0], poblacion, capital, area]:
            td = html.new_tag("td", style="padding: 5px;")
            td.string = str(dato)
            fila.append(td)
    with open(f"Informacion{continenteElegido}.html", "w", encoding="utf-8") as file:
        file.write(str(html))

#b. ¿Cuántos viven?
def poblacionMayorMenor(infoPaises):
    """
    Función: 
    Entradas:
    Salidas:
    """
    poblacionMayorMenor= []
    while infoPaises:
        maximo = infoPaises[0]
        for pais in infoPaises:
            if pais[3] > maximo[3]:
                maximo = pais
        poblacionMayorMenor.append(maximo)
        infoPaises.remove(maximo)
    html = BeautifulSoup("<html><head><title>Información de Países por Población</title></head><body></body></html>", "html.parser")
    encabezado = html.new_tag("h1", style="color: blue; text-align: center;")
    encabezado.string = "Información de Países por Población"
    html.body.append(encabezado)
    tabla = html.new_tag("table", style="width: 100%; border-collapse: collapse;")
    html.body.append(tabla)
    encabezados = html.new_tag("tr")
    tabla.append(encabezados)
    nombreEncabezados = ["Población", "isoAlpha3", "Nombre del país", "Área en metros cuadrados", "Nombre del continente"]
    for nombreEncabezado in nombreEncabezados:
        th = html.new_tag("th", style="background-color: lightgray; padding: 10px; text-align: left;")
        th.string = nombreEncabezado
        encabezados.append(th)
    colorFila=0
    for pais in poblacionMayorMenor:
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if colorFila % 2 == 0 else '#99C2FF'};")
        colorFila += 1
        tabla.append(fila)
        poblacion, isoAlpha3, nombrePais, area, continente = pais[3], pais[1][3], pais[0], pais[6], pais[5][0]
        for dato in [poblacion, isoAlpha3, nombrePais, area, continente]:
            td = html.new_tag("td", style="padding: 5px;")
            td.string = str(dato)
            fila.append(td)
    with open("¿Cuántos viven?.html", "w", encoding="utf-8") as file:
        file.write(str(html))

#c. De grandes a pequeños.
def territorioPaisesHTML(infoPaises):
    """
    Función: 
    Entradas:
    Salidas:
    """
    paisesOrdenados= []
    while infoPaises:
        paisMayor = infoPaises[0]
        for pais in infoPaises:
            if pais[6] > paisMayor[6]:
                paisMayor = pais
        paisesOrdenados.append(paisMayor)
        infoPaises.remove(paisMayor)
    html = BeautifulSoup("<html><head><title>Información de países por territorio</title></head><body></body></html>", "html.parser")
    encabezado = html.new_tag("h1", style="color: blue; text-align: center;")
    encabezado.string = "Información de Países por Población"
    html.body.append(encabezado)
    tabla = html.new_tag("table", style="width: 100%; border-collapse: collapse;")
    html.body.append(tabla)
    encabezados = html.new_tag("tr")
    tabla.append(encabezados)
    nombreEncabezados = ["Área en metros cuadrados", "fipsCode", "Nombre del país", "Nombre del continente"]
    for nombreEncabezado in nombreEncabezados:
        th = html.new_tag("th", style="background-color: lightgray; padding: 10px; text-align: left;")
        th.string = nombreEncabezado
        encabezados.append(th)
    colorFila=0
    for pais in paisesOrdenados:
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if colorFila % 2 == 0 else '#99C2FF'};")
        colorFila += 1
        tabla.append(fila)
        area, fipsCode, nombrePais, continente = pais[6], pais[1][1], pais[0], pais[5][1]
        for dato in [area, fipsCode, nombrePais, continente]:
            td = html.new_tag("td", style="padding: 5px;")
            td.string = str(dato)
            fila.append(td)
    with open("De grandes a pequeños.html", "w", encoding="utf-8") as file:
        file.write(str(html))

#d. Zonas azules.
def mostrarZonasAzulesHTML(infoPaises):
    """
    Función: 
    Entradas:
    Salidas:
    """
    paisesZonasAzules= ["Costa Rica", "Greece", "Italy", "Japan", "United States"]
    paisesAzules = [pais for pais in infoPaises if pais[0] in paisesZonasAzules]
    html = BeautifulSoup("<html><head><title>Países con zonas azules</title></head><body></body></html>", "html.parser")
    encabezado = html.new_tag("h1", style="color: blue; text-align: center;")
    encabezado.string = "Información de Países por Población"
    html.body.append(encabezado)
    tabla = html.new_tag("table", style="width: 100%; border-collapse: collapse;")
    html.body.append(tabla)
    encabezados = html.new_tag("tr")
    tabla.append(encabezados)
    nombreEncabezados = ["geonameId", "Nombre del país", "currencyCode", "Idiomas", "Población", "Áreas en metro cuadrados"]
    for nombreEncabezado in nombreEncabezados:
        th = html.new_tag("th", style="background-color: lightgray; padding: 10px; text-align: left;")
        th.string = nombreEncabezado
        encabezados.append(th)
    colorFila=0
    for pais in paisesAzules:
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if colorFila % 2 == 0 else '#99C2FF'};")
        colorFila += 1
        tabla.append(fila)
        geonameID, countryName, currencyCode, lenguage, population, areaInSqKm  = pais[1][4], pais[0], pais[2], pais[7], pais[3], pais[6]
        for dato in [geonameID, countryName, currencyCode, lenguage, population, areaInSqKm ]:
            td = html.new_tag("td", style="padding: 5px;")
            td.string = str(dato)
            fila.append(td)
    with open("Zonas azules.html", "w", encoding="utf-8") as file:
        file.write(str(html))

#e. Países con el mismo idioma.
def contarIdiomasHTML(infoPaises):
    """
    Función: 
    Entradas:
    Salidas:
    """
    idiomasUnicos = []
    cantidadPaises = []
    paisesIdioma = []
    idiomasContinente = []
    def idiomaPrincipal(codigoIdioma):
        return codigoIdioma.split("-")[0]
    for pais in infoPaises:
        idiomas = pais[7].split(",")
        for idioma in idiomas:
            idioma = idiomaPrincipal(idioma.strip())
            if idioma not in idiomasUnicos:
                idiomasUnicos.append(idioma)
                cantidadPaises.append(1)
                paisesIdioma.append([pais[0]])
                idiomasContinente.append([pais[5][0]])
            else:
                index = idiomasUnicos.index(idioma)
                cantidadPaises[index] += 1
                paisesIdioma[index].append(pais[0])
                if pais[5][0] not in idiomasContinente[index]:
                    idiomasContinente[index].append(pais[5][0])
    html = BeautifulSoup("<html><head><title>Cantidad de Países por Idioma</title></head><body></body></html>", "html.parser")
    encabezado = html.new_tag("h1", style="color: blue; text-align: center;")
    encabezado.string = "Cantidad de Países por Idioma"
    html.body.append(encabezado)
    tabla = html.new_tag("table", style="width: 100%; border-collapse: collapse;")
    html.body.append(tabla)
    encabezados = html.new_tag("tr")
    tabla.append(encabezados)
    nombreEncabezados = ["Idioma", "Cantidad de Países", "Países", "Continentes"]
    for nombreEncabezado in nombreEncabezados:
        th = html.new_tag("th", style="background-color: lightgray; padding: 10px; text-align: left;")
        th.string = nombreEncabezado
        encabezados.append(th)
    color = 0
    for i in range(len(idiomasUnicos)):
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if color % 2 == 0 else '#99C2FF'};")
        coloor += 1
        tabla.append(fila)
        idioma = idiomasUnicos[i]
        cantidad = cantidadPaises[i]
        tdIdioma = html.new_tag("td", style="padding: 5px;")
        tdIdioma.string = idioma
        fila.append(tdIdioma)
        tdCantidad = html.new_tag("td", style="padding: 5px;")
        tdCantidad.string = str(cantidad)
        fila.append(tdCantidad)
        paises = paisesIdioma[i]
        tdPaises = html.new_tag("td", style="padding: 5px;")
        tdPaises.string = ", ".join(paises)
        fila.append(tdPaises)
        continentes = idiomasContinente[i]
        tdContinentes = html.new_tag("td", style="padding: 5px;")
        tdContinentes.string = ", ".join(continentes)
        fila.append(tdContinentes)
    with open("Países con el mismo idioma.html", "w", encoding="utf-8") as file:
        file.write(str(html))

#f. Pago con la misma moneda.
def mostrarPaisesMonedaHTML(infoPaises):
    """
    Función: 
    Entradas:
    Salidas:
    """
    monedas = [pais[2] for pais in infoPaises if pais[2]]
    unicaMoneda = list(set(monedas))
    print("Monedas disponibles:")
    for i, moneda in enumerate(unicaMoneda, start=1):
        print(f"{i}. {moneda}")
    seleccion = int(input("Seleccione una moneda (ingrese el número): ")) - 1
    seleccionMoneda = unicaMoneda[seleccion]
    monedaPaises = [pais for pais in infoPaises if pais[2] == seleccionMoneda]
    html = BeautifulSoup("<html><head><title>Países por Moneda</title></head><body></body></html>", "html.parser")
    encabezado = html.new_tag("h1", style="color: blue; text-align: center;")
    encabezado.string = "Países que utilizan la moneda",seleccionMoneda
    html.body.append(encabezado)
    contador = 0
    for pais in monedaPaises:
        contador += 1
    contadorHTML= html.new_tag("p")
    contadorHTML.string = "Cantidad de países que utilizan esta moneda:",contador
    html.body.append(contadorHTML)
    tabla = html.new_tag("table", style="width: 100%; border-collapse: collapse;")
    html.body.append(tabla)
    encabezados = html.new_tag("tr")
    tabla.append(encabezados)
    nombreEncabezados = ["Nombre del país", "Código", "Población", "Capital", "Área"]
    for nombreEncabezado in nombreEncabezados:
        th = html.new_tag("th", style="background-color: lightgray; padding: 10px; text-align: left;")
        th.string = nombreEncabezado
        encabezados.append(th)
    monedaPaises.sort(key=lambda x: x[0])
    colorFila = 0
    for pais in monedaPaises:
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if colorFila % 2 == 0 else '#99C2FF'};")
        colorFila += 1
        tabla.append(fila)
        nombre, codigos, poblacion, capital, area = pais[0], pais[1], pais[3], pais[4], pais[6]
        for dato in [nombre, codigos[0], poblacion, capital, area]:
            td = html.new_tag("td", style="padding: 5px;")
            td.string = str(dato)
            fila.append(td)
    with open(f"paises{seleccionMoneda}.html", "w", encoding="utf-8") as file:
        file.write(str(html))
    print("Archivo HTML creado con los países que utilizan la moneda",seleccionMoneda,"y el contador de países.")

#g. Códigos de un determinado país.
def cogidosPaisHTML(infoPaises):
    """
    Función: 
    Entradas:
    Salidas:
    """
    continentes = list(set([pais[5][0] for pais in infoPaises]))
    print("Continentes Disponibles:")
    for i, continente in enumerate(continentes, start=1):
        print(f"{i}. {continente}")
    seleccionContinente = int(input("Seleccione un continente (ingrese el número): ")) - 1
    continenteSeleccionado = continentes[seleccionContinente]
    paises = [pais for pais in infoPaises if pais[5][0] == continenteSeleccionado]
    print("Países en el continente:",continenteSeleccionado)
    for i, pais in enumerate(paises, start=1):
        print(f"{i}. {pais[0]}")
    seleccionPais = int(input("Seleccione un país dentro del continente (ingrese el número): ")) - 1
    paisSeleccionado = paises[seleccionPais]
    html = BeautifulSoup("<html><head><title>Códigos del País</title></head><body></body></html>", "html.parser")
    encabezado = html.new_tag("h1", style="color: blue; text-align: center;")
    encabezado.string = "Detalles del País"
    html.body.append(encabezado)
    listaDetalles = html.new_tag("ul")
    html.body.append(listaDetalles)
    detalles = ["Nombre del continente: " + str(paisSeleccionado[5][0]),"Nombre del país: " + str(paisSeleccionado[0]),"countryCode: " + str(paisSeleccionado[1][0]),"fipsCode: " + str(paisSeleccionado[1][1]),"isoNumeric: " + str(paisSeleccionado[1][2]),"isoAlpha3: " + str(paisSeleccionado[1][3]),"geonameId: " + str(paisSeleccionado[1][4])]
    colorFila = 0  
    for detalle in detalles:
        detalle = html.new_tag("li", style=f"background-color: {'#CCE6FF' if colorFila % 2 == 0 else '#99C2FF'};")
        colorFila += 1
        detalle.string = detalle
        listaDetalles.append(detalle)
    with open("Códigos de un determinado país.html", "w", encoding="utf-8") as file:
        file.write(str(html))
    print("Archivo HTML creado con los detalles del país seleccionado.")

#h. Hablantes por idioma
def calcularHablantesXPaisHTML(infoPaises):
    """
    Función: 
    Entradas:
    Salidas:
    """
    unicoIdioma = []
    hablantesIdiomas = []
    for pais in infoPaises:
        if len(pais) > 10 and pais[10] is not None:
            idiomas = pais[10].split(",")
            poblacion = pais[3]
            for idioma in idiomas:
                idiomaPrincipal = idioma.strip().split("-")[0]
                if idiomaPrincipal not in unicoIdioma:
                    unicoIdioma.append(idiomaPrincipal)
                    hablantesIdiomas.append(poblacion)
                else:
                    index = unicoIdioma.index(idiomaPrincipal)
                    hablantesIdiomas[index] += poblacion
    html = BeautifulSoup("<html><head><title>Hablantes por Idioma</title></head><body></body></html>", "html.parser")
    encabezado = html.new_tag("h1", style="color: blue; text-align: center;")
    encabezado.string = "Hablantes por Idioma"
    html.body.append(encabezado)
    tabla = html.new_tag("table", style="width: 100%; border-collapse: collapse;")
    html.body.append(tabla)
    encabezados = html.new_tag("tr")
    tabla.append(encabezados)
    nombreEncabezados = ["Idioma", "Cantidad de Hablantes"]
    for nombreEncabezado in nombreEncabezados:
        th = html.new_tag("th", style="background-color: lightgray; padding: 10px; text-align: left;")
        th.string = nombreEncabezado
        encabezados.append(th)
    colorFila = 0
    for idioma, hablantes in zip(unicoIdioma, hablantesIdiomas):
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if colorFila % 2 == 0 else '#99C2FF'};")
        colorFila += 1
        tabla.append(fila)
        tdIdioma = html.new_tag("td", style="padding: 5px;")
        tdIdioma.string = idioma
        fila.append(tdIdioma)
        tdHablantes = html.new_tag("td", style="padding: 5px;")
        tdHablantes.string = f"{hablantes:,}"
        fila.append(tdHablantes)
    with open("Hablantes por idioma.html", "w", encoding="utf-8") as file:
        file.write(str(html))
    print("Archivo HTML creado con los hablantes por idioma.")