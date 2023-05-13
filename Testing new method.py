import itertools
import statistics

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
from statistics import mean


def createListIfNone(listaDada):
    if listaDada is None: listaDada = []

class Equipo:
    # Agrego valores iniciales de los datos que me interesan de la pagina web como otros que quiera crear yo nuevos
    ## DATOS ENTRANTES
    name = ""
    equiposQueHaGanado = []
    equiposQueHaPerdido = []
    equiposQueHaEmpatado = []
    golesAFavor = []
    golesEnContra = []

    puntosDeDebilidad = 0
    puntosDeFuerza = 0

    ## DATOS CALCULADOS INTERNAMENTE
    equiposQueHaEmpatadoNombre = []
    equiposQueHaGanadoNombre = []
    equiposQueHaPerdidoNombre = []

    golesAFavorAverage = 0
    golesAFavorMax = 0
    golesAFavorMin = 0
    golesAFavorDesV = 0

    golesEnContraAverage = 0
    golesEnContraMax = 0
    golesEnContraMin = 0
    golesEnContraDesV = 0

    def __init__(self, name, ganados=None, perdidos=None, empatados=None,
                 golesAfavor=None, golesEnContra=None):
        self.name = name
        createListIfNone(ganados)
        createListIfNone(perdidos)
        createListIfNone(empatados)
        createListIfNone(golesAfavor)
        createListIfNone(golesEnContra)

    def calculateFormulas(self):
        self.golesAFavorAverage = mean(self.golesAFavor)
        self.golesAFavorMax = max(self.golesAFavor)
        self.golesAFavorMin = min(self.golesAFavor)
        self.golesAFavorDesV = statistics.pstdev(self.golesAFavor)

        self.golesEnContraAverage = mean(self.golesEnContra)
        self.golesEnContraMax = max(self.golesEnContra)
        self.golesEnContraMin = min(self.golesEnContra)
        self.golesEnContraDesV = statistics.pstdev(self.golesEnContra)

        self.equiposQueHaGanadoNombre = [tm.name for tm in self.equiposQueHaGanado]
        self.equiposQueHaPerdidoNombre = [tm.name for tm in self.equiposQueHaPerdido]
        self.equiposQueHaEmpatadoNombre = [tm.name for tm in self.equiposQueHaEmpatado]


###################################################################################################################################################################
def getEquipo(teamName, listaDeEquipos):
    for b in listaDeEquipos:
        if b.name == teamName:
            return b

###################################################################################################################################################################
def getLinkHtml(route):
    soupOfLinks = []
    for links in route:
        link_py = requests.get(links)
        soupOfLinks.append(BeautifulSoup(link_py.text, 'html.parser'))
    return soupOfLinks

###################################################################################################################################################################
def getTeamsObjects(route):
    listOfTeams = []
    for URLWebsite in route:
        tableData = URLWebsite.find('table', {'class': "styled__TableStyled-sc-43wy8s-1 iOBNZZ"})
        eachRowMatch = tableData.find_all('div', {'class': 'styled__MatchStyled-sc-2hkd8m-1 jVNhaC'})
        for row in eachRowMatch:
            teams = row.find_all('p', {'class': 'styled__TextRegularStyled-sc-1raci4c-0 hvREvZ'})
            lenOfTeams = len(teams)
            for i in range(lenOfTeams):
                teamClass = Equipo(teams[i].contents[0])
                listOfTeams.append(teamClass)
    return listOfTeams

###################################################################################################################################################################
def metodoFuerza(iter, teamToCheck, teamToAddPoints, teamsCountedAlready, resetPoints, valorDePuntos, factorDegenerativo):
    if resetPoints:
        teamToAddPoints.puntosDeFuerza = 0
    if iter <= 0:
        return
    for G in teamToCheck.equiposQueHaGanado:
        teamToAddPoints.puntosDeFuerza += 1*valorDePuntos
        if G in teamsCountedAlready:
            continue
        iter -= 1
        teamsCountedAlready.append(G)
        valorDePuntosNuevo = valorDePuntos*factorDegenerativo   # Poner valorDePuntos en la funcion de vuelta y variar las dos variables
        metodoFuerza(iter, G, teamToAddPoints, teamsCountedAlready, False, valorDePuntosNuevo,factorDegenerativo)

###################################################################################################################################################################
def metodoDebilidad(iter, teamToCheck, teamToAddPoints, teamsCountedAlready, resetPoints, valorDePuntos, factorDegenerativo):
    if resetPoints:
        teamToAddPoints.puntosDeDebilidad = 0
    if (iter <= 0): return
    for L in teamToCheck.equiposQueHaPerdido:
        teamToAddPoints.puntosDeDebilidad += 1*valorDePuntos
        if L in teamsCountedAlready:
            continue
        iter -= 1
        teamsCountedAlready.append(L)
        valorDePuntosNuevo = factorDegenerativo * valorDePuntos
        metodoDebilidad(iter, L, teamToAddPoints, teamsCountedAlready, False, valorDePuntosNuevo, factorDegenerativo)

###################################################################################################################################################################
def addPointsStrengthWeakness(listOfTeams, resetPoints, valorDePuntos, factorDegenerativo):
    for team in listOfTeams:
        iter = 200
        metodoFuerza(iter, team, team, [], resetPoints, valorDePuntos, factorDegenerativo)
        metodoDebilidad(iter, team, team, [], resetPoints, valorDePuntos, factorDegenerativo)

###################################################################################################################################################################
def getPreviousJourneys(routeRef, itermax):  # INWORK
    linkPreviousJourneys_eachURL = {}
    for routeRef_individual in routeRef:
        # busco la jornada actual
        journeys = routeRef_individual.find('div', {'class': 'styled__SubHeaderCalendarGrid-sc-1engvts-8 iYpljZ'}).find('div', {
            'class': 'styled__DropdownContainer-d9k1bl-0 kmhQzc'})
        currentJourney = journeys.find('span').contents[0]
        # busco las jornadas
        eachjourney = journeys.find('ul', {'class': 'styled__ItemsList-d9k1bl-2 hkGQnA'}).find_all('a')
        lenJourneys = len(eachjourney)
        previousJourneys = []
        linkPreviousJourneys = []  # uso esto para buscar cada jornada
        for numday, day in enumerate(eachjourney):
            linkPreviousJourneys.append('https://www.laliga.com/' + day['href'])
            previousJourneys.append(day.contents[0])
            if day.contents[0] == currentJourney:
                del previousJourneys[:numday - itermax]
                previousJourneys = previousJourneys[:-1]
                del linkPreviousJourneys[:numday - itermax]
                linkPreviousJourneys = linkPreviousJourneys[:-1]
                break
        previousJourneys.reverse()
        linkPreviousJourneys.reverse()
        linkPreviousJourneys_eachURL[routeRef_individual] = linkPreviousJourneys
    return linkPreviousJourneys_eachURL

###################################################################################################################################################################
def getResults(routes, there_are_results):
    for eachLeague in routes:
        tableData = eachLeague.find('table', {'class': "styled__TableStyled-sc-43wy8s-1 iOBNZZ"})
        eachRowMatch = tableData.find_all('div', {'class': 'styled__MatchStyled-sc-2hkd8m-1 jVNhaC'})
        resultadosPartidos = []
        for row in eachRowMatch:
            match = {}
            results = row.find_all('p', {'class': 'styled__TextRegularStyled-sc-1raci4c-0 fYuQIM'})
            teams = row.find_all('p', {'class': 'styled__TextRegularStyled-sc-1raci4c-0 hvREvZ'})
            lenOfTeams = len(teams)
            if there_are_results:
                for i in range(lenOfTeams):
                    match[teams[i].contents[0]] = results[i].contents[0]
            else:
                for i in range(lenOfTeams):
                    match[teams[i].contents[0]] = 'No Data'
            resultadosPartidos.append(match)

    return resultadosPartidos

###################################################################################################################################################################
def lecturaDeJornada(resultadosEstaJornada, listOfTeams, there_is_data, it_is_Reference):
    for match in resultadosEstaJornada:
        teams = list(match.keys())
        team_1 = getEquipo(teams[0], listOfTeams)
        team_2 = getEquipo(teams[1], listOfTeams)
        if there_is_data and it_is_Reference:
            team_1.equiposQueHaGanado = []
            team_1.equiposQueHaPerdido = []
            team_2.equiposQueHaPerdido = []
            team_2.equiposQueHaGanado = []
            team_1.equiposQueHaEmpatado = []
            team_2.equiposQueHaEmpatado = []
            if match[teams[0]] > match[teams[1]]:
                match['Resultado'] = 1
            if match[teams[0]] < match[teams[1]]:
                match['Resultado'] = 2
            if match[teams[0]] == match[teams[1]]:
                match['Resultado'] = 'x'
        elif there_is_data is False and it_is_Reference:
            team_1.equiposQueHaGanado = []
            team_1.equiposQueHaPerdido = []
            team_2.equiposQueHaPerdido = []
            team_2.equiposQueHaGanado = []
            team_1.equiposQueHaEmpatado = []
            team_2.equiposQueHaEmpatado = []
        else:
            if match[teams[0]] > match[teams[1]]:
                team_1.equiposQueHaGanado.append(team_2)
                team_2.equiposQueHaPerdido.append(team_1)
                match['Resultado'] = 1
            if match[teams[0]] < match[teams[1]]:
                match['Resultado'] = 2
                team_2.equiposQueHaGanado.append(team_1)
                team_1.equiposQueHaPerdido.append(team_2)
            if match[teams[0]] == match[teams[1]]:
                match['Resultado'] = 'x'
                team_1.equiposQueHaEmpatado.append(team_2)
                team_2.equiposQueHaEmpatado.append(team_1)
    return resultadosEstaJornada

###################################################################################################################################################################
def calculatePointsAndPorcentaje(resultadosTotalDeReferencia, listOfTeams, there_is_data, margenDeError,printData, printDataForMaxProb):
    numHits = 0
    for partido in resultadosTotalDeReferencia:
        llaves = list(partido.keys())
        team_1 = getEquipo(llaves[0], listOfTeams)
        team_2 = getEquipo(llaves[1], listOfTeams)
        pointsTeam_1 = team_1.puntosDeFuerza + team_2.puntosDeDebilidad
        pointsTeam_2 = team_2.puntosDeFuerza + team_1.puntosDeDebilidad
        minimumP = min([pointsTeam_1, pointsTeam_2])
        if minimumP == 0:
            minimumP = 1
        pointsTeam_1_Normalized = abs(round(pointsTeam_1 / minimumP, 5))
        pointsTeam_2_Normalized = abs(round(pointsTeam_2 / minimumP, 5))
        if there_is_data:
            if printData and printDataForMaxProb:
                print(team_1.name, round(pointsTeam_1_Normalized, 2), round(pointsTeam_2_Normalized, 2), team_2.name,
                  partido[llaves[2]])
            if abs(pointsTeam_1_Normalized - pointsTeam_2_Normalized) > margenDeError and pointsTeam_1_Normalized > pointsTeam_2_Normalized and \
                    partido[llaves[2]] == 1:
                numHits += 1
            if abs(pointsTeam_1_Normalized - pointsTeam_2_Normalized) > margenDeError and pointsTeam_1_Normalized < pointsTeam_2_Normalized and \
                    partido[llaves[2]] == 2:
                numHits += 1
            if abs(pointsTeam_1_Normalized - pointsTeam_2_Normalized) < margenDeError and partido[llaves[2]] == 'x':
                numHits += 1
        else:
            if printData and printDataForMaxProb:
                print(team_1.name, round(pointsTeam_1_Normalized, 2), round(pointsTeam_2_Normalized, 2), team_2.name)

    porcentajeAcierto = 100 * numHits / len(resultadosTotalDeReferencia)
    return porcentajeAcierto, margenDeError












###################################################################################################################################################################
# INPUT DATA #
URL_Ref_1 = 'https://www.laliga.com/laliga-santander/resultados'
URL_Ref_2 = 'https://www.laliga.com/laliga-smartbank/resultados'
URL_Ref_3 = 'https://www.laliga.com/futbol-femenino/resultados'
URL = [URL_Ref_1, URL_Ref_2, URL_Ref_3]

in_this_link_there_are_results_Ref = False
maxValueOfMatchsCalculated_Ref = 5


###################################################################################################################################################################
maxValueOfMatchsCalculated_Ref = maxValueOfMatchsCalculated_Ref + 1
URL_in_HTML = getLinkHtml(URL)
listOfTotalTeams = getTeamsObjects(URL_in_HTML)


print('/////////////////////////////////////////////////////////////////////////////////////////////////')
print('Entramos en la jornada SELECCIONADA')
linksOfPreviousJourneys = getPreviousJourneys(URL_in_HTML, maxValueOfMatchsCalculated_Ref)
print('Usaremos los siguientes links para su calculo de probabilidad: ' + str(linksOfPreviousJourneys))

def iterateThroughJourneys(listOfTeams,linksPreviousJourneys,maxValueMatchesCalculated, there_is_data):
    datosRecopiladosJornada = []
    for num in range(1, maxValueMatchesCalculated, 1):
        for numLink, linkRep in enumerate(linksPreviousJourneys):
            soup_repetible = getLinkHtml(linksPreviousJourneys[linkRep][:num])
            #actualizo resultados de esta jornada
            results_rep = getResults(soup_repetible, True)
            datosRecopiladosJornada[linkRep] = lecturaDeJornada(results_rep, listOfTeams, True, False)
        #for???
        if there_is_data:
            #Mejor combinacion para mayor % de acierto
            factoresDegenerativos = np.arange(-0.4, 0.95, 0.1)
            valoresDePuntos = np.arange(0.1, 0.95, 0.05)
            for valorDePuntos_iter in valoresDePuntos:
                for factorDegenerativo_iter in factoresDegenerativos:
                    addPointsStrengthWeakness(listOfTeams, True, valorDePuntos_iter, factorDegenerativo_iter)
                    # Margen de Error para Empate
                    max_error_margen = np.arange(0, 0.5, 0.01)
                    porcentajeYMargenError = {}
                    for iError in max_error_margen:
                        porcentajeDeAcierto, margenDeError = calculatePorcentaje(datosRecopiladosJornada)
                        porcentajeYMargenError[margenDeError] = porcentajeDeAcierto
        else:


        #llamo a la funcion para obtener el porcentaje de aciertos.


cuantasJornadasCojemos = iterateThroughJourneys()
resultadosJornadaDeReferencia = getResults(linksOfPreviousJourneys, in_this_link_there_are_results_Ref)




checkLastResultsWithTheMethod = checkIfMethodWorksInLastestJourneys(URL_in_HTML, linksOfPreviousJourneys,maxValueOfMatchsCalculated_Ref)

###################################################################################################################################################################
# listOfPrimera = getDataOfMaxEfficiency(URL_Ref, in_this_link_there_are_results_Ref, maxValueOfMatchsCalculated_Ref)
for i in listOfTotalTeams:
    print(i.name)







def checkIfMethodWorksInLastestJourneys(URL_in_HTML, linksPreviousJourneys, maxValueOfMatchsCalculated):
    for num in range(1, maxValueOfMatchsCalculated, 1):
        for numLeague, eachLeague in enumerate(linksPreviousJourneys):
            print(linksPreviousJourneys[eachLeague][:num])
            soup_repetible = getLinkHtml(linksPreviousJourneys[eachLeague][:num])
            results_rep = getResults(soup_repetible)


            # print('#####################################################################################################################################################################')
            # print('Entramos en la jornada: ' + str(previousJourneys_Repeticiones[numLink]))
            # getPorcentaje(soup_rep, maxValueOfMatchsCalculated, listOfTeams, results_rep, True)
            # print('/////////////////////////////////////////////////////////////////////////////////////////////////')
            # print('CAMBIO DE JORNADA QUE COMPROBAR')
        print(len(eachLeague))