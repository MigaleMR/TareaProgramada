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
import sys
sys.setrecursionlimit(5000)
from lxml import etree
from bs4 import BeautifulSoup
import requests as req
import os
import re

def opcionCrearEstructura():
    """
    """
    df = pd.read_excel("D:\Estudios de Ale\Compu\GitHub\Tareas Programadas\TareaProgramada/paises.xlsx", sheet_name=0)
    paises = df.to_numpy()
    crearPaisesLista(paises)
    return menu() and infoPaises

def opcionListaPaisesXlm(): 
    """
    """
    return menu() and listaPaises(infoPaises)
    
def menu():
    """
    Funcionamiento: de manera repetitiva, muestra el menú al usuario. 
    Entradas:
        -opcion(int): dígito que se le solicita al usuario para indicar
        la prueba que desea realizar.
    Salidas:resultado según lo solicitado
    """
    print ("\n**************************\n")
    print ("Laboratorio de listas")
    print ("Menú Principal")
    print ("\n**************************\n")
    print ("1. Agregar convalecientes donadores del día")
    print ("2. Decodificar donador")
    print ("3. Listar donadores según registro de naturalizaciones")
    print ("4. Donadores totales del país")
    print ("5. Donadores no tipicos")
    print ("0. Salir del sistema")
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
                return 
            elif opcion == 4:
                return 
            elif opcion == 5:
                return 
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