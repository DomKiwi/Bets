from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
from IPython.display import display
class Equipo:       #Clasificacion de Equipos con sus respectivos datos de interes como puntos, victorias, equipos contrarios vencidos, etc..
    'Agrego valores iniciales de los datos que me interesan de la pagina web como otros que quiera crear yo nuevos'
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
    golesEncontraUltimasJornadas = 0
    golesAfavorUltimasJornadas = 0
    maximosGoles = 0
    minimosGoles = 0
    maximosGolesEnContra = 0
    minimosGolesEnContra = 0
    mediaGolPorPartidoMarcados = 0
    mediaGolPorPartidoEnContra = 0

    def getDataframe(self):         #de los valores que estoy trabajando, los meto en un dataframe para manejarlos mejor
        recopilacionequipo = [self.columnaPosiciones, self.name,
                              self.puntos, self.partidos, self.wins, self.draws, self.loses,  self.afavor, self.encontra, self.equiposQueHaGanado,self.equiposQueHaPerdido,
                              self.equiposQueHaEmpatado, self.golesAfavorUltimasJornadas, self.golesEncontraUltimasJornadas, self.maximosGoles, self.minimosGoles,
                              self.maximosGolesEnContra, self.minimosGolesEnContra, self.mediaGolPorPartidoMarcados,
                              self.mediaGolPorPartidoEnContra
                              ]
        recopilacionequipo = pd.DataFrame(recopilacionequipo).transpose()
        return recopilacionequipo
        
    def __init__(self, columnasPosiciones, name, puntos, partidos, wins,
                 draws, loses, afavor, encontra, ganados, perdidos, empatados,
                 golesAfavorUltimasJornadas, golesEncontraUltimasJornadas, maximosGoles, minimosGoles,
                 maximosGolesEnContra,minimosGolesEnContra, mediaGolPorPartidoMarcados, mediaGolPorPartidoEnContra):     #Llamo a los datos que me interan ya inicializados y les añado el valor que he dado en la entrada de la clase
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
        self.golesAfavorUltimasJornadas = golesAfavorUltimasJornadas
        self.golesEncontraUltimasJornadas = golesEncontraUltimasJornadas
        self.maximosGoles = maximosGoles
        self.minimosGoles = minimosGoles
        self.maximosGolesEnContra = maximosGolesEnContra
        self.minimosGolesEnContra = minimosGolesEnContra
        self.mediaGolPorPartidoMarcados = mediaGolPorPartidoMarcados
        self.mediaGolPorPartidoEnContra = mediaGolPorPartidoEnContra

page = requests.get('https://www.resultados-futbol.com/primera')
soup = BeautifulSoup(page.text, 'html.parser')

blockquote_items = soup.find('table', {'id': 'tabla2'})
blockquote_items = blockquote_items.find('tbody')
blockquote_items = blockquote_items.find_all('tr')
listaDeEquipos = []
dataframetotal = pd.DataFrame()

for num, blockquote in enumerate(blockquote_items):
    #con cada equipo poner su fila en horizontal todos los datos, escribo todas las opciones para que recoga los datos

    columnaPosiciones = blockquote.find("th", {"class": ["pos2 pos-cha", "pos3 pos-uefa", "pos5 pos-conf", "", "pos6 pos-desc"]}).contents[0]
    equipo = blockquote.find("td", {"class": ["equipo", "equipo sube", "equipo baja"]}).find('a').contents[0]
    puntos = blockquote.find("td", {"class": "pts"}).contents[0]
    partidos = blockquote.find("td", {"class": "pj"}).contents[0]
    wins = blockquote.find("td", {"class": "win"}).contents[0]
    draws = blockquote.find("td", {"class": "draw"}).contents[0]
    loses = blockquote.find("td", {"class": "lose"}).contents[0]
    afavor = blockquote.find("td", {"class": "f"}).contents[0]
    encontra = blockquote.find("td", {"class": "c"}).contents[0]

    resultadopartidos = blockquote.find_all("span", {"class": "classicsmall"})
    equiposQueHaGanado = []
    equiposQueHaperdido = []
    equiposQueHaEmpatado =[]
    golesAfavorUltimasJornadas = 0
    golesEncontraUltimasJornadas = 0
    minimosGoles = 100
    maximosGoles = 0
    minimosGolesEnContra = 100
    maximosGolesEnContra = 0
    for resultado in resultadopartidos:
        resultadoDelPartido = resultado.find("li", {"class": "title g"}).contents[0]
        equiposDelPartido = resultado.find_all("b", {"class": "bname"})
        ambosEquipos = [b.get_text() for b in equiposDelPartido]
        equipoContrario = ambosEquipos.copy()
        equipoContrario.remove(equipo)
        golesDelPartido = resultado.find_all("b", {"class": "bres"})
        golesDeAmbos = [b.get_text() for b in golesDelPartido]
        equiposYgoles = dict(map(lambda i, j: (i, j), ambosEquipos, golesDeAmbos))

        if int(equiposYgoles[equipo])>maximosGoles: maximosGoles = int(equiposYgoles[equipo])
        if int(equiposYgoles[equipo])<minimosGoles: minimosGoles = int(equiposYgoles[equipo])
        if int(equiposYgoles[equipoContrario[0]])>maximosGolesEnContra: maximosGolesEnContra = int(equiposYgoles[equipoContrario[0]])
        if int(equiposYgoles[equipoContrario[0]])<minimosGolesEnContra: minimosGolesEnContra = int(equiposYgoles[equipoContrario[0]])

        golesAfavorUltimasJornadas = golesAfavorUltimasJornadas + int(equiposYgoles[equipo])
        golesEncontraUltimasJornadas = golesEncontraUltimasJornadas + int(equiposYgoles[equipoContrario[0]])

        if resultadoDelPartido == 'VICTORIA':
            equiposQueHaGanado.append(equipoContrario[0])
        if resultadoDelPartido == 'DERROTA':
            equiposQueHaperdido.append(equipoContrario[0])
        if resultadoDelPartido == 'EMPATE':
            equiposQueHaEmpatado.append(equipoContrario[0])

    numDePartidos = len(equiposQueHaGanado) + len(equiposQueHaperdido) + len(equiposQueHaEmpatado)
    mediaGolPorPartidoMarcados = golesAfavorUltimasJornadas/numDePartidos
    mediaGolPorPartidoEnContra = golesEncontraUltimasJornadas/numDePartidos

    Data = Equipo(columnaPosiciones, equipo, puntos, partidos, wins, draws, loses,
                  afavor, encontra, equiposQueHaGanado, equiposQueHaperdido, equiposQueHaEmpatado,
                  golesAfavorUltimasJornadas, golesEncontraUltimasJornadas, maximosGoles, minimosGoles,
                  maximosGolesEnContra,minimosGolesEnContra, mediaGolPorPartidoMarcados, mediaGolPorPartidoEnContra
                  )
    recopilacionDeDatos = Data.getDataframe()
    dataframetotal = pd.concat([dataframetotal,recopilacionDeDatos])
    listaDeEquipos.append(Data)





header = ["posicion", "nombre", "puntos", "partidos", "ganados", "empatados",
          "perdidos", "afavor", "encontra", "Ha Ganado vs", "Ha perdido vs",
          "Ha empatado vs", "golesAfavorUltimas5", "golesEnContraUltimas5", "maximos goles marcados ultimos5", "minimos goles marcados ultimos5", "maximos goles en contra ultimo5", "minimos goles en contra ultimos5",
          "media gol marcado ultimos5", "media gol en contra ultimos5"]
dataframetotal.columns = header
print(dataframetotal.to_string())

dataframetotal.to_excel("output.xlsx", sheet_name = "Datos en vivo", index=0)





#Implementar:
    #Grafica por cada quiepo con medias y desviaciones
    #añadir metodologias de probabilidad para los datos recogidos
    #