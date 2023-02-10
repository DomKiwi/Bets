
import xlrd
import xlwt
import os
import PySimpleGUI as sg            #Tambien esta EASYGUI
import numpy as np
import pandas as pd
import openpyxl
import functools
import pyexcel as pyexcel


class pepito:

    def __init__(self):
        pass
    def setupLayout(self):
        sg.theme('Dark Grey 13')
        layout = [[sg.Image(source='Obuu_logo.png')],
                  [sg.Input(), sg.FileBrowse(key="Excel")],
                  [sg.Input(), sg.FileBrowse(key="ExcelAlternate")],
                  [sg.Input(), sg.FileBrowse(key="ExcelAlternates")],
                  [sg.Input(key="ColFinal"), sg.Text('Introduce hasta que columna')],
                  [sg.OK(), sg.Cancel()]]
        window = sg.Window('Ejemplo File', layout)
        event, values = window.read()
        window.close()
        return values
    def spreadsheet_column_encoding(self, col):
        return functools.reduce(
            lambda result, char: result * 26 + ord(char) - ord("A") + 1, col, 0
        )
    def atexto(self, convert):
        if type(convert) is list:
            list_convert = []
            for i in convert:
                r = str(i)
                if self.isfloat(r) and 'E' not in r:
                    pos_decimal_r = r.find('.')   #Comienza en 0
                    p = float(r)
                    p_text = str(p)
                    pos_decimal_p = p_text.find('.')    #Comienza en 0
                    if pos_decimal_r != -1:     #Tiene puntos
                        dif_len = pos_decimal_r - pos_decimal_p
                    else:               # No tiene puntos
                        len_r = len(r)
                        len_p = len(p_text)-2
                        dif_len = len_r-len_p
                    if p.is_integer():
                        text_final1 = str(int(p))
                        text_final = text_final1.zfill(dif_len+len(text_final1))
                    else:
                        text_final1 = str(p)
                        text_final = text_final1.zfill(dif_len+len(text_final1))
                else:
                    text_final = r
                list_convert.append(text_final)
            resultado = list_convert
        else:
            r = str(convert)
            if self.isfloat(r) and 'E' not in r:
                pos_decimal_r = r.find('.')  # Comienza en 0
                p = float(r)
                p_text = str(p)
                pos_decimal_p = p_text.find('.')  # Comienza en 0
                if pos_decimal_r != -1:  # Tiene puntos
                    dif_len = pos_decimal_r - pos_decimal_p
                else:  # No tiene puntos
                    len_r = len(r)
                    len_p = len(p_text) - 2
                    dif_len = len_r - len_p
                if p.is_integer():
                    text_final1 = str(int(p))
                    text_final = text_final1.zfill(dif_len + len(text_final1))
                else:
                    text_final1 = str(p)
                    text_final = text_final1.zfill(dif_len + len(text_final1))
            else:
                text_final = r
            resultado = text_final
        return resultado
    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False
    def quitarnan_listas(self, lista):
        lista2 = [[y for y in x if pd.notna(y)] for x in lista.values.tolist()]
        return lista2
    def reunion_datos(self, referencias_listas,df3):
        for lista in referencias_listas:
            if len(lista[1:]) != 0:
                df2 = pd.DataFrame(columns=['uno', 'dos'])
                df2['dos'] = lista[1:]  # SOLUCIONAR ERROR DE SI ESTA VACIO
                df2['uno'] = lista[0]
            else:
                diccionario = {'uno': [lista[0]], 'dos': [lista[0]]}
                df2 = pd.DataFrame.from_dict(diccionario)
            df3 = pd.concat([df3, df2], axis=0)
            del df2
        return df3
    def agregarAlternativos(self):
        alts = []
        while True:
            entrada = input('Selecciona las columnas que tengan alternativas de estos Parts Numbers de una en una (Capital Letters) ')
            if entrada.strip():  # si contiene algo es True, de lo contrario False
                entrada1 = self.spreadsheet_column_encoding(entrada)-1
                alts.append(entrada1)  # agregamos en caso contenga algo
            else:
                break  # detenemos el ciclo for
        return alts
    def crearDataframeConReferencias(self, values):
        df = pd.read_excel(values["ExcelAlternates"], sheet_name=None)    # Hojas = df.keys()   #Nombres de las paginas
        df3 = pd.DataFrame()
        for key in df:
            p = pd.DataFrame(df[key])
            o = pd.DataFrame(df[key].head(5))
            print(key, o)
            partsNumbers = self.spreadsheet_column_encoding(input('Selecciona la columna de PartsNumbers de referencia '))-1
            listnumallref = [partsNumbers]
            dataframeDeReferencias = p.iloc[:, listnumallref]
            reunionDeP = dataframeDeReferencias
            # listaDeReferencias = dataframeDeReferencias.to_numpy().T.tolist()
            nombreCol = p.columns[partsNumbers]
            pSinRef = p.drop(nombreCol, axis=1)
            referencias_listas = self.obtenerColsAlternate(pSinRef,dataframeDeReferencias,reunionDeP)
            #Agrupacion de datos
            df3 = self.reunion_datos(referencias_listas,df3)
        return df3
    def obtenerColsAlternate(self,p,dataframeDeReferencias,reunionDeP):
        for r, columna in enumerate(p):
            print(columna)
            q = 0
            for valor in p[columna]:
                if dataframeDeReferencias.isin([valor]).any().any():
                    q = q+1
                    if q > 10:
                        reunionDeP = pd.concat([reunionDeP, p[columna]], axis=1)
                        break
        reunionDeP.to_excel(self.wb2, sheet_name= reunionDeP.columns[0], index=False)
        reunionDePSinNan = self.quitarnan_listas(reunionDeP)  #meto dataframe con Nan y saco listas sin nan
        return reunionDePSinNan
            # alts2 = self.agregarAlternativos()
            # listnumallref.extend(alts2)
            # referencias = p.iloc[:, listnumallref]
    def estiloDelArte(self,wb,colorNum):
        style = xlwt.XFStyle()

        font = xlwt.Font()
        font.name = 'Times New Roman'
        font.height = 20 * 11
        font.bold = True
        style.font = font

        pattern = xlwt.Pattern()
        pattern.pattern = pattern.SOLID_PATTERN
        if colorNum == 1:
            pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']
        elif colorNum == 2:
            xlwt.add_palette_colour("azul", 0x21)
            wb.set_colour_RGB(0x21, 0, 141, 210)
            pattern.pattern_fore_colour = xlwt.Style.colour_map['azul']
        elif colorNum == 3:
            xlwt.add_palette_colour("rojo", 0x20)
            wb.set_colour_RGB(0x20, 255, 204, 204)
            pattern.pattern_fore_colour = xlwt.Style.colour_map['rojo']
        elif colorNum == 4:
            pattern.pattern_fore_colour = xlwt.Style.colour_map['light_green']
        elif colorNum == 5:
            xlwt.add_palette_colour("grisaceo", 0x23)
            wb.set_colour_RGB(0x23, 224, 224, 224)
            pattern.pattern_fore_colour = xlwt.Style.colour_map['grisaceo']
        else:
            pattern.pattern_fore_colour = xlwt.Style.colour_map['ice_blue']
        style.pattern = pattern

        alignment = xlwt.Alignment()
        alignment.horz = alignment.HORZ_RIGHT
        style.alignment = alignment

        borders = xlwt.Borders()
        borders.right = borders.THIN
        borders.bottom = borders.THIN
        style.borders = borders
        return style
        # 1 Gris oscurillo   #2 azul     #3 rojo     #4 light_green    #5 grisaceo   #6 ice Blue
    def filtro(self, values):
        WB = xlrd.open_workbook(values["Excel"])
        wbFiltro = xlwt.Workbook()
        style1 = self.estiloDelArte(wbFiltro, 1)
        style2 = self.estiloDelArte(wbFiltro, 2)

        NumeroColFinal = self.spreadsheet_column_encoding(values["ColFinal"])
        Referencias1 = []
        Paginas = WB.sheets()
        for pagina in Paginas:
            Referencias1.extend(WB.sheet_by_name(pagina.name).col_values(0, 1))
        RefsNuevas = list(dict.fromkeys(Referencias1))
        Referencias = self.atexto(Referencias1)
        ReferenciasUnicas = list(dict.fromkeys(Referencias))
        print(len(RefsNuevas))
        LongColRef = 0
        NombresDeHojas = []
        ListaHojas = []
        for ncol, columna1 in enumerate(WB.sheet_by_index(0).row_values(0, 0, NumeroColFinal + 1)):
            columna = self.atexto(columna1)
            if len(columna) == 0:
                columna = str('Parameter' + str(ncol + 1))
                print('Beware! There is no good header on page: ' + str(1) + ' error 1')
                print(columna + ' has been set')

            NombresDeHojas.append(columna)
            nc = NombresDeHojas.count(columna)
            columna = columna if nc == 1 else columna + str(nc)

            Hoja = wbFiltro.add_sheet(columna)
            Pim = WB.sheet_by_index(0).row_values(0, 0, NumeroColFinal + 1)
            Hoja.write(0, 0, Pim[0], style=style2)
            for i in range(0, len(ReferenciasUnicas)):
                Hoja.write(i + 1, 0, ReferenciasUnicas[i], style=style1)
            if ncol != 0:
                for npag, pagina in enumerate(WB.sheets()):
                    ReferenciaValor = {}
                    ColLimit = WB.sheet_by_index(npag).ncols
                    for nrow, fila1 in enumerate(WB.sheet_by_name(pagina.name).col_values(0, 1)):
                        Ref = self.atexto(fila1)
                        Val = xlrd.sheet.Cell
                        if ncol < ColLimit:
                            Val = pagina.cell(nrow + 1, ncol)
                        else:
                            Val.value = 0
                        if Val.value != 0 or Val.value != 0.0:
                            Val.value = self.atexto(Val.value)
                            if Ref not in ReferenciaValor:
                                ReferenciaValor[Ref] = Val.value
                            else:
                                try:
                                    if Val.value not in ReferenciaValor[Ref]:
                                        ReferenciaValor[Ref].append(Val.value)
                                except:
                                    if Val.value != ReferenciaValor[Ref]:
                                        ReferenciaValor[Ref] = [ReferenciaValor[Ref], Val.value]

                    del Val.value, Val

                    for j in range(0, len(ReferenciaValor)):
                        try:
                            Referencia = list(ReferenciaValor.keys())
                            Refer = Referencia[j]
                            Posicion = ReferenciasUnicas.index(Refer)
                            Vale = ReferenciaValor[Refer]
                            Hoja.write(Posicion + 1, npag + 1, str(Vale))
                        except Exception as e:
                            print('Error found: ' + str(e) + '. Type: ' + str(type(e)))

                    Hoja.write(0, npag + 1, pagina.name, style=style2)
                print('We have made the parameter ' + str(columna) + '. Remain:' + str(NumeroColFinal - ncol))

        print('The filter by parameters has been completed, we proceed to the union of these parameters in order')
        wbFiltro.save('ReducedDataOld.xls')
        pyexcel.save_book_as(file_name='ReducedDataOld.xls',
                       dest_file_name='ReducedData.xlsx')
    def jerarquia(self, dflistado, nombrepagina):
        for i, lista in enumerate(dflistado):
            if len(lista) == 0:
                del lista
                continue
            if i == 0:
                listaCabecero = nombrepagina
                df = pd.DataFrame(listaCabecero).T
            else:
                Referencia = [lista[0]]
                for dato in lista[1:]:
                    if len(str(dato)) != 0:
                        Referencia.append(dato)
                        break
                if len(Referencia) == 1:
                    Referencia.append('')
                filaDataFrame = pd.DataFrame(Referencia).T
                df = pd.concat([df, filaDataFrame], axis=0, ignore_index=True)
                del Referencia
        return df
    def asignarParametros(self):
        WB = pd.read_excel('ReducedData.xlsx', sheet_name=None)
        os.remove('ReducedData.xlsx')
        wbOrdenado = pd.ExcelWriter('RDF_Limpio.xlsx')
        dfConjunto = pd.DataFrame()
        for j, pagina in enumerate(WB):
            if j != 0:
                pd.options.display.max_columns = None
                dfEntrada = WB[pagina]
                parametro = pagina
                columnas = list(dfEntrada)
                ordenColumnas = list(range(0, len(columnas)))
                columnasOrdenadas = pd.DataFrame(columnas, ordenColumnas).T
                # dfOrden = dfEntrada
                print('Las columnas para el parametro: ', parametro, ' siguen este orden: ')
                print(columnasOrdenadas)
                ordenNuevo = []
                while True:
                    entrada = input('Selecciona el orden nuevo numero a numero ')
                    if entrada.strip():  # si contiene algo es True, de lo contrario False
                        entrada1 = entrada
                        ordenNuevo.append(entrada1)  # agregamos en caso contenga algo
                    else:
                        break  # detenemos el ciclo for
                dfOrdenado = pd.DataFrame(dfEntrada[columnas[0]])
                for i in ordenNuevo:
                    nombrecolumna = columnas[int(i)]
                    columna = dfEntrada.pop(nombrecolumna)
                    dfOrdenado = pd.concat([dfOrdenado, columna], axis=1, ignore_index=True)
                dfOrdenado.to_excel(wbOrdenado, sheet_name=pagina, index=False)
                # Sacamos valores de este dataFrame nuevo ordenado
                dfOrdenadoListado = self.quitarnan_listas(dfOrdenado)  # meto dataframe con Nan y saco listas sin nan
                nombreParametro = [columnas[0], parametro]
                # modulo de jerarquia
                dfFiltradoOrdenado = self.jerarquia(dfOrdenadoListado, nombreParametro)
                dfConjunto = pd.concat([dfConjunto, dfFiltradoOrdenado], axis=1, ignore_index=True)
        dfConjunto.to_excel(wbOrdenado, sheet_name='Data Reunited', index=False)
        wbOrdenado.save()


    def inicio(self):
        values = self.setupLayout()
        #Obtencion de todas las alternativas
        df3 = self.crearDataframeConReferencias(values)   #Lo quito para ahorrar tiempo
        # df3 = pd.DataFrame()
        df3.to_excel(self.wbAlternates1, sheet_name='alternates_todas', index=False)

        #Filtrado de Datos
        self.filtro(values)
        self.asignarParametros()


    wb2 = pd.ExcelWriter('DatosPorSeparadoAlternates.xlsx')
    wbAlternates1 = pd.ExcelWriter('Todas_las_Alternativas.xlsx')

pepe = pepito()     #Inicializacion de clase, entran variables
Solucion = pepe.inicio()
pepe.wb2.save()
pepe.wbAlternates1.save()
