####################################################################
#Elaborado por: Alejandro Madrigal y Daniel Campos
#Fecha de creación: 03-10-2023 Hora: 1:00pm
#Fecha de finalización: 04-10-2023 Hora: 11:00pm
#Versión: 3.11.5
####################################################################
#Importación de librerias
from tareaProgramada1 import *
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from lxml import etree
from bs4 import BeautifulSoup
import requests as req
import sys
sys.setrecursionlimit(5000)
#Opción de crear estructura de datos
def opcionCrearEstructura():
    """
    Función: Crea la estructura de datos de los países. 
    Entradas: Archivo con los datos de los países.
    Salidas: Estructura de datos de los países.
    """
    df = pd.read_excel("paises.xlsx", sheet_name=0)
    paises = df.to_numpy()
    crearPaisesLista(paises)
    return menu()
#Opción de crear XML de los países
def opcionListaPaisesXML():
    """
    Función: Crea el XML de los países.
    Entradas: Estructura de datos de los países.
    Salidas: XML de los países.
    """
    infoPaises = crearPaisesLista(paises) 
    listaPaises(infoPaises)
    return menu()
#Opcion de menú de HTML
def opcionHTML():
    """
    Función: Muestra el menú de HTML.
    Entradas: Digito que se le solicita al usuario para indicar la prueba que desea realizar.
    Salidas: Resultado según lo solicitado.
    """
    return menuHTML()
#Menú principal
def menu():
    """
    Función: Muestra el menú al usuario. 
    Entradas: Dígito que se le solicita al usuario para indicar la prueba que desea realizar.
    Salidas: Resultado según lo solicitado.
    """
    print ("\n**************************\n")
    print ("Tarea programada 1")
    print ("Menú Principal")
    print("\n**************************\n")
    print("Instrucciones:")
    print("\nDebe crear primero la lista con la opción 1. \nLuego acceder a la opción 2.\nLuego acceder a la opción 3 para redirigirse a las sección de HTML.")
    print ("\n**************************\n")
    print ("1. Crear lista de países")
    print ("2. Crear XML de países (Te aparecerá una pestaña para abrir el XML, con tu navegador de preferencia)")
    print ("3. Crear HTMLs de países")
    print ("0. Salir del programa")
    print ("\n**************************\n")
    try:
        opcion = int(input("Escoja una opción: "))
        print ("\n**************************\n")
        if opcion>=0 or opcion<=5:
            if opcion == 1:
                print("Lista de paises creada con éxito.")
                return opcionCrearEstructura()
            elif opcion == 2:
                print("XML creado con éxito.")
                return opcionListaPaisesXML()
            elif opcion == 3:
                return opcionHTML() 
            elif opcion == 0:
                print("Gracias por usar nuestro programa. \n¡Esperamos que te haya servido la información que te brindamos!\n¡Vuelva pronto!")
                return ""
            else:
                print ("Opción inválida, digite una de las opciones")
                return menu()
    except ValueError:
        print("Opción inválida, debe ingresar sólo los números de las opciones.")
        return menu()
#Opciones HTML
#1. Listar países por continente
def opcionHtmlContinente():
    """
    Función: LLama a la función htmlContinente.
    Entradas: Información de los países.
    Salidas: HTML de los países por continente.
    """
    infoPaises = crearPaisesLista(paises)
    htmlContinente(infoPaises)
    return menuHTML()
#2. Listar países por población mayor a menor
def opcionPoblacionMayorMenorHTML():
    """
    Función: LLama a la función poblacionMayorMenor.
    Entradas: Información de los países.
    Salidas: HTML de los países por población mayor a menor.
    """
    infoPaises = crearPaisesLista(paises)
    poblacionMayorMenor(infoPaises)
    return menuHTML()
#3. Listar países por mayor o menor territorio
def opcionTerritorioPaisesHTML():
    """
    Función: Llama a la función territorioPaisesHTML.
    Entradas: Información de los países.
    Salidas: HTML de los países por mayor o menor territorio.
    """
    infoPaises = crearPaisesLista(paises)
    territorioPaisesHTML(infoPaises)
    return menuHTML()
#4. Listar países con zonas azules
def opcionmostrarZonasAzulesHTML():
    """
    Función: Llama a la función mostrarZonasAzulesHTML.
    Entradas: Información de los países.
    Salidas: HTML de los países con zonas azules.
    """
    infoPaises = crearPaisesLista(paises)
    mostrarZonasAzulesHTML(infoPaises)
    return menuHTML()
#5. Listar idiomas
def opcioncontarIdiomasHTML():
    """
    Función: Llama a la función contarIdiomasHTML.
    Entradas: Información de los países.
    Salidas: HTML de los idiomas.
    """
    infoPaises = crearPaisesLista(paises)
    contarIdiomasHTML(infoPaises)
    return menuHTML()
#6. Listar países por moneda.
def opcionmostrarPaisesMonedaHTML():
    """
    Función: Llama a la función mostrarPaisesMonedaHTML.
    Entradas: Información de los países.
    Salidas: HTML de los países por moneda.
    """
    infoPaises = crearPaisesLista(paises)
    mostrarPaisesMonedaHTML(infoPaises)
    return menuHTML()
#7. Códigos de un país.
def opcioncogidosPaisHTML():
    """
    Función: Llama a la función cogidosPaisHTML.
    Entradas: Información de los países.
    Salidas: HTML de los códigos de un país.
    """
    infoPaises = crearPaisesLista(paises)
    codigosPaisHTML(infoPaises)
    return menuHTML()
#8. Calcular población por idioma
def opicioncalcularHablantesPaisHTML():
    """
    Función: Llama a la función calcularHablantesPaisHTML.
    Entradas: Información de los países.
    Salidas: HTML de la población por idioma.
    """
    infoPaises = crearPaisesLista(paises)
    contarPersonasPorIdiomaHTML(infoPaises)
    return menuHTML()
#Menú HTML
def menuHTML():
    """
    Función: Muestra el menú al usuario. 
    Entradas: Dígito que se le solicita al usuario para indicar la prueba que desea realizar.
    Salidas: Resultado según lo solicitado.
    """
    print ("\n**************************\n")
    print ("Laboratorio de listas")
    print ("Menú HTML")
    print ("\n**************************\n")
    print ("1. HTML de países por continente")
    print ("2. HTML de países por población mayor a menor")
    print ("3. HTML de países por mayor a menor territorio")
    print ("4. HTML de países con zonas azules")
    print ("5. HTML de idiomas")
    print ("6. HTML de países por moneda")
    print ("7. HTML de códigos de un país")
    print ("8. HTML de población por idioma")
    print ("0. Salir del submenú")
    print ("\n**************************\n")
    try:
        opcion = int(input("Escoja una opción: "))
        print ("\n**************************\n")
        if opcion>=0 or opcion<=5:
            if opcion == 1:
                return opcionHtmlContinente()
            elif opcion == 2:
                return opcionPoblacionMayorMenorHTML()
            elif opcion == 3:
                return opcionTerritorioPaisesHTML()
            elif opcion == 4:
                return opcionmostrarZonasAzulesHTML()
            elif opcion == 5:
                return opcioncontarIdiomasHTML()
            elif opcion == 6:
                return opcionmostrarPaisesMonedaHTML()
            elif opcion == 7:
                return opcioncogidosPaisHTML()
            elif opcion == 8:
                return opicioncalcularHablantesPaisHTML()
            elif opcion == 0:
                print("¿Se te olvidó algo? ¡Tranquilo, te devolvemos al menú principal!\nSi no es así, presiona 0 para salir del programa.")
                return menu()
            else:
                print ("Opción inválida, digita una de las opciones")
                return menuHTML()
    except ValueError:
        print("Opción inválida, debe ingresar sólo los números de las opciones.")
        return menuHTML()
menu()