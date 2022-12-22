import math

class Rastreador:

    def __init__(self):
        self.centro_puntos = {}
        self.id_count = 1

    def rastreo(self, objetos):
        objetos_id = []

        for rect in objetos:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            #Miramos si ees objeto ya fue detectado
            objetos_det = False
            for id, pt in self.centro_puntos.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 25:
                    self.centro_puntos[id] = (cx, cy)
                    objetos_id.append([x, y, w, h, id])
                    objetos_det = True
                    break
            if objetos_det is False:
                self.centro_puntos[self.id_count] = (cx, cy) #Almacenamos la coordenada en x
                objetos_id.append([x, y, w , h, self.id_count]) #Agregamos el objeto con su ID
                self.id_count = self.id_count + 1 #Aumentamos el ID
        # Limpiar la lista por puntos centrales para eliminar IDS que ya no se usan
        new_center_points = {}
        for obj_bb_id in objetos_id:
            _, _, _, _, object_id = obj_bb_id
            center = self.centro_puntos[object_id]
            new_center_points[object_id] = center

        #Actualizar la lista con los ID no utilizados eliminados
        self.centro_puntos = new_center_points.copy()
        return objetos_id
