import csv
import requests
from math import radians, sin, cos, sqrt, atan2
class Coordenada:
    def __init__(self, latitud, longitud):
        self.latitud = latitud
        self.longitud = longitud
class Ciudad:
    def __init__(self, nombre_ciudad, nombre_pais):
        self.nombre_ciudad = nombre_ciudad
        self.nombre_pais = nombre_pais
def obtenerCoordenadasCSV(ciudad, pais, archivo_csv='worldcities.csv'):
    try:
        with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['city_ascii'].strip().lower() == ciudad.strip().lower() and row['country'].strip().lower() == pais.strip().lower():
                    return Coordenada(float(row['lat']), float(row['lng']))
    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo_csv}")
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
    return None
def obtenerCoordenadasAPI(ciudad, pais):
    try:
        url = f'https://nominatim.openstreetmap.org/search?q={ciudad},{pais}&format=json'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data and 'lat' in data[0] and 'lon' in data[0]:
                latitud = float(data[0]['lat'])
                longitud = float(data[0]['lon'])
                return Coordenada(latitud, longitud)
            else:
                print(f"No se encontraron coordenadas en la respuesta para {ciudad}, {pais}.")
        else:
            print(f"Error en la llamada a la API: {response.status_code}")
    except Exception as e:
        print(f"Error al llamar a la API: {e}")
    return None
def obtenerCoordenadasMOCK(ciudad, pais):
    coordenadas_fijas = {
        ('lima', 'peru'): Coordenada(-12.0464, -77.0428),
        ('paris', 'france'): Coordenada(48.8566, 2.3522),
        ('tokyo', 'japan'): Coordenada(35.6897, 139.6922),
        ('jakarta', 'indonesia'): Coordenada(-6.1750, 106.8275),
        ('delhi', 'india'): Coordenada(28.6100, 77.2300),
        ('bogota', 'colombia'): Coordenada(4.7110, -74.0721),
    }
    key = (ciudad.lower(), pais.lower())
    return coordenadas_fijas.get(key, None)
def distanciaHaversine(coord1, coord2):
    R = 6371.0  
    lat1, lon1 = radians(coord1.latitud), radians(coord1.longitud)
    lat2, lon2 = radians(coord2.latitud), radians(coord2.longitud)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distancia = R * c
    return distancia
def obtener_distancia(ciudad1, pais1, ciudad2, pais2, metodo='csv'):
    if metodo == 'csv':
        coord1 = obtenerCoordenadasCSV(ciudad1, pais1)
        coord2 = obtenerCoordenadasCSV(ciudad2, pais2)
    elif metodo == 'api':
        coord1 = obtenerCoordenadasAPI(ciudad1, pais1)
        coord2 = obtenerCoordenadasAPI(ciudad2, pais2)
    elif metodo == 'mock':
        coord1 = obtenerCoordenadasMOCK(ciudad1, pais1)
        coord2 = obtenerCoordenadasMOCK(ciudad2, pais2)
    else:
        raise ValueError("Método no soportado.")
    if coord1 and coord2:
        return distanciaHaversine(coord1, coord2)
    else:
        print("No se pudieron obtener las coordenadas de una o ambas ciudades.")
        return None
def CiudadesMasCercanas (ciudad1, pais1, ciudad2, pais2,ciudad3, pais3, metodo='csv'):

    if ciudad1 == ciudad2 or ciudad1 == ciudad3 or ciudad2 == ciudad3:
        return ciudad1 + " con " + ciudad2 + " tienen la mínima distancia de 0"

    if metodo == 'csv':
        coord1 = obtenerCoordenadasCSV(ciudad1, pais1)
        coord2 = obtenerCoordenadasCSV(ciudad2, pais2)
        coord3 = obtenerCoordenadasCSV(ciudad3, pais3)
    elif metodo == 'api':
        coord1 = obtenerCoordenadasAPI(ciudad1, pais1)
        coord2 = obtenerCoordenadasAPI(ciudad2, pais2)
        coord3 = obtenerCoordenadasCSV(ciudad3, pais3)
    elif metodo == 'mock':
        coord1 = obtenerCoordenadasMOCK(ciudad1, pais1)
        coord2 = obtenerCoordenadasMOCK(ciudad2, pais2)
        coord3 = obtenerCoordenadasCSV(ciudad3, pais3)
    else:
        raise ValueError("Método no soportado.")
    if coord1 and coord2 and coord3:
        coord1_2=distanciaHaversine(coord1, coord2)
        coord1_3=distanciaHaversine(coord1, coord3)
        coord2_3=distanciaHaversine(coord2, coord3)
        if coord1_2<coord1_3 and coord1_2<coord2_3:
            menor_distancia=coord1_2
            ciudades_con_menor_distancia=ciudad1+ " con "+ciudad2+ "tienen la mínima distancia de "+ str(menor_distancia)
            ciudades_con_menor_distancia=ciudad1+ " con "+ciudad2+ " tienen la mínima distancia de "+ str(menor_distancia)

            return ciudades_con_menor_distancia
        elif coord1_3<coord1_2 and coord1_3<coord2_3:
            menor_distancia=coord1_3
            ciudades_con_menor_distancia=ciudad1+" con "+ciudad3 + "tienen la mínima distancia de "+ str(menor_distancia)
            ciudades_con_menor_distancia=ciudad1+" con "+ciudad3 + " tienen la mínima distancia de "+ str(menor_distancia)

            return ciudades_con_menor_distancia
        else:
            menor_distancia=coord2_3
            ciudades_con_menor_distancia=ciudad2+" con "+ciudad3 +"tienen la mínima distancia de "+ str(menor_distancia)
            ciudades_con_menor_distancia=ciudad2+" con "+ciudad3 +" tienen la mínima distancia de "+ str(menor_distancia)
            return ciudades_con_menor_distancia
    else:
        print("No se pudieron obtener las coordenadas de una o ambas ciudades.")
        return None


def test_Conection():
    ConnectionError = False
    if(ConnectionError):
        raise ConnectionError("Prueba de conexión falló: Error de conexión")


def testData(ciudad1, pais1, ciudad2, pais2, ciudad3, pais3, metodo):
    if (metodo=="csv"):
        ciudad1_exits=obtenerCoordenadasCSV(ciudad1, pais1)
        ciudad2_exits=obtenerCoordenadasCSV(ciudad2, pais2)
        ciudad3_exits=obtenerCoordenadasCSV(ciudad3, pais3)
    elif (metodo=="api"):
        ciudad1_exits=obtenerCoordenadasAPI(ciudad1, pais1)
        ciudad2_exits=obtenerCoordenadasAPI(ciudad2, pais2)
        ciudad3_exits=obtenerCoordenadasAPI(ciudad3, pais3)

    elif (metodo=="mock"):
        ciudad1_exits=obtenerCoordenadasMOCK(ciudad1, pais1)
        ciudad2_exits=obtenerCoordenadasMOCK(ciudad2, pais2)
        ciudad3_exits=obtenerCoordenadasMOCK(ciudad3, pais3)
    
    value_return=True
    if(ciudad1_exits is None):
        raise ValueError("No se encontró la ciudad 1/pais 1")
        value_return=False

    if(ciudad2_exits is None):
        raise ValueError("No se encontró la ciudad 2/pais2")
        value_return=False
    if(ciudad3_exits is None):
        raise ValueError("No se encontró la ciudad 3/pais 3")
        value_return=False
    
    if (value_return!=False):
        return True
    #En obtenerCoordenadas mandamos un mensaje de error en el caso que la data no exista u ocurra un error

def testSteps():
    ciudad1=input("Ingrese la ciudad 1: ")
    pais1=input("Ingrese el país 1: ")
    ciudad2=input("Ingrese la ciudad 2: ")
    pais2=input("Ingrese el país 2: ")
    ciudad3=input("Ingrese la ciudad 3: ")
    pais3=input("Ingrese el país 3: ")
    metodo=input("Ingrese el método: ")

    #Si el test de Data funciona correctamente, se procede a obtener la distancia entre las ciudades
    if(testData(ciudad1, pais1, ciudad2, pais2, ciudad3, pais3, metodo)==True): 
        distancia2=CiudadesMasCercanas(ciudad1, pais1, ciudad2, pais2, ciudad3, pais3, metodo)
        if distancia2 is not None:
            print(distancia2)
        else:
            print("No se pudo obtener la distancia entre las ciudades")
    else:
        print("No se pudo obtener la data de las ciudades")

def testExpectedResult():
    test_Conection()
    testSteps() #Test steps llama a testData y a CiudadesMasCercanas para los resultados

testExpectedResult()