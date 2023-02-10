from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests

class Equipo:
    columnaPosiciones = 0
    name = ""
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

    def getDataframe(self):
        recopilacionequipo = [self.columnaPosiciones, self.name, self.puntos, self.partidos,self.wins, self.loses, self.draws, self.afavor, self.encontra, self.equiposQueHaGanado,self.equiposQueHaPerdido, self.equiposQueHaEmpatado]
        recopilacionequipo = pd.DataFrame(recopilacionequipo).transpose()
        return recopilacionequipo
        
    def __init__(self, columnasPosiciones, name, puntos, partidos, wins, loses, draws, afavor, encontra, ganados, perdidos, empatados):
        self.columnaPosiciones = columnasPosiciones
        self.name = name
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
    # def atexto(self):
    #     return str(self.name , self.puntos, self.partidos,self.wins, self.loses, self.draws, self.afavor, self.encontra, self.wins, self.loses, self.draws)


page = requests.get('https://www.resultados-futbol.com/primera')
soup = BeautifulSoup(page.text, 'html.parser')

blockquote_items = soup.find('table', {'id': 'tabla2'})
blockquote_items = blockquote_items.find('tbody')
blockquote_items = blockquote_items.find_all('tr')
# print(blockquote_items)
# print(blockquote_items)
listaDeEquipos = []
header = ["posicion", "nombre", "puntos", "partidos", "ganados", "empatados", "perdidos", "afavor", "encontra", "victorias", "derrotas", "empates"]
dataframetotal = pd.DataFrame(header).transpose()
print(dataframetotal)

for num, blockquote in enumerate(blockquote_items):
    #con cada equipo poner su fila en horizontal todos los datos, escribo todas las opciones para que recoga los datos
    columnaPosiciones = blockquote.find("th", {"class": ["pos2 pos-cha", "pos3 pos-uefa", "pos5 pos-conf", "", "pos6 pos-desc"]}).contents[0]
    # print(columnaPosiciones)
    # columnaPosiciones = "hola"

    equipo = blockquote.find("td", {"class": ["equipo", "equipo sube", "equipo baja"]})
    equipo = equipo.find('a').contents[0]

    puntos = blockquote.find("td", {"class": "pts"}).contents[0]
    partidos = blockquote.find("td", {"class": "pj"}).contents[0]
    wins = blockquote.find("td", {"class": "win"}).contents[0]
    draws = blockquote.find("td", {"class": "draw"}).contents[0]
    loses = blockquote.find("td", {"class": "lose"}).contents[0]

    Data = Equipo(columnaPosiciones, equipo, puntos, partidos, wins, loses, draws, 0, 0, [], [], [])
    recopilacionDeDatos = Data.getDataframe()
    print(type(recopilacionDeDatos))
    dataframetotal = pd.concat([dataframetotal,recopilacionDeDatos])
    listaDeEquipos.append(Data)

    # fila = blockquote.find(id='')
    # filaPar = blockquote.find(class = 'cmp')
    # filaImpar = blockquote.find(class = 'impar')
    # for x in columnaPosiciones:
    #     print(x.text)

# for equipo in listaDeEquipos:
# print(pd.DataFrame(listaDeEquipos))
# print(pd.DataFrame.from_dict(Puntos, orient='index', columns=['Puntos']))
print(dataframetotal)
