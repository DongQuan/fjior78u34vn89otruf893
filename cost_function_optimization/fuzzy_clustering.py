import numpy as np

euclidean_distance = lambda data, point: np.sqrt(np.sum(np.power(data - point, 2), axis = 1).reshape((len(data), 1)))

def fuzzy(data, no_of_clusters, centroids_initial = None, q = 1.25):
    ''' An implementation of the fuzzy clustering algorithm.
    
    Parameters:
        data((m x n) 2-d numpy array): a data set of m instances and n features
        no_of_clusters(integer): the number of clusters
        centroids_initial(): the optional initial values for the centroids
        q(integer): fuzzifier parameter
    
    Returns:
        data((m x (n + 1)) 2-d numpy array): the data set with one more column that contains the vector's cluster
        centroids_new((k x n)2-d numpy array): contains the k = no_of_clusters centroids with n features
        ita(float): a parameter used in possibilistic clustering.
        centroids_history((l x 2) 2-d numpy array): an array to keep the previous positions of the centroids for 
                                                    better visualisation of the result. 
        partition_matrix ((n x 2) 2-d numpy array): the matrix containing the weights which depict the grade of
                                                    membership of a vector i to the cluster j 
    
    '''
    # Initializations
    N = len(data)
    partition_matrix = np.zeros((N, no_of_clusters))
    no_of_features = len(data[0])
    # if the centroid are provided as parameter use them, otherwise create them
    if centroids_initial == None:
        centroids_old = np.random.choice(np.arange(np.min(data), np.max(data), 0.1), size = (no_of_clusters, no_of_features), replace = False)
    else:
        centroids_old = centroids_initial
    centroids_new = np.zeros(centroids_old.shape) 
    centroids_history = np.copy(centroids_old) # this array stacks the old positions of the centroids
    
    # A do - while loop implementation in Python, as the loop needs to run at least once
    condition = True
    
    while condition:
        # Update the U matrix 
        for i in range(N):
            # Precalculate euclidean distances for the current vector.
            eucl_dist = euclidean_distance(centroids_old, data[i,:])
            for j in range(no_of_clusters):
                partition_matrix[i][j] = 1 / np.sum(np.power((1./eucl_dist) * eucl_dist[j, 0], (1/(q-1))))
        
        # Update the centroids
        for i, centroid in enumerate(centroids_old):
            centroids_new[i] = np.sum(np.power(partition_matrix[:,[i]], q) * data,axis = 0) / np.sum(np.power(partition_matrix[:,i], q))
        
        # Update the termination criterion where e = 0.00001
        criterion_array = np.absolute(centroids_new - centroids_old) < 0.00001
        if np.all(criterion_array) :
            condition = False
        
        centroids_old = np.copy(centroids_new)
        centroids_history = np.vstack((centroids_history, centroids_old))
    
    # Ita calculation - applied when we use possibilistic clustering
    ita = []
    for i, centroid in enumerate(centroids_new):
        ita.append(np.sum(np.power(partition_matrix[:, [i]],q) * euclidean_distance(data, centroid)) / np.sum(np.power(partition_matrix[:, i], q)))
    
    # Assign each vector to a cluster taking the greatest u
    assigned_cluster = np.argmax(partition_matrix, axis = 1) 
    data = np.hstack((data, assigned_cluster.reshape(N, 1)))
    
    return data, centroids_new, ita, centroids_history, partition_matrix
    


