import tensorflow as tf 
import random
import copy
from earth_distance import distance
from matplotlib import pyplot as plt

def read_cities(file_name):
    """
    Read in the cities from the given `file_name`, and return 
    them as a list of four-tuples: 

      [(state, city, latitude, longitude), ...] 

    Use this as your initial `road_map`, that is, the cycle 

      Alabama -> Alaska -> Arizona -> ... -> Wyoming -> Alabama.
    """
    road_map = []
    stream = open(file_name,"r")
    content = stream.readlines()
    for entry in content:
        entry = entry.split("\t")
        # Turn the string numbers into float numbers
        entry[2], entry[3] = float(entry[2]), float(entry[3]) 
        road_map.append(tuple(entry))
    return road_map


def print_cities(road_map):
    """
    Prints a list of cities, along with their locations. 
    Prints only one or two digits after the decimal point.
    """
    for data in road_map:
        lat = ((data[2])//.01)/100 #latitude to 2 decimal places
        lon = ((data[3])//.01)/100 #longitude to 2 decimal places
        print(data[1]+"  Latitude:",lat, "Longitude:",lon)

    return None


def compute_total_distance(road_map):
    """
    Returns, as a floating point number, the sum of the distances of all 
    the connections in the `road_map`. Distances are calculated in miles.
    Distance function imported from earth_distance.py
    """
    
    total_dist = 0
    
    for location in range(len(road_map)):       
        dist = distance(road_map[location][2], road_map[location][3],
                            road_map[(location+1) % len(road_map)][2], 
                            road_map[(location+1) % len(road_map)][3])
        total_dist += dist
            
    return total_dist

def swap_adjacent_cities(road_map, index):
    """
    Take the city at location `index` in the `road_map`, and the city at 
    location `index+1` (or at `0`, if `index` refers to the last element 
    in the list), swap their positions in the `road_map`, compute the 
    new total distance, and return the tuple 

        (new_road_map, new_total_distance)
    """
    
    new_road_map = road_map

    new_road_map[index], new_road_map[(index+1) % len(new_road_map)] = \
      new_road_map[(index+1) % len(new_road_map)], new_road_map[index]

    new_total_distance = compute_total_distance(new_road_map)
    
    return (new_road_map, new_total_distance)

def swap_cities(road_map, index1, index2):
    """
    Take the city at location `index` in the `road_map`, and the 
    city at location `index2`, swap their positions in the `road_map`, 
    compute the new total distance, and return the tuple 

        (new_road_map, new_total_distance)

    Allow for the possibility that `index1=index2`,
    and handle this case correctly.
    """
    
    new_road_map = road_map

    if index1 != index2:
        new_road_map[index1], new_road_map[index2] = \
        new_road_map[index2], new_road_map[index1]      

    new_total_distance = compute_total_distance(new_road_map)

    return (new_road_map, new_total_distance)

def insert_cities(road_map, old_index, new_index):
    """
    Take the city at location `old_index` in the `road_map`, take it out and
    slot it into 'new_index', and return the tuple 

        (new_road_map, new_total_distance)

    Allow for the possibility that `index1=index2`,
    and handle this case correctly.
    """
    new_road_map = road_map
    new_road_map.insert(new_index, new_road_map.pop(old_index))
    
    new_total_distance = compute_total_distance(new_road_map)
    
    return (new_road_map, new_total_distance)

def find_best_cycle(road_map):
    """
    Using a combination of `swap_cities`, `swap_adjacent_cities` and 
    'insert_cities', try `10000` swaps, and each time keep the best cycle 
    found so far. After `10000` swaps, return the best cycle found so far.
    """
    
    best_road_map = road_map
    compare = copy.deepcopy(best_road_map)
    best_dist = compute_total_distance(best_road_map)
    
    for attempt in range(10000):
        
        # Does a random adjacent swap
        index = random.randint(0,len(best_road_map)-1)
        new_dist1 = (swap_adjacent_cities(compare, index))
        
        # No changes made to road_map if total distance is the same
        if new_dist1[1] < best_dist:
            best_road_map = copy.deepcopy(new_dist1[0])
            best_dist = copy.deepcopy(new_dist1[1])

        
        # Does a random swap of 2 cities
        index1 = random.randint(0,len(best_road_map)-1)
        index2 = random.randint(0,len(best_road_map)-1)
        new_dist2 = (swap_cities(compare, index1, index2))

        # No changes made to road_map if total distance is the same
        if new_dist2[1] < best_dist:
            best_road_map = copy.deepcopy(new_dist2[0])
            best_dist = copy.deepcopy(new_dist2[1])
            
        # Does a random position insert of a city
        old_index = random.randint(0,len(best_road_map)-1)
        new_index = random.randint(0,len(best_road_map)-1)
        new_dist3 = (insert_cities(compare, old_index, new_index))

        # No changes made to road_map if total distance is the same
        if new_dist3[1] < best_dist:
            best_road_map = copy.deepcopy(new_dist3[0])
            best_dist = copy.deepcopy(new_dist3[1])
    
    return best_road_map

def circle_route_eastwest(road_map):
    """
    Split road_map into east and west by sorting map by longitude.
    Sort first half of map by latitude and second half of map by latitude 
    in reverse order. Outputs circle road_map and total distance.    
    """
    #Sort map by longitude, split map into two.
    road_map.sort(key=lambda tup: tup[2])
    east = road_map[:len(road_map)//2]
    west = road_map[len(road_map)//2:]

    #Sort first half of map by latitude
    east.sort(key=lambda tup: tup[3])
    #Sort second half of map by latitude in reverse order. 
    west.sort(key=lambda tup: tup[3], reverse = True)

    return east + west

def circle_route_northsouth(road_map):
    """
    Split road_map into north and south by sorting map by latitude.
    Sort first half of map by longitude and second half of map by longitude 
    in reverse order.
    """
    #Sort map by latitude, split map into two.

    road_map.sort(key=lambda tup: tup[3])
    south = road_map[:len(road_map)//2]
    north = road_map[len(road_map)//2:]
    
    #Sort first half of map by longitude
    south.sort(key=lambda tup: tup[2])
    #Sort second half of map by longitude in reverse order. 
    north.sort(key=lambda tup: tup[2], reverse = True)
   
    return south + north

def best_route(road_map):
    """Checks to see if the map is best ordered by circle_route_northsouth or
    circle_route_eastwest, then does 10,000 random position inserts using
    'insert_cities'"""
    
    # Order by circle_route_northsouth or
    circle_route_eastwest
    best_road_map = circle_route_eastwest(road_map)
    compare = copy.deepcopy(best_road_map)
    best_dist = compute_total_distance(best_road_map)
    
    if compute_total_distance(circle_route_eastwest(road_map)) > \
    compute_total_distance(circle_route_northsouth(road_map)):
            best_road_map = circle_route_northsouth(road_map)
    
    # 10,000 random position inserts
    for attempt in range(100000):
        
        old_index = random.randint(0,len(best_road_map)-1)
        new_index = random.randint(0,len(best_road_map)-1)
        new_dist3 = (insert_cities(compare, old_index, new_index))
    
        # No changes made to road_map if total distance is the same
        if new_dist3[1] < best_dist:
            best_road_map = copy.deepcopy(new_dist3[0])
            best_dist = copy.deepcopy(new_dist3[1])
    
    return best_road_map

def print_map(road_map):
    """
    Prints, in an easily understandable format, the cities and 
    their connections, along with the cost for each connection 
    and the total cost. Outputs circle road_map and total distance.
    """
    
    # Print Format:
    """
    State1, City1 -> State2, City 2
    Distance: (distance) miles
    Total Distance: (total distance) miles
    """
    
    for dest in range(len(road_map)):
        print(str(dest+1) + ")", road_map[dest][0] + ",", road_map[dest][1], 
             "->", road_map[(dest + 1) % len(road_map)][0] + ",", 
             road_map[(dest + 1) % len(road_map)][1] + "\nDistance:", 
             (distance(road_map[dest][2], road_map[dest][3],
             road_map[(dest+1) % len(road_map)][2], 
             road_map[(dest+1) % len(road_map)][3])//.01)/100,"miles\n")
        
    print("Total distance:", 
          (compute_total_distance(road_map)//.01)/100,"miles\n")
    
    return None

def plot_map(road_map):
    """
    Prints a visualised plot of the route.
    """
    latitude = []
    longitude = []
    city = []
    
    for points in road_map:
        latitude.append(points[2])
        longitude.append(points[3])
        city.append(points[1])
    
    # Plots the location of the cities with a black dot
    plt.scatter(longitude, latitude, color = "black")
    
    # Joins the cities with a dotted red line
    plt.plot(longitude, latitude, color = "red", linestyle = "--")
    
    # Connects the last point back to the first point
    plt.plot([longitude[0],longitude[-1]], [latitude[0],latitude[-1]], 
             color = "red", linestyle = "--")
    
    # Labels the cities in blue
    for x, y, loc in zip(longitude, latitude, city):
        plt.text(x, y, loc, color = "blue")
        
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Suggested Route")
    
    plt.show()
    
    return None

def main():
    """
    Reads in, and prints out, the city data, then creates the "best"
    cycle and prints it out.
    """
    # Ensure the outcome is constant
    #random.seed(333)
    
    # Reads in a file
    road_map = read_cities("city-data.txt")
    
    # Prints out the data to 2 decimal places
    print_cities(road_map)
    
   
    # Sorts list by either circular-NS or circular-EW, then goes through swaps
    print("\nBest cycle:\n")
    best_cycle = best_route(road_map)
    
    # Prints itinerary for best cycle
    print_map(best_cycle)
    
    # Prints map for best cycle
    plot_map(best_cycle)
    
    return None

if __name__ == "__main__":
    main()
