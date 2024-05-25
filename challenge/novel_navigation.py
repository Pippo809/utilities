import numpy as np
import pandas as pd
from itertools import permutations
from python_tsp.exact import solve_tsp_dynamic_programming

def total_distance(points, route):
    distance = 0
    for i in range(len(route)):
        if i > 0 and points[route[i]][1] > points[route[i - 1]][1] and points[route[i]][0] == points[route[i - 1]][0]:
            return np.inf
        else:
            distance += np.linalg.norm(points[route[i]] - points[route[i - 1]])
    return distance

def euclidean_distance_matrix_no_vertical(points):
    matrix = np.sqrt(
        ((points[:, :, None] - points[:, :, None].T) ** 2).sum(axis=1)
    )
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if points[i][0] == points[j][0] and points[i][1] < points[j][1]:
                matrix[i][j] = np.inf
    return matrix

def novel_navigation(points):
    # Brute force approach, too slow
    # min_route = min((perm for perm in permutations(range(len(points))) if perm[0] == 0), key=lambda route: total_distance(points, route))
    # return min_route, total_distance(points, min_route)
    
    # Dynamic programming approach
    # I calculate the distance matrix, and set to infinite the distance of every point that is directly above another one
    distance_matrix = euclidean_distance_matrix_no_vertical(points)
    
    # I use the python_tsp library to solve the TSP problem as a dynamic programming problem (exact solution)
    permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
    return permutation, distance


if __name__ == '__main__':
    ds = pd.read_csv("1_novel_navigation.csv")
    points = ds.values
    route, distance = novel_navigation(points)
    print(route)
    print(distance)
    
    # Print path to visualize it, I readd the initial point to close the path
    # import matplotlib.pyplot as plt
    # route.append(route[0])
    # distance = total_distance(points, route)
    # for point in points:
    #     plt.scatter(point[0], point[1])
    # for i in range(len(route) - 1):
    #     plt.plot([points[route[i]][0], points[route[i + 1]][0]], [points[route[i]][1], points[route[i + 1]][1]])
    # plt.show()