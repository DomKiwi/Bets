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
    columnaPosiciones = 0
    puntos = 0
    partidos = 0
    wins = 0
    loses = 0
    draws = 0
    afavor = 0
    encontra = 0
    equiposQueHaGanado = []
    equiposQueHaPerdido = []
    equiposQueHaEmpatado = []
    puntosGanados = 0
    puntosPerdidos = 0
    puntosEmpatados = 0
    golesEncontraUltimasJornadas = 0
    golesAfavorUltimasJornadas = 0
    maximosGoles = 0
    minimosGoles = 0
    maximosGolesEnContra = 0
    minimosGolesEnContra = 0
    mediaGolPorPartidoMarcados = 0
    mediaGolPorPartidoEnContra = 0
    # puntosDeFuerza = len(equiposQueHaGanado)
    puntosDeDebilidad = 0
    puntosDeFuerza = 0
    equiposQueHaEmpatadoNombre = []
    equiposQueHaGanadoNombre = []
    equiposQueHaPerdidoNombre = []

    def __init__(self, name, columnasPosiciones=0, puntos=0, partidos=0, wins=0,
                 draws=0, loses=0, afavor=0, encontra=0, ganados=[], perdidos=[], empatados=[],
                 golesAfavorUltimasJornadas=0, golesEncontraUltimasJornadas=0, maximosGoles=0, minimosGoles=0,
                 maximosGolesEnContra=0, minimosGolesEnContra=0, mediaGolPorPartidoMarcados=0,
                 mediaGolPorPartidoEnContra=0):  # Llamo a los datos que me interan ya inicializados y les añado el valor que he dado en la entrada de la clase
        self.name = name
        self.setvalues(columnasPosiciones, puntos, partidos, wins,
                       draws, loses, afavor, encontra, ganados, perdidos, empatados,
                       golesAfavorUltimasJornadas, golesEncontraUltimasJornadas, maximosGoles, minimosGoles,
                       maximosGolesEnContra, minimosGolesEnContra, mediaGolPorPartidoMarcados,
                       mediaGolPorPartidoEnContra)

    def setvalues(self, columnasPosiciones=0, puntos=0, partidos=0, wins=0,
                  draws=0, loses=0, afavor=0, encontra=0, ganados=[], perdidos=[], empatados=[],
                  golesAfavorUltimasJornadas=0, golesEncontraUltimasJornadas=0, maximosGoles=0, minimosGoles=0,
                  maximosGolesEnContra=0, minimosGolesEnContra=0, mediaGolPorPartidoMarcados=0,
                  mediaGolPorPartidoEnContra=0):  # Llamo a los datos que me interan ya inicializados y les añado el valor que he dado en la entrada de la clase
        self.columnaPosiciones = columnasPosiciones
        self.puntos = puntos
        self.partidos = partidos
        self.wins = wins
        self.loses = loses
        self.draws = draws
        self.afavor = afavor
        self.encontra = encontra
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
            self.columnaPosiciones,
            self.name,
            self.puntos,
            self.partidos,
            self.wins,
            self.draws,
            self.loses,
            self.afavor,
            self.encontra,
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
            "Position",
            "Team",
            "Points",
            "Matches",
            "Wins",
            "Draws",
            "Loses",
            "G_Scored",
            "G_Against",
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

def getTeamsObjects(soupOfTeams):
    listOfTeams = []
    tableData = soupOfTeams.find('table', {'class': "styled__TableStyled-sc-43wy8s-1 iOBNZZ"})
    eachRowMatch = tableData.find_all('div', {'class': 'styled__MatchStyled-sc-2hkd8m-1 jVNhaC'})
    for row in eachRowMatch:
        results = row.find_all('p', {'class': 'styled__TextRegularStyled-sc-1raci4c-0 fYuQIM'})
        teams = row.find_all('p', {'class': 'styled__TextRegularStyled-sc-1raci4c-0 hvREvZ'})
        lenOfTeams = len(teams)
        for i in range(lenOfTeams):
            # print(teams[i].contents[0], results[i].contents[0])
            teamClass = Equipo(teams[i].contents[0])
            listOfTeams.append(teamClass)
        # for t in teams:
        #     listOfTeams.append(t.contents[0])
        #     print(t.contents[0])
        # # goals = soupOfTeams.find_all('p', {'class': 'styled__TextRegularStyled-sc-1raci4c-0 fYuQIM'})
        # for r in results:
        #     g = r.find_all('p', {'class': 'styled__TextRegularStyled-sc-1raci4c-0 fYuQIM'})
        #     for gg in g:
        #         print(gg.contents[0])
        # break

    # for team in currentDay:
    #     teamObject = Equipo(team.contents[0])
    #     listOfTeams.append(teamObject)
    return listOfTeams

def getEquipo(teamName, listaDeEquipos):
    for b in listaDeEquipos:
        if b.name == teamName:
            return b

# route = requests.get('https://www.laliga.com/laliga-santander/resultados')  # Get URL
route = requests.get('https://www.laliga.com/laliga-santander/resultados/2022-23/jornada-20')  # Get URL

soupOfTeams = BeautifulSoup(route.text, 'html.parser')  # Use this format to read it

#For day BASE (obtener), -i to iter (4,5,6,7...) result efficiency

listOfPrimera = getTeamsObjects(soupOfTeams)
#obtener modulo de partidos de X jornada:
for i in listOfPrimera:
    print(i.name)