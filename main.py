from street_sprint import StreetSprint, ShortestPath

def main():
    # Get the names of 2 locations from user
    # Default locations are Beque Holic and The Hub in Gainesville, Florida
    location1 = input("Enter the first location: ")
    if location1 == "":
        location1 = "Beque Holic, Gainesville, Florida"

    location2 = input("Enter the second location: ")
    if location2 == "":
        location2 = "The Hub, Gainesville, Florida"

    s = StreetSprint()
    print('Map bounds: ', s.get_map_bounds())
    s.add_start_location(location1)
    s.add_end_location(location2)

    s.get_shortest_path("default")
    s.get_shortest_path("dijkstra")
    # s.get_shortest_path("bellman-ford")
    s.get_shortest_path("a-star")
    # Find the shortest path between the 2 locations


    # s.plot_map()

if __name__ == "__main__":
    main()