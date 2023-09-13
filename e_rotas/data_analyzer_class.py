import numpy as np


class DataAnalyzer:

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # raio da Terra em quilômetros
        dlat = np.radians(lat2 - lat1)
        dlon = np.radians(lon2 - lon1)
        a = (np.sin(dlat / 2) * np.sin(dlat / 2) +
             np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) *
             np.sin(dlon / 2) * np.sin(dlon / 2))
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        distance = R * c
        return distance
