from cities import *
import pytest

# Not essential
def test_read_cities():
    assert read_cities("test-dummy.txt") == [('Ishikawa', 'Kanazawa', 36.5613, 136.656205),
                                             ('Kanagawa', 'Yokohama', 35.906487, 139.6380),
                                             ('Hokkaido', 'Sapporo', 43.0621, 141.3544),
                                             ('Okinawa', 'Naha', 26.2123, 127.6792),
                                             ('Kyoto', 'Kyoto', 35.0116, 135.7680),
                                             ('Fukuoka', 'Fukuoka', 33.5904, 130.4017)]
    
    assert read_cities("test-dummy.txt") != [('Alabama', 'Montgomery', 32.361538, -86.279118),
                                             ('Alaska', 'Juneau', 58.301935, -134.41974),
                                             ('Arizona', 'Phoenix', 33.448457, -112.073844),
                                             ('Arkansas', 'Little Rock', 34.736009, -92.331122),
                                             ('California', 'Sacramento', 38.555605, -121.468926),
                                             ('Colorado', 'Denver', 39.7391667, -104.984167),
                                             ('Connecticut', 'Hartford', 41.767, -72.677),
                                             ('Delaware', 'Dover', 39.161921, -75.526755),
                                             ('Florida', 'Tallahassee', 30.4518, -84.27277),
                                             ('Georgia', 'Atlanta', 33.76, -84.39),
                                             ('Hawaii', 'Honolulu', 21.30895, -157.826182),
                                             ('Idaho', 'Boise', 43.613739, -116.237651),
                                             ('Illinois', 'Springfield', 39.78325, -89.650373),
                                             ('Indiana', 'Indianapolis', 39.790942, -86.147685),
                                             ('Iowa', 'Des Moines', 41.590939, -93.620866),
                                             ('Kansas', 'Topeka', 39.04, -95.69),
                                             ('Kentucky', 'Frankfort', 38.197274, -84.86311),
                                             ('Louisiana', 'Baton Rouge', 30.45809, -91.140229),
                                             ('Maine', 'Augusta', 44.323535, -69.765261),
                                             ('Maryland', 'Annapolis', 38.972945, -76.501157),
                                             ('Massachusetts', 'Boston', 42.2352, -71.0275),
                                             ('Michigan', 'Lansing', 42.7335, -84.5467),
                                             ('Wyoming', 'Cheyenne', 41.145548, -104.802042)]
    assert type(read_cities("test-dummy.txt")) is list

def test_compute_total_distance():
    data = read_cities("test-dummy.txt")
    assert compute_total_distance(data) == pytest.approx(3573.21394857)
    assert type(compute_total_distance(data)) is float

def test_swap_adjacent_cities():
    # Test to see if adjacent indexes swap
    data = read_cities("test-dummy.txt")
    assert swap_adjacent_cities(data, 0) == pytest.approx(([('Kanagawa', 'Yokohama', 35.906487, 139.6380),
                                             ('Ishikawa', 'Kanazawa', 36.5613, 136.656205),
                                             ('Hokkaido', 'Sapporo', 43.0621, 141.3544),
                                             ('Okinawa', 'Naha', 26.2123, 127.6792),
                                             ('Kyoto', 'Kyoto', 35.0116, 135.7680),
                                             ('Fukuoka', 'Fukuoka', 33.5904, 130.4017)], 3723.04738))
    assert type(swap_adjacent_cities(data, 0)) is tuple

def test_swap_adjacent_cities2():
    # Test to see if last and first indexes swap
    data = read_cities("test-dummy.txt")    
    assert swap_adjacent_cities(data, len(data)-1) == pytest.approx(([('Fukuoka', 'Fukuoka', 33.5904, 130.4017),
                                             ('Kanagawa', 'Yokohama', 35.906487, 139.6380),
                                             ('Hokkaido', 'Sapporo', 43.0621, 141.3544),
                                             ('Okinawa', 'Naha', 26.2123, 127.6792),
                                             ('Kyoto', 'Kyoto', 35.0116, 135.7680),
                                             ('Ishikawa', 'Kanazawa', 36.5613, 136.656205)], 3745.329178))
    assert type(swap_adjacent_cities(data, len(data)-1)) is tuple 

def test_swap_cities():
    data = read_cities("test-dummy.txt")
    assert swap_cities(data, 0, 2) == pytest.approx(([('Hokkaido', 'Sapporo', 43.0621, 141.3544),
                                             ('Kanagawa', 'Yokohama', 35.906487, 139.6380),
                                             ('Ishikawa', 'Kanazawa', 36.5613, 136.656205),
                                             ('Okinawa', 'Naha', 26.2123, 127.6792),
                                             ('Kyoto', 'Kyoto', 35.0116, 135.7680),
                                             ('Fukuoka', 'Fukuoka', 33.5904, 130.4017)], 3539.48531))
    assert type(swap_cities(data, 0, 2)) is tuple 

    # Test to see if the same indexes give the same output
    data = read_cities("test-dummy.txt")
    assert swap_cities(data, 0, 0) == pytest.approx(([('Ishikawa', 'Kanazawa', 36.5613, 136.656205),
                                             ('Kanagawa', 'Yokohama', 35.906487, 139.6380),
                                             ('Hokkaido', 'Sapporo', 43.0621, 141.3544),
                                             ('Okinawa', 'Naha', 26.2123, 127.6792),
                                             ('Kyoto', 'Kyoto', 35.0116, 135.7680),
                                             ('Fukuoka', 'Fukuoka', 33.5904, 130.4017)], 3573.21394857))                                            
    assert type(swap_cities(data, 0, 0)) is tuple 

def test_find_best_cycle():
    data = read_cities("test-dummy.txt")
    assert compute_total_distance(find_best_cycle(data)) <= compute_total_distance(data)
    assert type(find_best_cycle(data)) is list

def test_circle_route_northsouth():
    data = read_cities("test-dummy.txt")
    assert len(circle_route_northsouth(data)) == len(data)
    assert circle_route_northsouth(data) == [('Okinawa', 'Naha', 26.2123, 127.6792),
                                              ('Fukuoka', 'Fukuoka', 33.5904, 130.4017),
                                              ('Kyoto', 'Kyoto', 35.0116, 135.768),
                                              ('Hokkaido', 'Sapporo', 43.0621, 141.3544),
                                              ('Ishikawa', 'Kanazawa', 36.5613, 136.656205),
                                              ('Kanagawa', 'Yokohama', 35.906487, 139.638)]
    assert type(circle_route_northsouth(data)) is list 

def test_circle_route_eastwest():
    data = read_cities("test-dummy.txt")
    assert len(circle_route_eastwest(data)) == len(data)
    assert circle_route_eastwest(data) == [('Okinawa', 'Naha', 26.2123, 127.6792),
                                              ('Fukuoka', 'Fukuoka', 33.5904, 130.4017),
                                              ('Kyoto', 'Kyoto', 35.0116, 135.768),
                                              ('Hokkaido', 'Sapporo', 43.0621, 141.3544),
                                              ('Kanagawa', 'Yokohama', 35.906487, 139.638),
                                              ('Ishikawa', 'Kanazawa', 36.5613, 136.656205)]
    assert type(circle_route_eastwest(data)) is list 

def test_best_route():
    data = read_cities("test-dummy.txt")
    assert compute_total_distance(best_route(data)) <= compute_total_distance(read_cities("test-dummy.txt"))
    assert type(best_route(data)) is list

def insert_cities():
    data = read_cities("test-dummy.txt")
    assert insert_cities(data, 0, 0) == pytest.approx(([('Ishikawa', 'Kanazawa', 36.5613, 136.656205),
                                             ('Kanagawa', 'Yokohama', 35.906487, 139.6380),
                                             ('Hokkaido', 'Sapporo', 43.0621, 141.3544),
                                             ('Okinawa', 'Naha', 26.2123, 127.6792),
                                             ('Kyoto', 'Kyoto', 35.0116, 135.7680),
                                             ('Fukuoka', 'Fukuoka', 33.5904, 130.4017)], 3573.21394857))
    assert insert_cities(data, 0, 3) == pytest.approx(([('Kanagawa', 'Yokohama', 35.906487, 139.6380),
                                             ('Hokkaido', 'Sapporo', 43.0621, 141.3544),
                                             ('Ishikawa', 'Kanazawa', 36.5613, 136.656205),
                                             ('Okinawa', 'Naha', 26.2123, 127.6792),
                                             ('Kyoto', 'Kyoto', 35.0116, 135.7680),
                                             ('Fukuoka', 'Fukuoka', 33.5904, 130.4017)], 3546.7099438546193))
    assert insert_cities(data, 3, 0) == pytest.approx(([('Okinawa', 'Naha', 26.2123, 127.6792),
                                             ('Ishikawa', 'Kanazawa', 36.5613, 136.656205),
                                             ('Kanagawa', 'Yokohama', 35.906487, 139.6380),
                                             ('Hokkaido', 'Sapporo', 43.0621, 141.3544),
                                             ('Kyoto', 'Kyoto', 35.0116, 135.7680),
                                             ('Fukuoka', 'Fukuoka', 33.5904, 130.4017)], 3049.888463401265))
