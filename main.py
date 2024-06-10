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

ciudad1 = 'Lima'
pais1 = 'Peru'
ciudad2 = 'Bogota'
pais2 = 'Colombia'

distancia1 = obtener_distancia(ciudad1, pais1, ciudad2, pais2, metodo='csv')

if distancia1 is not None:
    print(f"La distancia entre {ciudad1} y {ciudad2} es de {distancia1:.2f} km.")
