import itertools
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import matplotlib.pyplot as plt
from random import randrange
import numpy as np
import openpyxl as pxl
import os
import zipfile
import atexit
import xlsxwriter
from vincent.colors import brews

class Equipo:
    # Agrego valores iniciales de los datos que me interesan de la pagina web como otros que quiera crear yo nuevos
    name = ""
    equiposQueHaGanado = []
    equiposQueHaPerdido = []
    equiposQueHaEmpatado = []
    golesEncontraUltimasJornadas = 0
    golesAfavorUltimasJornadas = 0
    maximosGoles = 0
    minimosGoles = 0
    maximosGolesEnContra = 0
    minimosGolesEnContra = 0
    mediaGolPorPartidoMarcados = 0
    mediaGolPorPartidoEnContra = 0
    puntosDeDebilidad = 0
    puntosDeFuerza = 0
    equiposQueHaEmpatadoNombre = []
    equiposQueHaGanadoNombre = []
    equiposQueHaPerdidoNombre = []

    def __init__(self, name, ganados=[], perdidos=[], empatados=[],
                 golesAfavorUltimasJornadas=0, golesEncontraUltimasJornadas=0, maximosGoles=0, minimosGoles=0,
                 maximosGolesEnContra=0, minimosGolesEnContra=0, mediaGolPorPartidoMarcados=0,
                 mediaGolPorPartidoEnContra=0):  # Llamo a los datos que me interan ya inicializados y les añado el valor que he dado en la entrada de la clase
        self.name = name
        self.setvalues(ganados, perdidos, empatados,
                       golesAfavorUltimasJornadas, golesEncontraUltimasJornadas, maximosGoles, minimosGoles,
                       maximosGolesEnContra, minimosGolesEnContra, mediaGolPorPartidoMarcados,
                       mediaGolPorPartidoEnContra)

    def setvalues(self,ganados=[], perdidos=[], empatados=[],
                  golesAfavorUltimasJornadas=0, golesEncontraUltimasJornadas=0, maximosGoles=0, minimosGoles=0,
                  maximosGolesEnContra=0, minimosGolesEnContra=0, mediaGolPorPartidoMarcados=0,
                  mediaGolPorPartidoEnContra=0):  # Llamo a los datos que me interan ya inicializados y les añado el valor que he dado en la entrada de la clase
        self.equiposQueHaGanado = ganados
        self.equiposQueHaPerdido = perdidos
        self.equiposQueHaEmpatado = empatados
        self.golesAfavorUltimasJornadas = golesAfavorUltimasJornadas
        self.golesEncontraUltimasJornadas = golesEncontraUltimasJornadas
        self.maximosGoles = maximosGoles
        self.minimosGoles = minimosGoles
        self.maximosGolesEnContra = maximosGolesEnContra
        self.minimosGolesEnContra = minimosGolesEnContra
        self.mediaGolPorPartidoMarcados = mediaGolPorPartidoMarcados
        self.mediaGolPorPartidoEnContra = mediaGolPorPartidoEnContra

    def transformData(self):
        self.equiposQueHaGanadoNombre = [tm.name for tm in self.equiposQueHaGanado]
        self.equiposQueHaPerdidoNombre = [tm.name for tm in self.equiposQueHaPerdido]
        self.equiposQueHaEmpatadoNombre = [tm.name for tm in self.equiposQueHaEmpatado]

    def getDataframe(self):  # de los valores que estoy trabajando, los meto en un dataframe para manejarlos mejor
        self.transformData()
        recopilacionequipo = [
            self.name,
            self.equiposQueHaGanadoNombre,
            self.equiposQueHaPerdidoNombre,
            self.equiposQueHaEmpatadoNombre,
            self.golesAfavorUltimasJornadas,
            self.golesEncontraUltimasJornadas,
            self.maximosGoles,
            self.minimosGoles,
            self.maximosGolesEnContra,
            self.minimosGolesEnContra,
            self.mediaGolPorPartidoMarcados,
            self.mediaGolPorPartidoEnContra,
            self.puntosDeFuerza,
            self.puntosDeDebilidad
        ]
        recopilacionImportanteEquipo = [
            self.name,
            self.golesAfavorUltimasJornadas,
            self.golesEncontraUltimasJornadas,
            self.maximosGoles,
            self.minimosGoles,
            self.maximosGolesEnContra,
            self.minimosGolesEnContra,
            self.mediaGolPorPartidoMarcados,
            self.mediaGolPorPartidoEnContra,
            self.puntosDeFuerza,
            self.puntosDeDebilidad
        ]
        recopilacionequipo = pd.DataFrame(recopilacionequipo).transpose()
        recopilacionImportanteEquipo = pd.DataFrame(recopilacionImportanteEquipo).transpose()

        recopilacionequipo.columns = [
            "Team",
            "Won vs",
            "Lost vs",
            "Draw vs",
            "G_Scored last_4",
            "G_Against last_4",
            "Max G_Scored last_4",
            "Min G_Scored last_4",
            "Max G_Against last_4",
            "Min G_Against last_4",
            "Averg G_Scored last_4",
            "Averg G_Against last_4",
            "Strength Points",
            "Weakness Points"
        ]
        recopilacionImportanteEquipo.columns = [
            "Team",
            "G_Scored last_4",
            "G_Against last_4",
            "Max G_Scored last_4",
            "Min G_Scored last_4",
            "Max G_Against last_4",
            "Min G_Against last_4",
            "Averg G_Scored last_4",
            "Averg G_Against last_4",
            "Strength Points",
            "Weakness Points"
        ]
        return recopilacionequipo, recopilacionImportanteEquipo

def getEquipo(teamName, listaDeEquipos):
    for b in listaDeEquipos:
        if b.name == teamName:
            return b
###################################################################################################################################################################

def getTeamsObjects(route):
    listOfTeams = []
    tableData = route.find('table', {'class': "styled__TableStyled-sc-43wy8s-1 iOBNZZ"})
    eachRowMatch = tableData.find_all('div', {'class': 'styled__MatchStyled-sc-2hkd8m-1 jVNhaC'})
    resultadosPartidos = []
    for row in eachRowMatch:
        match = {}
        results = row.find_all('p', {'class': 'styled__TextRegularStyled-sc-1raci4c-0 fYuQIM'})
        teams = row.find_all('p', {'class': 'styled__TextRegularStyled-sc-1raci4c-0 hvREvZ'})
        lenOfTeams = len(teams)
        for i in range(lenOfTeams):
            match[teams[i].contents[0]] =  results[i].contents[0]
            teamClass = Equipo(teams[i].contents[0])
            listOfTeams.append(teamClass)
        resultadosPartidos.append(match)
    return listOfTeams
###################################################################################################################################################################

def getPreviousJourneys(route, listOfTeams, itermax):
    #busco la jornada actual
    journeys = soupOfTeams.find('div', {'class': 'styled__SubHeaderCalendarGrid-sc-1engvts-8 iYpljZ'}).find('div', {'class': 'styled__DropdownContainer-d9k1bl-0 kmhQzc'})
    currentJourney = journeys.find('span').contents[0]
    #busco las jornadas
    eachjourney = journeys.find('ul', {'class': 'styled__ItemsList-d9k1bl-2 hkGQnA'}).find_all('a')
    lenJourneys = len(eachjourney)
    previousJourneys = []
    linkPreviousJourneys = []   #uso esto para buscar cada jornada
    for numday, day in enumerate(eachjourney):
        linkPreviousJourneys.append(day['href'])
        previousJourneys.append(day)
        if day.contents[0] == currentJourney:
            break

    enterPage = requests.get('https://www.laliga.com/' + linkPreviousJourneys[0])  # Get URL






###################################################################################################################################################################
route = requests.get('https://www.laliga.com/laliga-santander/resultados')  # Get URL
soupOfTeams = BeautifulSoup(route.text, 'html.parser')  # Use this format to read it

###################################################################################################################################################################

#For day BASE (obtener), -i to iter (4,5,6,7...) result efficiency
# Set inicial
listOfPrimera = getTeamsObjects(soupOfTeams)
itermax = 12
getPreviousJourneys(route, listOfPrimera, itermax)
###################################################################################################################################################################

#obtener modulo de partidos de X jornada:
# for i in listOfPrimera:
#     print(i.name)