# cluster.py
#
# Author: Damian Eads
# Date:   September 22, 2007
#
# Copyright (c) 2007, Damian Eads
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#   - Redistributions of source code must retain the above
#     copyright notice, this list of conditions and the
#     following disclaimer.
#   - Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer
#     in the documentation and/or other materials provided with the
#     distribution.
#   - Neither the name of the author nor the names of its
#     contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Portions of the documentation make reference to the product MATLAB.
# MATLAB is a Registered Trademark of The MathWorks Corporation.

import _cluster_wrap
import scipy, scipy.stats
import types
import math

cpy_non_euclid_methods = {'single': 0, 'complete': 1, 'average': 2, 'weighted': 6}
cpy_euclid_methods = {'centroid': 3, 'median': 4, 'ward': 5}
cpy_linkage_methods = set(cpy_non_euclid_methods.keys()).union(set(cpy_euclid_methods.keys()))
array_type = type(scipy.array([]))

def randdm(pnts):
    """ Generates a random distance matrix stored in condensed form. A
        pnts * (pnts - 1) / 2 sized vector is returned.
    """
    if pnts >= 2:
        D = scipy.rand(pnts * (pnts - 1) / 2)
    else:
        raise AttributeError("The number of points in the distance matrix must be at least 2.")
    return D

def linkage(y, method='single', metric='euclidean'):
    """ linkage(y, method)

        Performs hierarchical clustering on the condensed distance matrix y.
        y must be a n * (n - 1) sized vector where n is the number of points
        paired in the distance matrix. The behavior of this function is
        very similar to the MATLAB linkage function.

        A (n - 1) * 4 matrix Z is returned. At the i'th iteration, clusters
        with indices Z[i, 0] and Z[i, 1] are combined to form cluster n + i.
        A cluster with an index less than n corresponds to one of the n
        original clusters. The distance between clusters Z[i, 0] and
        Z[i, 1] is given by Z[i, 2]. The fourth value Z[i, 3] represents the
        number of nodes in the cluster n + i.

        The following methods are used to compute the distance dist(s, t)
        between two clusters s and t. Suppose there are s_n original objects
        s[0], s[1], ..., s[n-1] in cluster s and t_n original objects
        t[0], t[1], ..., t[n-1] in cluster t.
        
          * method='single' assigns dist(s,t) = MIN(dist(s[i],t[j]) for
            all points i in cluster s and j in cluster t.

               (also called Nearest Point Algorithm)

          * method='complete' assigns dist(s,t) = MAX(dist(s[i],t[j]) for
            all points i in cluster s and j in cluster t.

               (also called Farthest Point Algorithm or Voor Hees)

          * method='average' assigns dist(s,t) =
               sum_{ij} { dist(s[i], t[j]) } / (|s|*|t|)
            for all points i and j where |s| and |t| are the
            cardinalities of clusters s and t, respectively.

               (also called UPGMA)

          * method='weighted' assigns

               dist(q,u) = (dist(s,u) + dist(t,u))/2

            where q is the newly formed cluster consisting of s and t,
            and u is a remaining cluster in the unused forest of
            clusters. (also called WPGMA)

        linkage(X, method, metric='euclidean')

        Performs hierarchical clustering on the objects defined by the
        n by m observation matrix X.

        If the metric is 'euclidean' then the following methods may be
        used:

          * method='centroid' assigns dist(s,t) = euclid(c_s, c_t) where
            c_s and c_t are the centroids of clusters s and t,
            respectively. When two clusters s and t are combined into a new
            cluster q, the new centroid is computed over all the original
            objects in clusters s and t. (also called UPGMC)

          * method='median' assigns dist(s,t) as above. When two clusters
            s and t are combined into a new cluster q, the average of
            centroids s and t give the new centroid q. (also called WPGMC)
           
          * method='ward' uses the Ward variance minimization algorithm.
            The new entry dist(q, u) is computed as follows,

                 dist(q,u) =

             ----------------------------------------------------
             | |u|+|s|            |u|+|t|            |u|
             | ------- d(u,s)^2 + ------- d(u,t)^2 - --- d(s,t)^2
            \|    T                  T                T

            where q is the newly formed cluster consisting of clusters
            s and t, u is an unused cluster in the forest, and |*|
            is the cardinality of its argument. (also called incremental)
        """
    if type(y) != array_type:
        raise AttributeError('Incompatible data type. y must be an array.')
    s = y.shape
    if type(method) != types.StringType:
        raise AttributeError("Argument 'method' must be a string.")
    if y.dtype != 'double':
        raise AttributeError('Incompatible data type. y must be a matrix of doubles.')

    if len(s) == 1:
        d = scipy.ceil(scipy.sqrt(s[0] * 2))
        if d * (d - 1)/2 != s[0]:
            raise AttributeError('Incompatible vector size. It must be a binomial coefficient.')
        if method not in cpy_non_euclid_methods.keys():
            raise AttributeError("Valid methods when the raw observations are omitted are 'single', 'complete', 'weighted', and 'average'.")
        Z = scipy.zeros((d - 1, 4))
        _cluster_wrap.linkage_wrap(y, Z, int(d), \
                                   int(cpy_non_euclid_methods[method]))
    elif len(s) == 2:
        X = y
        n = s[0]
        m = s[1]
        if method not in cpy_linkage_methods:
            raise AttributeError('Invalid method: %s' % method)
        if method in cpy_non_euclid_methods.keys():
            dm = pdist(X, metric)
            Z = scipy.zeros((n - 1, 4))
            _cluster_wrap.linkage_wrap(dm, Z, n, \
                                       int(cpy_non_euclid_methods[method]))
        elif method in cpy_euclid_methods.keys():
            if metric != 'euclidean':
                raise AttributeError('Method %s requires the distance metric to be euclidean' % s)
            dm = pdist(X, metric)
#            if method == 'ward':
#                dm = scipy.sqrt((dm ** 2.0))
#                dm = (dm ** 2.0) / 2.0
            Z = scipy.zeros((n - 1, 4))
            _cluster_wrap.linkage_euclid_wrap(dm, Z, X, m, n,
                                              int(cpy_euclid_methods[method]))
    return Z

class cnode:

    def __init__(self, id, left=None, right=None, dist=0, count=1):
        self.id = id
        self.left = left
        self.right = right
        self.dist = dist
        self.count = count

def totree(Z, return_dict=False):
    """
    t = totree(Z)
    
    Converts a hierarchical clustering encoded in the matrix Z (by linkage)
    into a tree. The root cnode object is returned.
    
    Each cnode object has a left, right, dist, id, and count attribute. The
    left and right attributes point to cnode objects that were combined to
    generate the cluster. If both are None then the cnode object is a
    leaf node, its count must be 1, and its distance is meaningless but
    set to 0.0.

    A reference to the root of the tree is returned.

    If return_dict is True the object returned is a tuple (t,Z) where
    """

    if type(Z) is not array_type:
        raise AttributeError('Z must be a numpy.ndarray')

    if Z.dtype != 'double':
        raise AttributeError('Z must have double elements, not %s', str(Z.dtype))
    if len(Z.shape) != 2:
        raise AttributeError('Z must be a matrix')

    if Z.shape[1] != 4:
        raise AttributeError('Z must be a (n-1) by 4 matrix')

    # The number of original objects is equal to the number of rows minus
    # 1.
    n = Z.shape[0] + 1

    # Create an empty dictionary.
    d = {}

    # If we encounter a cluster being combined more than once, the matrix
    # must be corrupt.
    if scipy.unique(Z[:, 0:2].reshape((2 * (n - 1),))) != 2 * (n - 1):
        raise AttributeError('Corrupt matrix Z. Some clusters are more than once.')
    # If a cluster index is out of bounds, report an error.
    if (Z[:, 0:2] >= 2 * n - 1).sum() > 0:
        raise AttributeError('Corrupt matrix Z. Some cluster indices (first and second) are out of bounds.')
    if (Z[:, 0:2] < 0).sum() > 0:
        raise AttributeError('Corrupt matrix Z. Some cluster indices (first and second columns) are negative.')
    if Z[:, 2] < 0:
        raise AttributeError('Corrupt matrix Z. Some distances (third column) are negative.')

    if Z[:, 3] < 0:
        raise AttributeError('Counts (fourth column) are invalid.')

    # Create the nodes corresponding to the n original objects.
    for i in xrange(0, n):
        d[i] = cnode(i)

    nd = None

    for i in xrange(0, n - 1):
        fi = Z[i, 0]
        fj = Z[i, 1]
        if fi < i + n:
            raise AttributeError('Corrupt matrix Z. Index to derivative cluster is used before it is formed. See row %d, column 0' % fi)
        if fi < i + n:
            raise AttributeError('Corrupt matrix Z. Index to derivative cluster is used before it is formed. See row %d, column 1' % fj)
        nd = cnode(i + n, d[Z[i, 0]], d[Z[i, 1]])
        if d[int(Z[i, 0])].count + d[int(Z[i, 1])].count != nd.count:
            raise AttributeError('Corrupt matrix Z. The count Z[%d,3] is incorrect.' % i)
        d[n + i] = nd

    return nd

def squareform(X, force="no", checks=True):
    """ Converts a vectorform distance vector to a squareform distance
    matrix, and vice-versa. 

    v = squareform(X)

      Given a square dxd symmetric distance matrix X, v=squareform(X)
      returns a d*(d-1)/2 (n \choose 2) sized vector v.

      v[(i + 1) \choose 2 + j] is the distance between points i and j.
      If X is non-square or asymmetric, an error is returned.

    X = squareform(v)

      Given a d*d(-1)/2 sized v for some integer d>=2 encoding distances
      as described, X=squareform(v) returns a dxd distance matrix X. The
      X[i, j] and X[j, i] value equals v[(i + 1) \choose 2 + j] and all
      diagonal elements are zero.

    As with MATLAB, if force is equal to 'tovector' or 'tomatrix',
    the input will be treated as a distance matrix or distance vector
    respectively.

    If checks is set to False, no checks will be made for matrix
    symmetry nor zero diaganols. This is useful if it is known that
    X - X.T is small and diag(X) is close to zero. These values are
    ignored any way so they do not disrupt the squareform
    transformation.
    """
    
    if type(X) is not array_type:
        raise AttributeError('The parameter passed must be an array.')

    if X.dtype != 'double':
        raise AttributeError('A double array must be passed.')

    s = X.shape

    # X = squareform(v)
    if len(s) == 1 and force != 'tomatrix':
        # Grab the closest value to the square root of the number
        # of elements times 2 to see if the number of elements
        # is indeed a binomial coefficient.
        d = int(scipy.ceil(scipy.sqrt(X.shape[0] * 2)))

        print d, s[0]
        # Check that v is of valid dimensions.
        if d * (d - 1) / 2 != int(s[0]):
            raise AttributeError('Incompatible vector size. It must be a binomial coefficient n choose 2 for some integer n >= 2.')
        
        # Allocate memory for the distance matrix.
        M = scipy.zeros((d, d), 'double')

        # Fill in the values of the distance matrix.
        _cluster_wrap.to_squareform_from_vector_wrap(M, X)

        # Return the distance matrix.
        M = M + M.transpose()
        return M
    elif len(s) != 1 and force.lower() == 'tomatrix':
        raise AttributeError("Forcing 'tomatrix' but input X is not a distance vector.")
    elif len(s) == 2 and force.lower() != 'tovector':
        if s[0] != s[1]:
            raise AttributeError('The matrix argument must be square.')
        if checks:
            if scipy.sum(scipy.sum(X == X.transpose())) != scipy.product(X.shape):
                raise AttributeError('The distance matrix must be symmetrical.')
            if (X.diagonal() != 0).any():
                raise AttributeError('The distance matrix must have zeros along the diagonal.')

        # One-side of the dimensions is set here.
        d = s[0]
        
        # Create a vector.
        v = scipy.zeros(((d * (d - 1) / 2),), 'double')

        # Convert the vector to squareform.
        _cluster_wrap.to_vector_from_squareform_wrap(X, v)
        return v
    elif len(s) != 2 and force.lower() == 'tomatrix':
        raise AttributeError("Forcing 'tomatrix' but input X is not a distance vector.")
    else:
        raise AttributeError('The first argument must be a vector or matrix. A %d-dimensional array is not permitted' % len(s))

def pdist(X, metric='euclidean', p=2):
    """ Computes the distance between m points in n-dimensional space.

        1. pdist(X)

        Computes the distance between m points using Euclidean distance
        (2-norm) as the distance metric between the points. The points
        are arranged as m n-dimensional row vectors in the matrix X.

        2. pdist(X, 'minkowski', p)

        Computes the distances using the Minkowski distance (p-norm) where
        p is a number.

        3. pdist(X, 'cityblock')

        Computes the city block or manhattan distance between the points.

        4. pdist(X, 'seuclidean')

        Computes the standardized euclidean distance so that the distances
        are of unit variance.

        5. pdist(X, 'cosine')

        Computes the cosine distance between vectors u and v. This is
        
           1 - uv^T
           -----------
           |u|_2 |v|_2

        where |*|_2 is the 2 norm of its argument *.

        6. pdist(X, 'correlation')

        Computes the correlation distance between vectors u and v. This is

           1 - (u - n|u|_1)(v - n|v|_1)^T
           --------------------------------- ,
           |(u - n|u|_1)|_2 |(v - n|v|_1)|^T

        where |*|_1 is the Manhattan (or 1-norm) of its argument *,
        and n is the common dimensionality of the vectors.

        7. pdist(X, 'hamming')

        Computes the normalized Hamming distance, or the proportion
        of those vector elements between two vectors u and v which
        disagree. To save memory, the matrix X can be of type boolean.

        8. pdist(X, 'jaccard')

        Computes the Jaccard distance between the points. Given two
        vectors, u and v, the Jaccard disaance is the proportion of
        those elements u_i and v_i that disagree where at least one
        of them is non-zero.

        9. pdist(X, 'chebyshev')

        Computes the Chebyshev distance between the points. The
        Chebyshev distance between two vectors u and v is the maximum
        norm-1 distance between their respective elements. More
        precisely, the distance is given by

           d(u,v) = max_{i=1}^{n}{|u_i-v_i|}.

        10. pdist(X, f)
        
        Computes the distance between all pairs of vectors in X
        using the user supplied 2-arity function f. For example,
        Euclidean distance between the vectors could be computed
        as follows,

            dm = pdist(X, \
                       (lambda u, v: \
                        scipy.sqrt(((u-v)*(u-v).T).sum())))

        11. pdist(X, 'test_Y')

        Computes the distance between all pairs of vectors in X
        using the distance metric Y but with a more succint,
        verifiable, but less efficient implementation.

       """

    # FIXME: need more efficient mahalanobis distance.
    # TODO: canberra, bray-curtis, matching, dice, rogers-tanimoto,
    #       russell-rao, sokal-sneath, yule
    
    if type(X) is not array_type:
        raise AttributeError('The parameter passed must be an array.')
    
    s = X.shape

    if len(s) != 2:
        raise AttributeError('A matrix must be passed.');

    m = s[0]
    n = s[1]
    dm = scipy.zeros((m * (m - 1) / 2,), dtype='double')

    mtype = type(metric)
    if mtype is types.FunctionType:
        k = 0
        for i in xrange(0, m - 1):
            for j in xrange(i+1, m):
                dm[k] = metric(X[i, :], X[j, :])
                k = k + 1
    elif mtype is types.StringType:
        mstr = metric.lower()
        if X.dtype != 'double' and (mstr != 'hamming' and mstr != 'jaccard'):
            AttributeError('A double array must be passed.')
        if mstr in set(['euclidean', 'euclid', 'eu', 'e']):
            _cluster_wrap.pdist_euclidean_wrap(X, dm)
        elif mstr in set(['cityblock', 'cblock', 'cb', 'c']):
            _cluster_wrap.pdist_city_block_wrap(X, dm)
        elif mstr in set(['hamming', 'hamm', 'ha', 'h']):
            if X.dtype == 'double':
                _cluster_wrap.pdist_hamming_wrap(X, dm)
            elif X.dtype == 'bool':
                _cluster_wrap.pdist_hamming_bool_wrap(X, dm)
            else:
                raise AttributeError('Invalid input matrix type %s for hamming.' % str(X.dtype))
        elif mstr in set(['jaccard', 'jacc', 'ja', 'j']):
            if X.dtype == 'double':
                _cluster_wrap.pdist_hamming_wrap(X, dm)
            elif X.dtype == 'bool':
                _cluster_wrap.pdist_hamming_bool_wrap(X, dm)
            else:
                raise AttributeError('Invalid input matrix type %s for jaccard.' % str(X.dtype))
        elif mstr in set(['chebyshev', 'cheby', 'cheb', 'ch']):
            _cluster_wrap.pdist_chebyshev_wrap(X, dm)            
        elif mstr in set(['minkowski', 'mi', 'm']):
            _cluster_wrap.pdist_minkowski_wrap(X, dm, p)
        elif mstr in set(['seuclidean', 'se', 's']):
            VV = scipy.stats.var(X, axis=0)
            _cluster_wrap.pdist_seuclidean_wrap(X, VV, dm)
        # Need to test whether vectorized cosine works better.
        # Find out: Is there a dot subtraction operator so I can
        # subtract matrices in a similar way to multiplying them?
        # Need to get rid of as much unnecessary C code as possible.
        elif mstr in set(['cosine_old', 'cos_old']):
            norms = scipy.sqrt(scipy.sum(X * X, axis=1))
            _cluster_wrap.pdist_cosine_wrap(X, dm, norms)
        elif mstr in set(['cosine', 'cos']):
            norms = scipy.sqrt(scipy.sum(X * X, axis=1))
            nV = norms.reshape(m, 1)
            # The numerator u * v
            nm = scipy.dot(X, X.T)
            
            # The denom. ||u||*||v||
            de = scipy.dot(nV, nV.T);

            dm = 1 - (nm / de)
            dm[xrange(0,m),xrange(0,m)] = 0
            dm = squareform(dm)
        elif mstr in set(['correlation', 'co']):
            X2 = X - scipy.repmat(scipy.mean(X, axis=1).reshape(m, 1), 1, n)
            norms = scipy.sqrt(scipy.sum(X2 * X2, axis=1))
            _cluster_wrap.pdist_cosine_wrap(X2, dm, norms)
        elif mstr in set(['stub_mahalanobis']):
            k = 0;
            XV = scipy.dot(X, scipy.cov(X.T))
            dm = scipy.dot(XV, X.T)
            print dm.shape
            dm[xrange(0,m),xrange(0,m)] = 0
            dm = squareform(dm, checks=False)
        elif metric == 'test_euclidean':
            dm = pdist(X, (lambda u, v: scipy.sqrt(((u-v)*(u-v).T).sum())))
        elif metric == 'test_seuclidean':
            D = scipy.diagflat(scipy.stats.var(X, axis=0))
            DI = scipy.linalg.inv(D)
            dm = pdist(X, (lambda u, v: scipy.sqrt(((u-v)*DI*(u-v).T).sum())))
        elif metric == 'mahalanobis':
            V = scipy.cov(X.T)
            VI = scipy.linalg.inv(V)
            dm = pdist(X, (lambda u, v: scipy.sqrt(scipy.dot(scipy.dot((u-v),VI),(u-v).T).sum())))
        elif metric == 'test_cityblock':
            dm = pdist(X, (lambda u, v: abs(u-v).sum()))
        elif metric == 'test_minkowski':
            dm = pdist(X, (lambda u, v: math.pow((abs(u-v)**p).sum(), 1.0/p)))
        elif metric == 'test_cosine':
            dm = pdist(X, \
                       (lambda u, v: \
                        (1.0 - (scipy.dot(u, v.T) / \
                                (math.sqrt(scipy.dot(u, u.T)) * \
                                 math.sqrt(scipy.dot(v, v.T)))))))
        elif metric == 'test_correlation':
            dm = pdist(X, \
                       (lambda u, v: 1.0 - \
                        (scipy.dot(u - u.mean(), (v - v.mean()).T) / \
                         (math.sqrt(scipy.dot(u - u.mean(), \
                                              (u - u.mean()).T)) \
                          * math.sqrt(scipy.dot(v - v.mean(), \
                                                (v - v.mean()).T))))))
        elif metric == 'test_hamming':
            dm = pdist(X, (lambda u, v: (u != v).mean()))
        elif metric == 'test_jaccard':
            dm = pdist(X, \
                       (lambda u, v: \
                        ((scipy.bitwise_and((u != v),
                                       scipy.bitwise_or(u != 0, \
                                                   v != 0))).sum()) / \
                        (scipy.bitwise_or(u != 0, v != 0)).sum()))
        elif metric == 'test_chebyshev':
            dm = pdist(X, lambda u, v: max(abs(u-v)))
        else:
            raise AttributeError('Unknown Distance Metric: %s' % mstr)
    else:
        raise AttributeError('2nd argument metric must be a string identifier or a function.')
    return dm

def cophenet(*args, **kwargs):
    """
    d = cophenet(Z)

      Calculates the cophenetic distances between each observation in a
      hierarchical clustering defined by the linkage Z.

      Suppose p and q are original observations in disjoint clusters
      s and t, respectively and that s and t are joined by a direct
      parent cluster u. The cophenetic distance between observations
      i and j is simply the distance between clusters s and t.

      d is cophenetic distance matrix in condensed form. The ij'th
      entry is the cophenetic distance between original observations
      i and j.

    c = cophenet(Z, Y)

      Calculates the cophenetic correlation coefficient of a hierarchical
      clustering of a set of n observations in m dimensions. Returns the
      distance as a scalar. Y is the condensed distance matrix generated
      by pdist.

    (c, d) = cophenet(Z, Y, [])

      Same as cophenet(Z, Y) except the distance matrix is returned as
      the second element of a tuple.
      
    """
    nargs = len(args)

    if nargs < 1:
        raise AttributeError('At least one argument must be passed to cophenet.')
    Z = args[0]

    if (type(Z) is not array_type) or Z.dtype != 'double':
        raise AttributeError('First argument Z must be an array of doubles.')
    Zs = Z.shape

    if len(Zs) != 2:
        raise AttributeError('First argument Z must be a 2-dimensional array.')

    if Zs[1] != 4:
        raise AttributeError('First argument Z must have exactly 4 columns.')
    
    n = Zs[0] + 1

    zz = scipy.zeros((n*(n-1)/2,), dtype='double')
    _cluster_wrap.cophenetic_distances_wrap(Z, zz, int(n))
    if nargs == 1:
        return zz

    Y = args[1]
    if (type(Y) is not array_type) and Y.dtype != 'double':
        raise AttributeError('Second argument Y must be an array of doubles.')

    Ys = Y.shape

    if len(Ys) != 1:
        raise AttributeError('Second argument Y must be a 1-D array.')

    if Ys[0] != n*(n-1)/2:
        raise AttributeError('Incorrect size of Y. It must be a distance vector containing n*(n-1) elements.')
    
    z = zz.mean()
    y = Y.mean()
    Yy = Y - y
    Zz = zz - z
    #print Yy.shape, Zz.shape
    numerator = (Yy * Zz)
    denomA = Yy ** 2
    denomB = Zz ** 2
    c = numerator.sum() / scipy.sqrt((denomA.sum() * denomB.sum()))
    #print c, numerator.sum()
    if nargs == 2:
        return c

    if nargs == 3:
        return (c, zz)

def inconsistent(Z, d=2):
    """
    Calculates the inconsistency coefficient for all ...
    """

def from_mlab_linkage(Z):
    """
    Z2 = from_mlab_linkage(Z)
    
    Converts a linkage matrix Z generated by MATLAB to a new linkage
    matrix Z2 compatible with this module. The conversion does two
    things:

     * the indices are converted from 1..N to 0..(N-1) form, and
    
     * a fourth column Z[:,3] is added where Z[i,3] is equal to
       the number of original observations (leaves) in the non-singleton
       cluster i.
    """

    if type(Z) is not array_type:
        raise AttributeError('First argument Z must be a two-dimensional array.')
    if Z.dtype != 'double':
        raise AttributeError('First argument Z must contain doubles.')
    if Z.shape[1] != 3:
        raise AttributeError('First argument Z must have 3 columns.')
    if Z.shape[0] < 1:
        raise AttributeError('First argument Z must have at least one row.')

    Zs = Z.shape
    Zpart = Z[:,0:2]
    Zd = Z[:,2].reshape(Zs[0], 1)
    if Zpart.min() != 1.0 and Zpart.max() != 2 * Zs[0]:
        raise AttributeError('The format of the indices is not 1..N');
    CS = scipy.zeros((Zs[0], 1), dtype='double')
    Zpart = Zpart - 1
    _cluster_wrap.calculate_cluster_sizes_wrap(scipy.hstack([Zpart, \
                                                             Zd]), \
                                               CS, int(Zs[0]) + 1)
    return scipy.hstack([Zpart, Zd, CS])

def to_mlab_linkage(Z):
    """
    Z2 = to_mlab_linkage(Z)

    Converts a linkage matrix Z generated by the linkage function of this
    module to one compatible with matlab. Z2 is the same as Z with the last
    column removed and the indices converted to 1.N form.
    """
    if type(Z) is not array_type:
        raise AttributeError('First argument Z must be a two-dimensional array.')
    if Z.dtype != 'double':
        raise AttributeError('First argument Z must contain doubles.')
    if Z.shape[1] != 4:
        raise AttributeError('First argument Z must have 4 columns.')
    if Z.shape[0] < 1:
        raise AttributeError('First argument Z must have at least one row.')
    
    return scipy.hstack([Z[:,0:2] + 1, Z[:,2]])

# To write...

def is_valid_linkage(Z):
    pass

def is_valid_y(y):
    pass

def is_valid_dm(D):
    pass
