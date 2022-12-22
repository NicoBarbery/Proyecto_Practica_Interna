# Importenos Librerias
import cv2
import numpy as np
from Rastreador import *
import time

# vamos a crear un objeto de seguimiento
seguimiento = Rastreador()

# Realizamos la lectura del video
cap = cv2.VideoCapture("Autos3.mp4")

# Vamos a realizar una deteccion de objetos con camara estable
deteccion = cv2.createBackgroundSubtractorMOG2(history=10000, varThreshold=12)

#Listas para timpos
carI = {}
carO = {}
prueba = {}


while True:
    #Lectura de la video captura
    ret, frame = cap.read()
    #frame = cv2.resize(frame, (1280, 720))

    height = frame.shape[0]
    width = frame.shape[1]


    #zona = frame[530: 720, 300:850]
    #Creamos una mascara
    mask = np.zeros((height, width), dtype=np.uint8)
    # elegimos una zona de interes para contar el paso de autos
    pts = np.array([[[890, 751],[1073,732], [1382,971], [945,971]]])
    # Umbral de binarizacion
    #_, mascara = cv2.threshold(mascara, 254, 255, cv2.THRESH_BINARY)
    #contornos, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #detecciones = []  # Lista donde vamos a almacenar la info
    #Creamos el poligono con los puntos
    cv2.fillPoly(mask, pts, 255)
    #Elegimos lo q este fuera de los puntos
    zona = cv2.bitwise_and(frame, frame, mask=mask)

    #Mostramos con lineas la zona de interes
    areag = [(890,751), (1073,732),(1382,971), (945,971)]
    area3 = [(815,402), (1032,402),(1060,470), (766,470)]
    area1 = [(667,630), (1120,630),(1208,848), (506,848)]
    area2 = [(766,470), (1060,470),(1120,630), (667,630)]

    #dibujamos
    #area general
    #cv2.polylines(frame, [np.array(areag, np.int32)], True, (255, 255, 0), 2)
    # Area 3
    #cv2.polylines(frame, [np.array(area3, np.int32)], True, (0, 130, 255), 1)
    # Area 2
    #cv2.polylines(frame, [np.array(area2, np.int32)], True, (0, 0, 255), 1)
    # Area 1
    #cv2.polylines(frame, [np.array(area1, np.int32)], True, (0, 130, 255), 1)


    mascara = deteccion.apply(zona)

    filtro = cv2.GaussianBlur(mascara, (11, 11),0)

    _, umbral = cv2.threshold(mascara, 254, 255, cv2.THRESH_BINARY)

    dila = cv2.dilate(umbral, np.ones((3, 3)))

    # Creamos un Kernel (mascara)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # Aplicamos el kernel para juntar los pixeles dispersos
    cerrar = cv2.morphologyEx(dila, cv2.MORPH_CLOSE, kernel)

    contornos, _= cv2.findContours(cerrar, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detecciones = []

    #Dibujamos todos los contrornos en frame
    for cont in contornos:
        #Eliminamos los contornos pequeños pequeños
        area = cv2.contourArea(cont)
        if area > 1800:
            x, y, ancho, alto = cv2.boundingRect(cont)
            #cv2.rectangle(zona,(x,y), (x + ancho, y + alto), (255, 255, 0), 3)
            #Almacenamos la informacion de las detecciones
            detecciones.append([x, y, ancho, alto])

    info_id = seguimiento.rastreo(detecciones)

    for inf in info_id:
        x, y, ancho, alto, id = inf
        #cv2.putText(zona, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)
        cv2.rectangle(frame, (x, y - 10), (x+ancho, y+alto), (0, 0, 255), 2)

        cx = int(x + ancho / 2)
        cy = int(y + alto / 2)

        a2 = cv2.pointPolygonTest(np.array(area2, np.int32), (cx, cy), False)
        # Si esta en el area de la mitad
        if a2 >= 0:
            carI[id] = time.process_time()

        if id in carI:
            cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)

            a3 = cv2.pointPolygonTest(np.array(area3, np.int32), (cx, cy), False)

            if a3 >= 0:
                tiempo = time.process_time() - carI[id]

                if tiempo % 1 == 0:
                    tiempo = tiempo + 0.323
                if tiempo % 1 != 0:
                    tiempo = tiempo + 1.016
                if id not in carO:
                    carO[id] = tiempo
                if id in carO:
                    tiempo = carO[id]

                    vel = 14.3/carO[id]
                    vel = vel * 3.6
                cv2.rectangle(frame, (x,y - 10), (x+100,y-50),(0,0,255),-1)
                cv2.putText(frame, str(int(vel)) + " KM / H" , (x,y -35), cv2.FONT_HERSHEY_PLAIN, 1,(255,255,255), 2)
        cv2.putText(frame, str(id), (x,y-15), cv2.FONT_HERSHEY_PLAIN,1, (0,0,0), 2)

    cv2.imshow("Carretera", frame)

    #cv2.imshow("Mascara", zona)

    key = cv2.waitKey(5)
    if key == 27:
        break

cap.release()
cap.destroyAllWindows()