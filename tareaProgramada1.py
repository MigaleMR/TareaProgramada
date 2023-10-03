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
infoPaises = crearPaisesLista(paises)
listaPaises(infoPaises)

#archivos html
def htmlContinente(infoPaises):
    continenteElegido = input("Ingrese el nombre del continente del cual desea obtener información (Europe, North America, Asia, Antartica, Africa, Oceania ): ")##############CAMBIAR##############
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
infoPaises = crearPaisesLista(paises)
htmlContinente(infoPaises)

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
poblacionMayorMenor(infoPaises)
infoPaises = crearPaisesLista(paises)

def territorioPaises(infoPaises):
    """
    """
    info_paises_ordenados = []
    while infoPaises:
        max_pais = infoPaises[0]
        for pais in infoPaises:
            if pais[6] > max_pais[6]:
                max_pais = pais
        info_paises_ordenados.append(max_pais)
        infoPaises.remove(max_pais)
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
territorioPaises(infoPaises)

infoPaises = crearPaisesLista(paises)
def mostrar_paises_con_zonas_azules(infoPaises):
    paises_con_zonas_azules = ["Costa Rica", "Greece", "Italy", "Japan", "United States"]
    paises_azules = [pais for pais in infoPaises if pais[0] in paises_con_zonas_azules]
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
    for pais in paises_azules:
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
mostrar_paises_con_zonas_azules(infoPaises)

def contar_paises_por_idioma(info_paises):
    """
    """
    idiomas_unicos = []
    cantidad_paises = []
    paises_por_idioma = []
    continentes_por_idioma = []
    def obtener_idioma_principal(codigo_idioma):
        return codigo_idioma.split("-")[0]
    for pais in info_paises:
        idiomas = pais[7].split(",")
        for idioma in idiomas:
            idioma = obtener_idioma_principal(idioma.strip())
            if idioma not in idiomas_unicos:
                idiomas_unicos.append(idioma)
                cantidad_paises.append(1)
                paises_por_idioma.append([pais[0]])
                continentes_por_idioma.append([pais[5][0]])
            else:
                index = idiomas_unicos.index(idioma)
                cantidad_paises[index] += 1
                paises_por_idioma[index].append(pais[0])
                if pais[5][0] not in continentes_por_idioma[index]:
                    continentes_por_idioma[index].append(pais[5][0])
    from bs4 import BeautifulSoup
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
    fila_color = 0
    for i in range(len(idiomas_unicos)):
        fila = html.new_tag("tr", style=f"background-color: {'#CCE6FF' if fila_color % 2 == 0 else '#99C2FF'};")
        fila_color += 1
        tabla.append(fila)
        idioma = idiomas_unicos[i]
        cantidad = cantidad_paises[i]
        td_idioma = html.new_tag("td", style="padding: 5px;")
        td_idioma.string = idioma
        fila.append(td_idioma)
        td_cantidad = html.new_tag("td", style="padding: 5px;")
        td_cantidad.string = str(cantidad)
        fila.append(td_cantidad)
        paises = paises_por_idioma[i]
        td_paises = html.new_tag("td", style="padding: 5px;")
        td_paises.string = ", ".join(paises)
        fila.append(td_paises)
        continentes = continentes_por_idioma[i]
        td_continentes = html.new_tag("td", style="padding: 5px;")
        td_continentes.string = ", ".join(continentes)
        fila.append(td_continentes)
    with open("cantidad_paises_por_idioma.html", "w", encoding="utf-8") as file:
        file.write(str(html))
contar_paises_por_idioma(infoPaises)

def mostrar_informacion_por_continente_y_pais(infoPaises):
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
    for detalle in detalles:
        detalle_tag = html.new_tag("li")
        detalle_tag.string = detalle
        detalles_lista.append(detalle_tag)
    with open("detalles_pais.html", "w", encoding="utf-8") as file:
        file.write(str(html))
    print("Archivo HTML creado con los detalles del país seleccionado.")
mostrar_informacion_por_continente_y_pais(infoPaises)

def calcular_hablantes_por_idioma(infoPaises):
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
    for idioma, hablantes in zip(idiomas_unicos, hablantes_por_idioma):
        fila = html.new_tag("tr")
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
calcular_hablantes_por_idioma(infoPaises)