import csv
from math import radians, cos, sin, asin, sqrt

class CoordinateConverter: # класс преобразования координат
    @staticmethod # объявление метода статическим (метод принадлежит классу, а не экземпляру)
    def dms_to_dd(d, m, s):
        '''Преобразует координаты из градусов, минут и секунд (DMS) в десятичные градусы (DD).
        Параметры:
        d (int): Градусы
        m (int): Минуты
        s (float): Секунды
        Возвращает:
        float: значение в десятичных градусах '''
        return d + m / 60 + s / 3600

    @staticmethod # объявление метода статическим
    def dd_to_dms(dd):
        '''Преобразует координаты из десятичных градусов в градусы, минуты и секунды.'''
        d = int(dd)
        minfloat = abs(dd - d) * 60
        m = int(minfloat)
        s = (minfloat - m) * 60
        return (d, m, s)

class DistanceCalculator: # класс вычисления расстояния между двумя точками
    @staticmethod
    def haversine(lon1, lat1, lon2, lat2):
        '''Основываясь на формуле гаверсинуса функция вычисляет расстояние
        между двумя точками на земной поверхности, заданными их широтой и долготой.'''
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 3959 # радиус Земли в милях
        return c * r

class ZipCodeDatabase: # класс для работы с базой данных почтовых индексов
    def __init__(self, filename):
        '''Инициализация базы данных почтовых индексов из файла.'''
        self.zipcode_database = self.load_zipcode_database(filename)

    def load_zipcode_database(self, filename):
        '''Метод для чтения данных из CSV-файла и преобразования их в словарь.
        Ключ - почтовый индекс, значения - кортеж с данными о местоположении.'''
        with open(filename, mode='r') as infile:
            reader = csv.reader(infile)
            next(reader, None)
            return {rows[0]: (rows[1], rows[2], rows[3], rows[4], rows[5]) for rows in reader}

    def find_location_by_zip(self, zipcode):
        '''Метод для поиска местоположения по заданному почтовому индексу'''
        if zipcode in self.zipcode_database:
            location_data = self.zipcode_database[zipcode]
            lat_dms = CoordinateConverter.dd_to_dms(float(location_data[0]))
            lon_dms = CoordinateConverter.dd_to_dms(float(location_data[1]))
            return f"ZIP Code {zipcode} is in {location_data[2]}, {location_data[3]}, {location_data[4]} county, coordinates: ({lat_dms[0]}°{lat_dms[1]}'{lat_dms[2]}\"N, {lon_dms[0]}°{lon_dms[1]}'{lon_dms[2]}\"W)."
        else:
            return "Zipcode not found."

    def find_zip_by_city_and_state(self, city, state):
        '''Метод для поиска всех почтовых индексов, соответствующих заданному городу и штату'''
        zipcodes = []
        for zipcode, details in self.zipcode_database.items():
            if details[2].lower() == city.lower() and details[3].lower() == state.lower():
                zipcodes.append(zipcode)
        return zipcodes if zipcodes else "City or state not found."

    def calculate_distance_by_zip(self, zipcode1, zipcode2):
        '''Метод для расчёта расстояния между двумя почтовыми индексами'''
        if zipcode1 in self.zipcode_database and zipcode2 in self.zipcode_database:
            lat1, lon1 = map(float, self.zipcode_database[zipcode1][:2])
            lat2, lon2 = map(float, self.zipcode_database[zipcode2][:2])
            return DistanceCalculator.haversine(lon1, lat1, lon2, lat2)
        else:
            return "The distance between the zip codes cannot be determined."

def main():
    database = ZipCodeDatabase('.\\data\\zip_codes_states.csv')  # экземпляр класса с базой данных
    while True:
        command = input("Enter command ('loc', 'zip', 'dist', 'end'): ").lower()
        if command == 'end':
            print("Done")
            break
        elif command == 'loc':
            zipcode = input("Enter a ZIP Code to lookup: ")
            print(database.find_location_by_zip(zipcode))  # метод экземпляра класса
        elif command == 'zip':
            city = input("Enter a city name to lookup: ")
            state = input("Enter a state name to lookup: ")
            zip_codes_found = database.find_zip_by_city_and_state(city, state)  # метод экземпляра класса
            print(f"The following ZIP Code(s) found for {city}, {state}: {', '.join(zip_codes_found)}")
        elif command == 'dist':
            zipcode1 = input("Enter the first ZIP Code: ")
            zipcode2 = input("Enter the second ZIP Code: ")
            print(f"Distance between {zipcode1} and {zipcode2}: {database.calculate_distance_by_zip(zipcode1, zipcode2)} miles")  # Используем методы экземпляра класса
        else:
            print(f"Invalid command, ignoring. ")

if __name__ == "__main__":
    main()
    # файл запущен как основная программа