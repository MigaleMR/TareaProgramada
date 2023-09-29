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
#informacion de la tabla de paises convertida a matriz
df = pd.read_excel("paises.xlsx", sheet_name=0)
paises = df.to_numpy()
infoPaises=[]
for pais in paises:
    countryCode = pais[0]
    countryName = pais[1]
    currencyCode = pais[2]
    population = pais[3]
    fipsCode = pais[4]
    isoNumeric = pais[5]
    capital = pais[6]
    continentName = pais[7]
    continentCode = pais[8]
    #se tuvo que cambiar NA por NRA porque NA se considera como un valor nulo y retorna "nan"
    areaInSqKm = pais[9]
    languages = pais[10]
    isoAlpha3 = pais[11]
    geonameId = pais[12]
    infoPais=[countryName,[countryCode,fipsCode,isoNumeric,isoAlpha3,geonameId],currencyCode,population,capital,[continentName,continentCode],areaInSqKm,languages]
    infoPaises.append(infoPais)   
#crear el archivo xml
import xml.etree.ElementTree as ET
root = ET.Element("paises")
for paisData in infoPaises:
    pais = ET.SubElement(root, "pais")
    nombre = ET.SubElement(pais, "nombre")
    nombre.text = paisData[0]
    codigo = ET.SubElement(pais, "codigo")
    codigo.text = paisData[1][0]
    fips = ET.SubElement(pais, "fips")
    fips.text = paisData[1][1]
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
tree.write("paises.xml")