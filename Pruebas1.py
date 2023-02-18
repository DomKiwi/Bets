####################################################################################################################################################################
######################################################  FIRST MODULE / FIRST DIVISION   ############################################################################
####################################################################################################################################################################
pagePrimeraDivision = requests.get('https://www.resultados-futbol.com/primera')  # Get URL

def searchForEachLeague(route):
    listOfTeams = []

    # Lets start the program searching for Data in website
    soupPrimeraDivision = BeautifulSoup(pagePrimeraDivision.text, 'html.parser')  # Use this format to read it

    blockquote_items = soupPrimeraDivision.find('table', {'id': 'tabla2'})  # Use Bs4 to find specific data
    blockquote_items = blockquote_items.find('tbody')
    blockquote_items = blockquote_items.find_all('tr')

    # Get name of teams and create a class for each one
    for num, blockquote in enumerate(blockquote_items):
        equipo = blockquote.find("td", {"class": ["equipo", "equipo sube", "equipo baja"]}).find('a').contents[0]
        team = Equipo(equipo)
        listOfTeams.append(team)

    ####################################################################################################################################################################
    # del bloque buscado empiezo a obtener los datos
    for num, blockquote in enumerate(blockquote_items):
        # con cada equipo poner su fila en horizontal todos los datos, escribo todas las opciones para que recoga los datos
        columnaPosiciones = \
            blockquote.find("th",
                            {"class": ["pos2 pos-cha", "pos3 pos-uefa", "pos5 pos-conf", "", "pos6 pos-desc", "pos2 pos-asc", "pos3 pos-play", "pos5 pos-desc"]}).contents[0]
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
        equiposQueHaEmpatado = []
        golesAfavorUltimasJornadas = 0
        golesEncontraUltimasJornadas = 0
        minimosGoles = 100
        maximosGoles = 0
        minimosGolesEnContra = 100
        maximosGolesEnContra = 0
        for x, resultado in enumerate(resultadopartidos):
            if x == 0: continue
            resultadoDelPartido = resultado.find("li", {"class": "title g"}).contents[0]
            equiposDelPartido = resultado.find_all("b", {"class": "bname"})
            ambosEquipos = [b.get_text() for b in equiposDelPartido]
            for num_1, b in enumerate(
                    ambosEquipos):  # Correccion por culpa de la Website de cambiar nombres asi porque si
                if equipo in b:
                    ambosEquipos[num_1] = equipo
                if 'Deportivo' in b:
                    ambosEquipos[num_1] = 'Deportivo'
            equipoContrario = ambosEquipos.copy()
            equipoContrario.remove(equipo)
            golesDelPartido = resultado.find_all("b", {"class": "bres"})
            golesDeAmbos = [b.get_text() for b in golesDelPartido]
            equiposYgoles = dict(map(lambda i, j: (i, j), ambosEquipos, golesDeAmbos))

            if int(equiposYgoles[equipo]) > maximosGoles: maximosGoles = int(equiposYgoles[equipo])
            if int(equiposYgoles[equipo]) < minimosGoles: minimosGoles = int(equiposYgoles[equipo])
            if int(equiposYgoles[equipoContrario[0]]) > maximosGolesEnContra: maximosGolesEnContra = int(
                equiposYgoles[equipoContrario[0]])
            if int(equiposYgoles[equipoContrario[0]]) < minimosGolesEnContra: minimosGolesEnContra = int(
                equiposYgoles[equipoContrario[0]])

            golesAfavorUltimasJornadas = golesAfavorUltimasJornadas + int(equiposYgoles[equipo])
            golesEncontraUltimasJornadas = golesEncontraUltimasJornadas + int(equiposYgoles[equipoContrario[0]])

            teamObject = getEquipo(equipo, listOfTeams)
            newEnemyName = equipoContrario[0]
            newEnemyObject = getEquipo(newEnemyName, listOfTeams)
            if resultadoDelPartido == 'VICTORIA':
                equiposQueHaGanado.append(newEnemyObject)
            if resultadoDelPartido == 'DERROTA':
                equiposQueHaperdido.append(newEnemyObject)
            if resultadoDelPartido == 'EMPATE':
                equiposQueHaEmpatado.append(newEnemyObject)

        numDePartidos = len(equiposQueHaGanado) + len(equiposQueHaperdido) + len(equiposQueHaEmpatado)
        mediaGolPorPartidoMarcados = golesAfavorUltimasJornadas / numDePartidos
        mediaGolPorPartidoEnContra = golesEncontraUltimasJornadas / numDePartidos

        teamObject.setvalues(columnaPosiciones, puntos, partidos, wins, draws, loses,
                             afavor, encontra, equiposQueHaGanado, equiposQueHaperdido, equiposQueHaEmpatado,
                             golesAfavorUltimasJornadas, golesEncontraUltimasJornadas, maximosGoles, minimosGoles,
                             maximosGolesEnContra, minimosGolesEnContra, mediaGolPorPartidoMarcados,
                             mediaGolPorPartidoEnContra)
    return listOfTeams

listaDeEquiposDePrimera = searchForEachLeague(pagePrimeraDivision)