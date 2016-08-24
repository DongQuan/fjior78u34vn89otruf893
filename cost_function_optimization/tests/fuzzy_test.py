from sklearn.datasets import *
import numpy as np
import matplotlib.pyplot as plt
from cost_function_optimization import fuzzy_clustering
from validity_scripts import internal_criteria, external_criteria
from scipy.stats import norm

import unittest

plt.style.use('ggplot')

class Test(unittest.TestCase):

    #@unittest.skip("no")
    def testBlobs(self):
        no_of_clusters= 6
        
        # Create the dataset
        X, y = make_blobs(n_samples=50, centers= no_of_clusters, n_features=2,random_state=None)
        
        # Run the clustering algorithm
        X, centroids, ita, centroids_history = fuzzy_clustering.fuzzy(X, no_of_clusters)
        
        # Plotting
        plot_data_util(X, centroids, centroids_history, no_of_clusters)
        
        # Examine Cluster Validity with statistical tests
        initial_gamma, list_of_gammas, result = internal_criteria.internal_validity(X, no_of_clusters)
        #initial_indices, list_of_indices = external_criteria.external_validity(X, no_of_clusters, y)
        
        # Histogram of gammas from internal criteria 
        hist_gamma_internal_criteria(initial_gamma, list_of_gammas, result)
        
        # Histogram of indices for external criteria
        '''for i in range(4):
            hist_gamma_internal_criteria(initial_indices[i], list_of_indices[i, :])
        ''' 
    
        
    @unittest.skip("no")
    def testCircles(self):
        no_of_clusters = 2
        X, y = make_circles(n_samples=100, shuffle = True, noise = 0.05, factor = 0.5, random_state = 10)
        X, centroids, ita, centroids_history = fuzzy_clustering.fuzzy(X, 2)
        plot_data_util(X, centroids, centroids_history, no_of_clusters)
        
    @unittest.skip("no")
    def testMoons(self):
        no_of_clusters = 2
        X, y = make_moons(n_samples=1000, shuffle = True, noise = 0.1, random_state = 10)
        X, centroids, ita, centroids_history = fuzzy_clustering.fuzzy(X, 2)
        X = plot_data_util(X, centroids, centroids_history, no_of_clusters)
    
    
    # Relative Criteria Clustering
    #@unittest.skip('no')
    def testRelativeBlobs(self):
        pass
    
    
    
def plot_data_util(X, centroids, centroids_history ,no_of_clusters):
    np.random.seed(seed = None)
    clusters = np.unique(X[:, 2])
    
    for i, cluster in enumerate(clusters):
        plt.scatter(X[ X[:,2] == cluster, 0], X[ X[:, 2] == cluster, 1], c=np.random.rand(3,1), s = 30)
    
    # Plots the centroids history
    #colors= ['k', 'b', 'g', 'y', 'm']
    for i in range(0, len(centroids_history),  no_of_clusters):
        for j in range(i, i + no_of_clusters):
            plt.plot(centroids_history[j, 0], centroids_history[j, 1], c = np.random.rand(3,1), marker = 'x', mew =  1, ms = 15, alpha = 0.3 + j * 0.7/(len(centroids_history)/no_of_clusters))
    
    # Plots the centroids
    for i, c in enumerate(centroids):
            plt.plot(centroids[i, 0], centroids[i, 1], c = 'r', marker = 'x', mew=2, ms = 10)
    
    plt.show()

def hist_gamma_internal_criteria(initial_gamma, list_of_gammas, result):
    n, bins, patches = plt.hist(list_of_gammas, bins = 50, color = 'g')
    plt.hist(initial_gamma, bins = 50, color = 'b')
    bincenters = 0.5*(bins[1:]+bins[:-1])
    y = norm.pdf(bincenters, np.mean(list_of_gammas), np.std(list_of_gammas))
    plt.plot(bincenters, y, 'r--', linewidth=1)
    
    plt.title('Histogram')
    plt.suptitle(result)
    plt.show()




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()