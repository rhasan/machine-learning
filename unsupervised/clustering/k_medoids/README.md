# k-medoids Clustering Algorithm
This is an implementation of [k-medoids clustering algorithm](https://en.wikipedia.org/wiki/K-medoids). I haven't found any python implementation so I implemented it.

The code is well tested and I used it in some experiments during my PhD.
 
 In short, in contrast to the k-means algorithm, k-medoids chooses datapoints as centers ( [medoids](https://en.wikipedia.org/wiki/Medoid) or exemplars).  A common application of the medoid is the k-medoids clustering algorithm, which is similar to the k-means algorithm but works when a mean or centroid is not definable. This algorithm basically works as follows. First, a set of medoids is chosen at random. Second, the distances to the other points are computed. Third, data are clustered according to the medoid they are most similar to. Fourth, the medoid set is optimized via an iterative process.