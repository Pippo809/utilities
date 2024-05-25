from sklearn.cluster import DBSCAN, KMeans
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def yin_yang(X, eps=0.2, min_samples=5):
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    y_dbscan = dbscan.fit_predict(X)

    # Select a random point in the lower left part of the dataset
    lower_left_points = np.where((X[:, 0] < -0.2) & (X[:, 1] < -0.2))[0]
    random_point_idx = np.random.choice(lower_left_points)
    
    yin_label = y_dbscan[random_point_idx]
    yin_region_points = X[y_dbscan == yin_label]
    num_yin_points = len(yin_region_points)
    return num_yin_points

if __name__ == '__main__':
    ds = pd.read_csv("2_partitioned_points.csv")
    scaler = StandardScaler()
    X = scaler.fit_transform(ds.values)

    num_yin_points = yin_yang(X, 0.25, 5)
    print(num_yin_points)
