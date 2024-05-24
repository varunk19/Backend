import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import networkx as nx
from math import radians, cos, sin, asin, sqrt

df = pd.read_csv("data_and_path/myDB.csv")

# s = source, d = destination

# column names
columns_df = df.columns


# Define the distance calculation function
def haversine(lat1, lon1, lat2, lon2):
    lon1, lon2, lat1, lat2 = map(radians, [lon1, lon2, lat1, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r


# Apply the distance function to each row in the DataFrame
df["distance(Km)"] = df.apply(
    lambda row: haversine(
        row["s_latitude"], row["s_longitude"], row["d_latitude"], row["d_longitude"]
    ),
    axis=1,
)


def find_optimal_path(
    flight_source, flight_destination, excluded_airport, included_airport
):
    # Sample data
    # data = {
    #     'airline': ['2B', '2B', '2B', '2B', '2B', '2B'],
    #     'airline_id': [410, 410, 410, 410, 410, 410],
    #     's_airport': ['AER', 'AER', 'AAA', 'AER', 'CCC', 'BBB'],
    #     's_airport_id': [2965, 2966, 2966, 2968, 2968, 2966],
    #     'd_airport': ['LED', 'AAA', 'BBB', 'CCC', 'DDD', 'LED'],
    #     'd_airport_id': [2990, 2990, 2962, 2990, 4078, 2962],
    #     'distance(Km)': [1000, 2000, 1500, 1800, 1200, 900]  # Distance between airports in km
    # }

    # Create DataFrame
    # df = pd.DataFrame(data)

    # Average speed and stopover time
    avg_speed = 900  # Average speed in km/hr
    stopover_time = 2  # Stopover time in hours

    # Check if source or destination is the excluded_airport
    if flight_source == excluded_airport:
        return "Flight cannot start from " + excluded_airport
    elif flight_destination == excluded_airport:
        return "There are no flights to " + excluded_airport
    else:
        # Create graph from DataFrame
        G = nx.from_pandas_edgelist(
            df, "s_airport", "d_airport", ["airline", "airline_id", "distance(Km)"]
        )

        # Function to find all routes from source to destination including indirect flights
        def find_all_routes(graph, source, destination):
            try:
                return list(nx.all_simple_paths(graph, source, destination))
            except nx.NetworkXNoPath:
                return []

        # Function to calculate total distance of a route
        def calculate_route_distance(route):
            distance = 0
            for i in range(len(route) - 1):
                distance += G[route[i]][route[i + 1]]["distance(Km)"]
            return distance

        # Function to calculate total time of a route
        def calculate_route_time(route):
            total_distance = calculate_route_distance(route)
            total_time = total_distance / avg_speed  # Time in hours
            total_time += (len(route) - 2) * stopover_time  # Add stopover time
            return total_time

        # Find all routes from source to destination
        all_routes = find_all_routes(G, flight_source, flight_destination)

        # Filter routes based on excluded_airport
        if excluded_airport:
            all_routes = [
                route for route in all_routes if excluded_airport not in route
            ]

        # Further filter routes based on included_airport
        if included_airport:
            all_routes = [route for route in all_routes if included_airport in route]

        # Sort routes by total time
        sorted_routes = sorted(all_routes, key=calculate_route_time)

        airports = {}

        for index, row in df.iterrows():
            airports[row["s_airport"]] = [row["s_latitude"], row["s_longitude"]]
            airports[row["d_airport"]] = [row["d_latitude"], row["d_longitude"]]

        # Prepare results
        results = []
        for i, route in enumerate(sorted_routes, start=1):
            total_distance = calculate_route_distance(route)
            total_time = calculate_route_time(route)
            total_stopovers = len(route) - 2
            results.append(
                {
                    "Route": [airports[each] for each in route],
                    "Total Distance (km)": total_distance,
                    "Total Stopovers": total_stopovers,
                    "Total Time (hours)": round(total_time, 2),
                }
            )

        # Determine the optimal path
        if sorted_routes:
            optimal_path = sorted_routes[0]
            optimal_distance = calculate_route_distance(optimal_path)
            optimal_time = calculate_route_time(optimal_path)
            optimal_stopovers = len(optimal_path) - 2
            optimal_result = {
                "Optimal Path": optimal_path,
                "Total Distance (km)": optimal_distance,
                "Total Stopovers": optimal_stopovers,
                "Total Time (hours)": round(optimal_time, 2),
            }
        else:
            optimal_result = "No routes found that satisfy the criteria."

        return results, optimal_result
