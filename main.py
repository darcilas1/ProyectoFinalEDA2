import sys
import random
from PyQt5 import QtWidgets, QtGui, QtCore
from grafos_ui import Ui_MainWindow
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QGraphicsItem


class Nodo(QGraphicsEllipseItem):
    def __init__(self, x, y, radius, id, app):
        super().__init__(-radius, -radius, 2 * radius, 2 * radius)
        self.setBrush(QtGui.QBrush(QtGui.QColor("lightblue")))
        self.setPen(QtGui.QPen(QtCore.Qt.black))
        self.id = id
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemSendsGeometryChanges)
        self.text_item = QGraphicsTextItem(f"Nodo {self.id}", self)
        self.text_item.setPos(-10, -10)
        self.app = app
        self.aristas = []

    def agregar_arista(self, arista):
        self.aristas.append(arista)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            for arista in self.aristas:
                arista.actualizar_posiciones()
        return super().itemChange(change, value)


class Arista(QGraphicsLineItem):
    def __init__(self, nodo1, nodo2, peso, scene):
        super().__init__()
        self.nodo1 = nodo1
        self.nodo2 = nodo2
        self.peso = peso
        self.scene = scene
        self.text_item = QGraphicsTextItem(str(self.peso))
        self.scene.addItem(self.text_item)
        self.actualizar_posiciones()
        self.setFlag(QGraphicsLineItem.ItemIsSelectable)
        self.setPen(QtGui.QPen(QtCore.Qt.black))

    def actualizar_posiciones(self):
        x1, y1 = self.nodo1.scenePos().x(), self.nodo1.scenePos().y()
        x2, y2 = self.nodo2.scenePos().x(), self.nodo2.scenePos().y()
        self.setLine(x1, y1, x2, y2)
        self.text_item.setPos((x1 + x2) / 2, (y1 + y2) / 2)

    def mousePressEvent(self, event):
        self.setPen(QtGui.QPen(QtCore.Qt.red, 3))
        self.nodo1.setPen(QtGui.QPen(QtCore.Qt.red, 3))
        self.nodo2.setPen(QtGui.QPen(QtCore.Qt.red, 3))
        super().mousePressEvent(event)


class GrafoApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(GrafoApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Conectar los botones a sus funciones
        self.graphicsView = self.ui.graphicsView
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        try:
            # Conectar el evento del clic en el encabezado de la tabla para generar pesos aleatorios
            self.ui.tableWidget.horizontalHeader().sectionClicked.connect(self.llenar_matriz_aleatoria)

            # Conectar el botón de pintar grafo
            self.ui.btnPintarGrafo.clicked.connect(self.dibujar_grafo)

            # Otros botones para generar matrices de adyacencia, k^2 y k^3
            self.ui.btnGenerarAdy.clicked.connect(self.generar_adyacencia)
            self.ui.btnGenerark2.clicked.connect(self.generar_k2)
            self.ui.btnGenerark3.clicked.connect(self.generar_k3)
            print("Botones conectados correctamente.")
        except AttributeError as e:
            print(f"Error al conectar botones: {e}")

        self.nodos = []
        self.aristas = []

    def llenar_matriz_aleatoria(self):
        """Llena la matriz (tableWidget) con valores aleatorios cuando se hace clic en los encabezados de las columnas"""
        try:
            filas = self.ui.tableWidget.rowCount()
            columnas = self.ui.tableWidget.columnCount()

            # Generar valores aleatorios para cada celda de la tabla
            for i in range(filas):
                for j in range(columnas):
                    if i == j:
                        # No crear aristas a sí mismo (diagonal)
                        self.ui.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem('0'))
                    else:
                        # Valores aleatorios entre 1 y 100 para las conexiones
                        valor_aleatorio = random.randint(1, 100)
                        self.ui.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(valor_aleatorio)))
            print("Matriz de pesos aleatorios generada.")
        except Exception as e:
            print(f"Error al llenar la matriz de pesos aleatorios: {e}")

    def dibujar_grafo(self):
        try:
            self.scene.clear()
            self.nodos.clear()
            self.aristas.clear()
            matriz = self.obtener_matriz()
            self.dibujar_nodos_y_aristas(matriz)
        except Exception as e:
            print(f"Error al dibujar el grafo: {e}")

    def obtener_matriz(self):
        try:
            filas = self.ui.tableWidget.rowCount()
            columnas = self.ui.tableWidget.columnCount()
            matriz = []
            for i in range(filas):
                fila = []
                for j in range(columnas):
                    item = self.ui.tableWidget.item(i, j)
                    valor = int(item.text()) if item and item.text().isdigit() else 0
                    fila.append(valor)
                matriz.append(fila)
            return matriz
        except Exception as e:
            print(f"Error al obtener la matriz: {e}")
            return []

    def dibujar_nodos_y_aristas(self, matriz):
        try:
            num_nodos = len(matriz)
            radius = 20
            width = self.graphicsView.width() - 100
            height = self.graphicsView.height() - 100

            for i in range(num_nodos):
                x = random.randint(50, width)
                y = random.randint(50, height)
                nodo = Nodo(x, y, radius, i + 1, self)
                nodo.setPos(x, y)
                self.scene.addItem(nodo)
                self.nodos.append(nodo)

            for i in range(num_nodos):
                for j in range(i + 1, num_nodos):
                    peso = matriz[i][j]
                    if peso > 0:
                        nodo1 = self.nodos[i]
                        nodo2 = self.nodos[j]
                        arista = Arista(nodo1, nodo2, peso, self.scene)
                        self.aristas.append(arista)
                        self.scene.addItem(arista)
                        nodo1.agregar_arista(arista)
                        nodo2.agregar_arista(arista)
            print("Nodos y aristas dibujados.")
        except Exception as e:
            print(f"Error al dibujar nodos y aristas: {e}")

    def generar_adyacencia(self):
        try:
            matriz = self.obtener_matriz()
            filas = len(matriz)
            columnas = len(matriz[0])
            self.ui.tableWidget_2.setRowCount(filas)
            self.ui.tableWidget_2.setColumnCount(columnas)
            for i in range(filas):
                for j in range(columnas):
                    valor = 1 if matriz[i][j] > 0 else 0
                    self.ui.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(valor)))
            print("Matriz de adyacencia generada.")
        except Exception as e:
            print(f"Error al generar matriz de adyacencia: {e}")

    def generar_k2(self):
        try:
            matriz = self.obtener_matriz()
            filas = len(matriz)
            columnas = len(matriz[0])
            k2 = [[0] * columnas for _ in range(filas)]
            for i in range(filas):
                for j in range(columnas):
                    suma = 0
                    for k in range(filas):
                        suma += matriz[i][k] * matriz[k][j]
                    k2[i][j] = suma
            self.ui.tableWidget_3.setRowCount(filas)
            self.ui.tableWidget_3.setColumnCount(columnas)
            for i in range(filas):
                for j in range(columnas):
                    self.ui.tableWidget_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(k2[i][j])))
            print("Matriz k^2 generada.")
        except Exception as e:
            print(f"Error al generar matriz k^2: {e}")

    def generar_k3(self):
        try:
            matriz = self.obtener_matriz()
            filas = len(matriz)
            columnas = len(matriz[0])
            k3 = [[0] * columnas for _ in range(filas)]
            for i in range(filas):
                for j in range(columnas):
                    suma = 0
                    for k in range(filas):
                        for l in range(filas):
                            suma += matriz[i][k] * matriz[k][l] * matriz[l][j]
                    k3[i][j] = suma
            self.ui.tableWidget_4.setRowCount(filas)
            self.ui.tableWidget_4.setColumnCount(columnas)
            for i in range(filas):
                for j in range(columnas):
                    self.ui.tableWidget_4.setItem(i, j, QtWidgets.QTableWidgetItem(str(k3[i][j])))
            print("Matriz k^3 generada.")
        except Exception as e:
            print(f"Error al generar matriz k^3: {e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GrafoApp()
    window.show()
    sys.exit(app.exec_())
