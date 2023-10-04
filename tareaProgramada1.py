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
import sys
sys.setrecursionlimit(5000)
from lxml import etree
from bs4 import BeautifulSoup
import os
# se tuvo que cambiar NA porque retornaban valores sin informacion (nan)
df = pd.read_excel("D:\Estudios de Ale\Compu\GitHub\Tareas Programadas\TareaProgramada/paises.xlsx", sheet_name=0)
paises = df.to_numpy()
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
infoPaises = crearPaisesLista(paises) 
def listaPaises(infoPaises):
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
    continenteElegido = input("Ingrese el nombre del continente del cual desea obtener información (Europe, North America, Asia, Antartica, Africa, Oceania, South America ): ")##############CAMBIAR##############
    filtrarPaises = [pais for pais in infoPaises if pais[5][0] == continenteElegido]
    if not filtrarPaises:
        print(f"No se encontraron países en el continente {continenteElegido}.")
        return
    html = BeautifulSoup("<html><head><title>Información de Países</title></head><body></body></html>", "html.parser")
    encabezado = html.new_tag("h1", style="color: blue; text-align: center;")
    encabezado.string = f"Información de Países en el Continente {continenteElegido}"
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
    color = 0
    for pais in filtrarPaises:
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if color % 2 == 0 else '#99C2FF'};")
        color += 1
        tabla.append(fila)
        nombre, codigos, poblacion, capital, area = pais[0], pais[1], pais[3], pais[4], pais[6]
        for dato in [nombre, codigos[0], poblacion, capital, area]:
            td = html.new_tag("td", style="padding: 5px;")
            td.string = str(dato)
            fila.append(td)
    with open(f"informacion_{continenteElegido}.html", "w", encoding="utf-8") as file:
        file.write(str(html))

#b. ¿Cuántos viven?
def poblacionMayorMenor(infoPaises):
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
    encabezados_tags = ["Población", "isoAlpha3", "Nombre del país", "Área en metros cuadrados", "Nombre del continente"]
    for encabezado_tag in encabezados_tags:
        th = html.new_tag("th", style="background-color: lightgray; padding: 10px; text-align: left;")
        th.string = encabezado_tag
        encabezados.append(th)
    fila_color=0
    for pais in poblacionMayorMenor:
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if fila_color % 2 == 0 else '#99C2FF'};")
        fila_color += 1
        tabla.append(fila)
        poblacion, isoAlpha3, nombre_pais, area, continente = pais[3], pais[1][3], pais[0], pais[6], pais[5][0]
        for dato in [poblacion, isoAlpha3, nombre_pais, area, continente]:
            td = html.new_tag("td", style="padding: 5px;")
            td.string = str(dato)
            fila.append(td)
    with open("informacion_por_poblacion.html", "w", encoding="utf-8") as file:
        file.write(str(html))

#c. De grandes a pequeños.
def territorioPaisesHTML(infoPaises):
    """
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
    encabezados_tags = ["Área en metros cuadrados", "fipsCode", "Nombre del país", "Nombre del continente"]
    for encabezado_tag in encabezados_tags:
        th = html.new_tag("th", style="background-color: lightgray; padding: 10px; text-align: left;")
        th.string = encabezado_tag
        encabezados.append(th)
    fila_color=0
    for pais in info_paises_ordenados:
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if fila_color % 2 == 0 else '#99C2FF'};")
        fila_color += 1
        tabla.append(fila)
        area, fipsCode, nombrePais, continente = pais[6], pais[1][1], pais[0], pais[5][1]
        for dato in [area, fipsCode, nombrePais, continente]:
            td = html.new_tag("td", style="padding: 5px;")
            td.string = str(dato)
            fila.append(td)
    with open("informacion_metros_cuadrados.html", "w", encoding="utf-8") as file:
        file.write(str(html))

#d. Zonas azules.
def mostrarZonasAzulesHTML(infoPaises):
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
    encabezados_tags = ["geonameId", "Nombre del país", "currencyCode", "Idiomas", "Población", "Áreas en metro cuadrados"]
    for encabezado_tag in encabezados_tags:
        th = html.new_tag("th", style="background-color: lightgray; padding: 10px; text-align: left;")
        th.string = encabezado_tag
        encabezados.append(th)
    fila_color=0
    for pais in paisesAzules:
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if fila_color % 2 == 0 else '#99C2FF'};")
        fila_color += 1
        tabla.append(fila)
        geonameID, countryName, currencyCode, lenguage, population, areaInSqKm  = pais[1][4], pais[0], pais[2], pais[7], pais[3], pais[6]
        for dato in [geonameID, countryName, currencyCode, lenguage, population, areaInSqKm ]:
            td = html.new_tag("td", style="padding: 5px;")
            td.string = str(dato)
            fila.append(td)
    with open("paises_azules.html", "w", encoding="utf-8") as file:
        file.write(str(html))

#e. Países con el mismo idioma.
def contarIdiomasHTML(infoPaises):
    """
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
    encabezados_tags = ["Idioma", "Cantidad de Países", "Países", "Continentes"]
    for encabezado_tag in encabezados_tags:
        th = html.new_tag("th", style="background-color: lightgray; padding: 10px; text-align: left;")
        th.string = encabezado_tag
        encabezados.append(th)
    color = 0
    for i in range(len(idiomasUnicos)):
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if color % 2 == 0 else '#99C2FF'};")
        coloor += 1
        tabla.append(fila)
        idioma = idiomasUnicos[i]
        cantidad = cantidadPaises[i]
        td_idioma = html.new_tag("td", style="padding: 5px;")
        td_idioma.string = idioma
        fila.append(td_idioma)
        td_cantidad = html.new_tag("td", style="padding: 5px;")
        td_cantidad.string = str(cantidad)
        fila.append(td_cantidad)
        paises = paisesIdioma[i]
        td_paises = html.new_tag("td", style="padding: 5px;")
        td_paises.string = ", ".join(paises)
        fila.append(td_paises)
        continentes = idiomasContinente[i]
        td_continentes = html.new_tag("td", style="padding: 5px;")
        td_continentes.string = ", ".join(continentes)
        fila.append(td_continentes)
    with open("cantidad_paises_por_idioma.html", "w", encoding="utf-8") as file:
        file.write(str(html))

#f. Pago con la misma moneda.
def mostrarPaisesMonedaHTML(infoPaises):
    monedas = [pais[2] for pais in infoPaises if pais[2]]
    monedas_unicas = list(set(monedas))
    print("Monedas disponibles:")
    for i, moneda in enumerate(monedas_unicas, start=1):
        print(f"{i}. {moneda}")
    seleccion = int(input("Seleccione una moneda (ingrese el número): ")) - 1
    moneda_seleccionada = monedas_unicas[seleccion]
    paises_con_moneda = [pais for pais in infoPaises if pais[2] == moneda_seleccionada]
    html = BeautifulSoup("<html><head><title>Países por Moneda</title></head><body></body></html>", "html.parser")
    encabezado = html.new_tag("h1", style="color: blue; text-align: center;")
    encabezado.string = f"Países que utilizan la moneda {moneda_seleccionada}"
    html.body.append(encabezado)
    contador = 0
    for pais in paises_con_moneda:
        contador += 1
    contador_html = html.new_tag("p")
    contador_html.string = f"Cantidad de países que utilizan esta moneda: {contador}"
    html.body.append(contador_html)
    tabla = html.new_tag("table", style="width: 100%; border-collapse: collapse;")
    html.body.append(tabla)
    encabezados = html.new_tag("tr")
    tabla.append(encabezados)
    encabezados_tags = ["Nombre del país", "Código", "Población", "Capital", "Área"]
    for encabezado_tag in encabezados_tags:
        th = html.new_tag("th", style="background-color: lightgray; padding: 10px; text-align: left;")
        th.string = encabezado_tag
        encabezados.append(th)
    paises_con_moneda.sort(key=lambda x: x[0])
    fila_color = 0
    for pais in paises_con_moneda:
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if fila_color % 2 == 0 else '#99C2FF'};")
        fila_color += 1
        tabla.append(fila)
        nombre, codigos, poblacion, capital, area = pais[0], pais[1], pais[3], pais[4], pais[6]
        for dato in [nombre, codigos[0], poblacion, capital, area]:
            td = html.new_tag("td", style="padding: 5px;")
            td.string = str(dato)
            fila.append(td)
    with open(f"paises_{moneda_seleccionada}.html", "w", encoding="utf-8") as file:
        file.write(str(html))
    print(f"Archivo HTML creado con los países que utilizan la moneda {moneda_seleccionada} y el contador de países.")

#g. Códigos de un determinado país.
def informacionPaisyContinenteHTML(infoPaises):
    """
    """
    continentes_unicos = list(set([pais[5][0] for pais in infoPaises]))
    print("Continentes Disponibles:")
    for i, continente in enumerate(continentes_unicos, start=1):
        print(f"{i}. {continente}")
    seleccion_continente = int(input("Seleccione un continente (ingrese el número): ")) - 1
    continente_seleccionado = continentes_unicos[seleccion_continente]
    paises_continente = [pais for pais in infoPaises if pais[5][0] == continente_seleccionado]
    print(f"Países en el continente {continente_seleccionado}:")
    for i, pais in enumerate(paises_continente, start=1):
        print(f"{i}. {pais[0]}")
    seleccion_pais = int(input("Seleccione un país dentro del continente (ingrese el número): ")) - 1
    pais_seleccionado = paises_continente[seleccion_pais]
    html = BeautifulSoup("<html><head><title>Códigos del País</title></head><body></body></html>", "html.parser")
    encabezado = html.new_tag("h1", style="color: blue; text-align: center;")
    encabezado.string = "Detalles del País"
    html.body.append(encabezado)
    detalles_lista = html.new_tag("ul")
    html.body.append(detalles_lista)
    detalles = ["Nombre del continente: " + str(pais_seleccionado[5][0]),"Nombre del país: " + str(pais_seleccionado[0]),"countryCode: " + str(pais_seleccionado[1][0]),"fipsCode: " + str(pais_seleccionado[1][1]),"isoNumeric: " + str(pais_seleccionado[1][2]),"isoAlpha3: " + str(pais_seleccionado[1][3]),"geonameId: " + str(pais_seleccionado[1][4])]
    fila_color = 0  
    for detalle in detalles:
        detalle_tag = html.new_tag("li", style=f"background-color: {'#CCE6FF' if fila_color % 2 == 0 else '#99C2FF'};")
        fila_color += 1
        detalle_tag.string = detalle
        detalles_lista.append(detalle_tag)
    with open("detalles_pais.html", "w", encoding="utf-8") as file:
        file.write(str(html))
    print("Archivo HTML creado con los detalles del país seleccionado.")

#h. Hablantes por idioma
def calcularHablantesXPaisHTML(infoPaises):
    idiomas_unicos = []
    hablantes_por_idioma = []
    for pais in infoPaises:
        if len(pais) > 10 and pais[10] is not None:
            idiomas = pais[10].split(",")
            poblacion = pais[3]
            for idioma in idiomas:
                idioma_principal = idioma.strip().split("-")[0]
                if idioma_principal not in idiomas_unicos:
                    idiomas_unicos.append(idioma_principal)
                    hablantes_por_idioma.append(poblacion)
                else:
                    index = idiomas_unicos.index(idioma_principal)
                    hablantes_por_idioma[index] += poblacion
    html = BeautifulSoup("<html><head><title>Hablantes por Idioma</title></head><body></body></html>", "html.parser")
    encabezado = html.new_tag("h1", style="color: blue; text-align: center;")
    encabezado.string = "Hablantes por Idioma"
    html.body.append(encabezado)
    tabla = html.new_tag("table", style="width: 100%; border-collapse: collapse;")
    html.body.append(tabla)
    encabezados = html.new_tag("tr")
    tabla.append(encabezados)
    encabezados_tags = ["Idioma", "Cantidad de Hablantes"]
    for encabezado_tag in encabezados_tags:
        th = html.new_tag("th", style="background-color: lightgray; padding: 10px; text-align: left;")
        th.string = encabezado_tag
        encabezados.append(th)
    fila_color = 0
    for idioma, hablantes in zip(idiomas_unicos, hablantes_por_idioma):
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if fila_color % 2 == 0 else '#99C2FF'};")
        fila_color += 1
        tabla.append(fila)
        td_idioma = html.new_tag("td", style="padding: 5px;")
        td_idioma.string = idioma
        fila.append(td_idioma)
        td_hablantes = html.new_tag("td", style="padding: 5px;")
        td_hablantes.string = f"{hablantes:,}"
        fila.append(td_hablantes)
    with open("hablantes_por_idioma.html", "w", encoding="utf-8") as file:
        file.write(str(html))
    print("Archivo HTML creado con los hablantes por idioma.")