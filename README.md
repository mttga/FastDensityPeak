# FastDensityPeak
Python highly optimized implementation of _Clustering by fast search and find of density peaks_ (2014)

Its main idea is to find the density (rho) and the minimum realtive distance (delta) of all the isntances. Plotting delta as a function of rho, the plot's outliers are the centroids. Each point is assigned to the centroid of it's nearest neighbour, starting from the points with highest density.

It is well known for requiring almost no hyperparameter optimization, while being time-effiecient and robust in retriving clusters of any shape. However, most of the implementations in python are very slow because they just copy-paste the original MATLAB code of the authors. The fastest require cython.

**This implementation requires only numpy and matplotlib, but it performes better than other implementations based on cython. In general, its permormances are more or less similar to sklearn's standard K-Means – expecially with not very large datasets.**

## How to use the algorithm

Simply add the fastdensitypeaks.py script in yuor project folder. Then you can import the algorithm as a standard sklearn class:

```Python
from fastdensitypeaks import FastDensityPeaks
from sklearn.datasets import make_moons

x, _ = make_moons(n_samples=2000, noise=0.15, random_state=0)

# Using fit_predict
fdp = FastDensityPeaks(verbose=True, autoassign=True)
labels = fdp.fit_predict(x) 

# Using fit 
fdp.fit(X)
labels = fdp.labels_

# Using manual assignation
fdp.decision_graph(80, 1.5)
```

In the standard implementation of the algorithm, the user is required to indicate to the algorithm the cenroids in the rho/delta decision graph. Here this is done using the decision_graph method. Additionaly, with autoassign=True the algorithm find them authomatically. 

**Refer to the real_datasets and toy_datasets.ipynb for real_datasets.ipynb notebooks for more details**

## About the parameters

- With verbose=True the decision graph (delta as function of rho) is authomatically displayed during the fit
- With autoassign=True the algorithm retrieves automatically the centroids. This method is a my addition to the original algorithm and it simply retrieves the outliers of the rho/delta decision graph using the z_scores of delta. It's euristich and sometimes can fail.
- The fraction parameter (in the fit method) it is used to retrieve authomatically the cutoff parameter dc. Basically, if we set it to 0.02, the cutoff will be defined so that the average number of neighbours will be the 2% of the data
- The fit_predict method returns the labels of the clusters (authomatically uses the autoassign function)
- Since the algorithm is performed one shot on all the data, a predict method doesn't make sense in this case
- The get_halo function returns the labels with an additional label (-1) for the points that could be referred as noise


## Look at the performances
![Alt text](results/toy_datasets.png?raw=true "Toy datasets")

## Summary of the contents
Folders:
- datasets: 
  - toy and real: contain the csvs of the datasets tested in the experiments
  - datasets.py: contains the function to load and preprocess the real datasets
- results: contains the tables and the plots produced in the experiments

Python files:
- fastdensitypeak.py: contains the class _FastDensityPeaks_, that is the implementation of the algorithm in the scikit-learn fashion

Notebooks:
- toy_datasets.ipynb: contains the experiments with the simple little datasets
- real_datasets.ipynb: contains the experiments with the three real datasets

Other:
- requirements.txt: contains the names of the packages required to run algorithm (for running the notebooks scikit-learn and pandas are also required)

