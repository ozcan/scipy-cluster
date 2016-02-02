**News (6th March 2013): I regret that the tutorial and API documentation were inaccessible for a week as yet another former university deleted my account. The links have been updated accordingly.**

**News (8th July 2012): I regret that the tutorial and API documentation were inaccessible for a week as my former university deleted my account. The links have been updated accordingly.**

**Note: all of the few remaining calls to scipy have been replaced with calls to numpy. Versions 0.1.8 and above do not require scipy as a dependency.**

# Introduction #

This library provides Python functions for agglomerative clustering. Its features include
  * generating hierarchical clusters from distance matrices
  * computing distance matrices from observation vectors
  * computing statistics on clusters
  * cutting linkages to generate flat clusters
  * and visualizing clusters with dendrograms.

The interface is very similar to MATLAB's Statistics Toolbox API to make code easier to port from MATLAB to Python/Numpy. The core implementation of this library is in C for efficiency.

# Setup and Installation #

## Windows ##

### Install dependencies ###

Install [Numpy](http://www.numpy.org/) by downloading the installer and running it. Make sure to run the installer for your version of Python (only Python versions 2.4 or 2.5 are supported).

If you use hcluster for plotting dendrograms, you will need [matplotlib](http://matplotlib.sf.net). Again, download the matplotlib installer for your version of Python. [Scipy](http://www.scipy.org/) is optional.

**Note: The few remaining calls to scipy have been replaced with numpy calls. Scipy is no longer required for hcluster.**

### Install hcluster ###

_Note: If you previously installed hcluster, remove it by going to Control Panel::Add/Remove Programs._

Download the installer that corresponds to your Python version. Run it.

### Optional ###

Install the [IPython](http://ipython.scipy.org) and [pyreadline](http://ipython.scipy.org/moin/PyReadline/Intro) libraries for a more user-friendly console interface to
Numpy, Scipy, and Matplotlib. [Ctypes](http://python.net/crew/theller/ctypes/) is required for Python 2.4.

### Pypi ###

[hcluster](http://pypi.python.org/pypi/hcluster/0.1.8) is available in the pypi index.

## Linux ##

### Debian ###

hcluster is available as a Debian package. Type
```
apt-get install python-hcluster
```
to install python-hcluster and its dependencies.

Thanks to Michael Hanke for packaging.

## FreeBSD ##

hcluster is available as a FreeBSD package. Type
```
cd /usr/ports/science/py-hcluster/ && make install clean
```
to install python-hcluster as a port. Otherwise, type
```
pkg_add -r py25-hcluster
```
to add as a package.

Thanks to Wen Heping for packaging.

### Ubuntu ###

**Required** Install `numpy` (required) by typing the following shell command as root:
```
apt-get install python-numpy
```

**Required** For building from source on Ubuntu 9.01 or higher:
```
apt-get install python-dev
```

**Optional** Install optional packages by typing the following shell commands as root:
```
apt-get install python-matplotlib # needed for dendrograms
apt-get install ipython
apt-get install python-scipy
```

Then follow the instructions for building from source on UNIX.

### Fedora and Red Hat Enterprise ###

**Required** Install `numpy` (required) by typing the following shell command as root:
```
yum install numpy
```

**Optional** Install optional packages by typing the following shell commands as root:
```
# The following are optional
yum install matplotlib # needed for dendrograms
yum install ipython
yum install scipy
```
to install Numpy, Scipy, and matplotlib.

Then follow the instructions for building from source on UNIX.

### Build from source on UNIX ###

Download the source tar ball, unpack it, and go into the source directory.
```
gzip -cd hcluster-XXX.tar.gz | tar xvf -
cd hcluster-XXX
```

Build the package by running the `setup.py` script with `build` as the build command.
```
python setup.py build
```

Install the package to a prefix of your choice (e.g. `/afs/qp/lib/python2.X/site-packages`) with `install` as the build command.
```
python setup.py install --prefix=/afs/qp
```
The `--prefix` option is optional and defaults to `/usr/local` on UNIX.

# hcluster Functions #

The hcluster Python library has an interface that is very similar to MATLAB's suite of hierarchical clustering functions found in the Statistics Toolbox. Some of the functions should be familiar to users of MATLAB (e.g. `linkage`, `pdist`, `squareform`, `cophenet`, `inconsistent`, and `dendrogram`). The `fcluster` and `fclusterdata` are equivalent to MATLAB's `cluster` and `cluseterdata` functions. All of the functions in this library reside in the `hcluster` package, which must be imported prior to using its functions.

# Python Help #
If you are unfamiliar with python, the [Python Tutorial](http://docs.python.org/tut/) is a good start. If you are looking for a good reference book, I highly recommend David Beazley's _Python Essential Reference_. It is by far the most comprehensive book I've come across, covering most of python's functionality with a very complete index.

# A Quick Example #
This script imports the `pdist`, `linkage`, and `dendrogram` functions. It then generates 10 random 100-dimensional observation vectors (with `pdist`), hierarchically clusters them (with `linkage`), and visualizes the result (with `dendrogram`).

```
from hcluster import pdist, linkage, dendrogram
import numpy
from numpy.random import rand

X = rand(10,100)
X[0:5,:] *= 2
Y = pdist(X)
Z = linkage(Y)
dendrogram(Z)

```

# Function Listing #

## Flat cluster formation ##

  * `fcluster`:           forms flat clusters from hierarchical clusters.
  * `fclusterdata`:       forms flat clusters directly from data.
  * `leaders`:            singleton root nodes for flat cluster.

## Agglomerative cluster formation ##

  * `linkage`:            agglomeratively clusters original observations.
  * `single`:             the single/min/nearest algorithm. (alias)
  * `complete`:           the complete/max/farthest algorithm. (alias)
  * `average`:            the average/UPGMA algorithm. (alias)
  * `weighted`:           the weighted/WPGMA algorithm. (alias)
  * `centroid`:           the centroid/UPGMC algorithm. (alias)
  * `median`:             the median/WPGMC algorithm. (alias)
  * `ward`:               the Ward/incremental algorithm. (alias)

## Distance matrix computation from a collection of raw observation vectors ##

  * `pdist`:              computes distances between each observation pair.
  * `squareform`:         converts a sq. D.M. to a condensed one and vice versa.

## Statistic computations on hierarchies ##

  * `cophenet`:           computes the cophenetic distance between leaves.
  * `from_mlab_linkage`:  converts a linkage produced by MATLAB(TM).
  * `inconsistent`:       the inconsistency coefficients for cluster.
  * `maxinconsts`:        the maximum inconsistency coefficient for each cluster.
  * `maxdists`:           the maximum distance for each cluster.
  * `maxRstat`:           the maximum specific statistic for each cluster.
  * `to_mlab_linkage`:    converts a linkage to one MATLAB(TM) can understand.

## Visualization ##

  * `dendrogram`:         visualizes linkages (requires matplotlib).

## Tree representations of hierarchies ##

  * `cnode`:              represents cluster nodes in a cluster hierarchy.
  * `lvlist`:             a left-to-right traversal of the leaves.
  * `totree`:             represents a linkage matrix as a tree object.

## Distance functions between two vectors u and v ##

  * `braycurtis`:         the Bray-Curtis distance.
  * `canberra`:           the Canberra distance.
  * `chebyshev`:          the Chebyshev distance.
  * `cityblock`:          the Manhattan distance.
  * `correlation`:        the Correlation distance.
  * `cosine`:             the Cosine distance.
  * `dice`:               the Dice dissimilarity (boolean).
  * `euclidean`:          the Euclidean distance.
  * `hamming`:            the Hamming distance (boolean).
  * `jaccard`:            the Jaccard distance (boolean).
  * `kulsinski`:          the Kulsinski distance (boolean).
  * `mahalanobis`:        the Mahalanobis distance.
  * `matching`:           the matching dissimilarity (boolean).
  * `minkowski`:          the Minkowski distance.
  * `rogerstanimoto`:     the Rogers-Tanimoto dissimilarity (boolean).
  * `russellrao`:         the Russell-Rao dissimilarity (boolean).
  * `seuclidean`:         the normalized Euclidean distance.
  * `sokalmichener`:      the Sokal-Michener dissimilarity (boolean).
  * `sokalsneath`:        the Sokal-Sneath dissimilarity (boolean).
  * `sqeuclidean`:        the squared Euclidean distance.
  * `yule`:               the Yule dissimilarity (boolean).

## Predicates ##

  * `is_valid_dm`:        checks for a valid distance matrix.
  * `is_valid_im`:        checks for a valid inconsistency matrix.
  * `is_valid_linkage`:   checks for a valid hierarchical clustering.
  * `is_valid_y`:         checks for a valid condensed distance matrix.
  * `is_isomorphic`:      checks if two flat clusterings are isomorphic.
  * `is_monotonic`:       checks if a linkage is monotonic.
  * `Z_y_correspond`:     checks for validity of distance matrix given a linkage

**Copyright (C) Damian Eads, 2007-2010. All Rights Reserved.**
**MATLAB is a registered trademark of the Mathworks Corporation**