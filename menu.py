####################################################################
#Elaborado por: Alejandro Madrigal y Daniel Campos
#Fecha de creación: 21-09-2023 Hora: 10:00pm
#Fecha de finalización:
#Versión: 3.11.5
####################################################################
#Importaci[o de librerias
from tareaProgramada1 import *
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from lxml import etree
from bs4 import BeautifulSoup
import requests as req
import os
import re
import sys
sys.setrecursionlimit(5000)

def opcionCrearEstructura():
    """
    Función: 
    Entradas:
    Salidas:
    """
    df = pd.read_excel("paises.xlsx", sheet_name=0)
    paises = df.to_numpy()
    crearPaisesLista(paises)
    return menu()

def opcionListaPaisesXlm():
    """
    Función: 
    Entradas:
    Salidas:
    """
    infoPaises = crearPaisesLista(paises) 
    listaPaises(infoPaises)
    return menu()

def opcionHTML():
    """
    Función: 
    Entradas:
    Salidas:
    """
    return menuHTML()
def menu():
    """
    Función: de manera repetitiva, muestra el menú al usuario. 
    Entradas: dígito que se le solicita al usuario para indicar la prueba que desea realizar.
    Salidas: resultado según lo solicitado
    """
    print ("\n**************************\n")
    print ("Laboratorio de listas")
    print ("Menú Principal")
    print("Debe crear primero la lista con la opción 1, luego acceder a la opción 2.\ny luego acceder a la opción 3 para redirigirse a las sección de HTML.")
    print ("\n**************************\n")
    print ("1. Crear lista de países")
    print ("2. Crear XML de países")
    print ("3. Crear HTMLs de países")
    print ("\n**************************\n")
    try:
        opcion = int(input("Escoja una opción: "))
        print ("\n**************************\n")
        if opcion>=0 or opcion<=5:
            if opcion == 1:
                return opcionCrearEstructura()
            elif opcion == 2:
                return opcionListaPaisesXlm()
            elif opcion == 3:
                return opcionHTML() 
            elif opcion == 0:
                print("Gracias por usar nuestro programa, ¡Vuelva pronto!")
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
    Función: 
    Entradas:
    Salidas:
    """
    infoPaises = crearPaisesLista(paises)
    htmlContinente(infoPaises)
    return menuHTML()
#2. Listar países por población mayor a menor
def opcionPoblacionMayorMenorHTML():
    """
    Función: 
    Entradas:
    Salidas:
    """
    infoPaises = crearPaisesLista(paises)
    poblacionMayorMenor(infoPaises)
    return menuHTML()
#3. Listar países por mayor o menor territorio
def opcionTerritorioPaisesHTML():
    """
    Función: 
    Entradas:
    Salidas:
    """
    infoPaises = crearPaisesLista(paises)
    territorioPaisesHTML(infoPaises)
    return menuHTML()
#4. Listar países con zonas azules
def opcionmostrarZonasAzulesHTML():
    """
    Función: 
    Entradas:
    Salidas:
    """
    infoPaises = crearPaisesLista(paises)
    mostrarZonasAzulesHTML(infoPaises)
    return menuHTML()
#5. Listar idiomas
def opcioncontarIdiomasHTML():
    """
    Función: 
    Entradas:
    Salidas:
    """
    infoPaises = crearPaisesLista(paises)
    contarIdiomasHTML(infoPaises)
    return menuHTML()
#6. Listar países por moneda
def opcionmostrarPaisesMonedaHTML():
    """
    Función: 
    Entradas:
    Salidas:
    """
    infoPaises = crearPaisesLista(paises)
    mostrarPaisesMonedaHTML(infoPaises)
    return menuHTML()
#7 Calcular población por idioma
def opicioncalcularHablantesXPaisHTML():
    """
    Función: 
    Entradas:
    Salidas:
    """
    infoPaises = crearPaisesLista(paises)
    calcularHablantesXPaisHTML(infoPaises)
    return menuHTML()
#Menú HTML
def menuHTML():
    """
    Funcionamiento: de manera repetitiva, muestra el menú al usuario. 
    Entradas: dígito que se le solicita al usuario para indicar la prueba que desea realizar.
    Salidas:resultado según lo solicitado
    """
    print ("\n**************************\n")
    print ("Laboratorio de listas")
    print ("Menú Principal")
    print ("\n**************************\n")
    print ("1. HTML de países por continente")
    print ("2. HTML de países por población mayor a menor")
    print ("3. HTML de países por mayor a menor territorio")
    print ("4. HTML de países con zonas azules")
    print ("5. HTML de idiomas")
    print ("6. HTML de países por moneda")
    print ("7. HTML de población por idioma")
    print ("0. Salir del sistema")
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
                return opicioncalcularHablantesXPaisHTML()
            elif opcion == 0:
                print("Gracias por donar su sangre, ahora fuiste tú, luego espero poder ser yo.")
                print("Salida del programa")
            else:
                print ("Opción inválida, digita una de las opciones")
                return menu()
    except ValueError:
        print("Opción inválida, debe ingresar sólo los números de las opciones.")
        return menu() 
menu()