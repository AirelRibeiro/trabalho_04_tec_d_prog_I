import numpy as np


class DataAnalyzer:

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        raio_lat_terra = 6371
        d_latitude = np.radians(lat2 - lat1)
        d_longitude = np.radians(lon2 - lon1)
        a = (np.sin(d_latitude / 2) * np.sin(d_latitude / 2) +
             np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) *
             np.sin(d_longitude / 2) * np.sin(d_longitude / 2))
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        distance = raio_lat_terra * c
        return distance

    @staticmethod
    def nearest_neighbor(points):
        unvisited = set(
            range(1, len(points))
        )  # índices que representam os pontos não visitados
        current_point = 0
        route = [current_point]

        while unvisited:
            nearest = min(
                unvisited, key=lambda x: DataAnalyzer.haversine(points.iloc[current_point]['latitude'],
                                                                points.iloc[current_point]['longitude'],
                                                                points.iloc[x]['latitude'],
                                                                points.iloc[x]['longitude'])
            )
            route.append(nearest)
            unvisited.remove(nearest)
            current_point = nearest

        route.append(0)  # Volta ao ponto inicial para fechar o ciclo
        return route
