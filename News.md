# What's new in Version 0.2.0 #

  1. Regression test suite implemented with 300 tests covering all functions except `dendrogram`. In the hcluster source directory type `nosetests hcluster` to run the tests.
  1. Several bugs were found and fixed while writing the tests.
  1. Better error handling in routines.
  1. Documentation is now in RST format.
  1. Changes to few function and class names so that the API conforms to Python naming conventions [PEP-0008](http://www.python.org/dev/peps/pep-0008/).
    * `cnode` is now `ClusterNode`
    * `totree` is now `to_tree`
    * `numobslinkage` is now `num_obs_linkage`
    * `numobs_y` is now `num_obs_y`
    * `numobs_dm` is now `num_obs_dm`
    * `Z_y_correspond` is now `correspond`
    * `lvlist` is now `leaves_list`

Note: efforts are made to avoid changing the API whenever possible. However, the previous releases were alpha releases. The primary focus of these releases was bug fixes and feature enhancements, not adherence to the Python naming standard.

# What's new in Version 0.1.9 #

  1. Fixed a bug in `hcluster.canberra` and `pdist(..., 'canberra')`.

# What's new in Version 0.1.8 #

  1. Arrays with data type other than `float64` (e.g. `float32`, `int`, `bool`) can be passed into any parameter in any function that requires a `double`. Any non-float64 data is copied into a new float64 array.
  1. Lists, tuples, and any other data structure supported by `numpy.asarray` can be passed as any parameter requiring a numpy array. For example, `pdist([[0.0, 3.0, 8.7], [3.4, 9.2, 16.2], [2.2, 3.0, 7.8]])` now processes its input without raising an exception. Internally, the list is converted to a numpy array, which can increase the memory footprint.
  1. Boolean distance functions now support passing non-boolean data with the caveat that storing any value other than 0 or 1 will generate meaningless distances for many of the functions.
  1. Scipy is no longer required as a dependency! You don't need to install it if you don't need it.

# What's new in Version 0.1.7 #

  1. Fixed some errors in the documentation for `median`, `centroid`, and `ward`.
  1. Fixed some bugs in predicates `numobs_y`, `numobs_linkage`, and `numobs_dm`.

# What's new in Version 0.1.6 #

  1. Fixed a bug introduced in 0.1.6 in pdist where passing boolean observation vectors always generates an exception.
  1. Fixed `jaccard_distance` function in `cluster.c`. It was a direct copy of `hamming`.
  1. Fixed `pdist('jaccard')` so it invokes the right C distance function.
  1. Fixed cluster.c so it compiles on OS X with gcc.

# What's new in Version 0.1.5 #

  1. Fixed a bug reported by a user where a `float32` array gets passed to the C function as a `float64` resulting in meaningless results in `pdist`.
  1. Fixed a bug involving API changes to fclusterdata. This caused fclusterdata to be completely nonfunctional.
  1. A new MSI installer for users with Python 2.5. Please let me know if it works.

# What's new in Version 0.1.4 #

  1. Added new `link_color_func` parameter to the `dendrogram` function.
  1. Fixed bug in `correlation` and `pdist(..., 'correlation')`.
  1. Fixed bug in `dendrogram` when `leaves_list` parameter is used.
  1. Added windows installer for Python versions 2.4 and 2.5. Windows users: please let me know if it works.