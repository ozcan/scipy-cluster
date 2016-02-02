# Introduction #

This page lists feature requests made by the author or other users. If you think a feature listed below may be useful to you, please put your name by the "Seconded by" field and e-mail the author. Popularity will receive due consideration.

# Feature Request 1: templatizing code #

Currently only numpy arrays containing 64-bit floats and booleans (u\_chars) are supported. Numpy arrays containing any other kind of numeric data are converted. This results in copying so additional memory is used. By converting the code from C to C++, much of it can be templatized, thereby reducing unnecessary copying, speeding up the code and reducing the memory footprint.

**Difficulty**: medium

**Requested by**: Damian Eads

**Seconded by**: None

**Date requested**: March 15, 2008

# Feature Request 2: support for sparse vectors #

The distance metrics currently available only work on non-sparse representations. Providing support for sparse representations will be of use to the following groups of users

  * **information retrieval**: document vectors are typically sparse, each element corresponding to a word and its value representing the incidence of the word.

**Difficulty**: hard

**Requested by**: Damian Eads

**Seconded by**: None

**Date requested**: March 15, 2008

# Feature Request 3: support for memory mapped arrays #

Currently, the size of the input set of vectors on which to compute distances and linkages is limited to the physical memory of the host machine or 2 GB, whichever is greater. Two features will enable hcluster to support larger datasets:


  * support for disk-based, memory-mapped arrays. Input and scratch space is allocated from the disk, and memory is mapped to it so existing algorithms.
  * provide an option for computing distances when they are needed. When this option is specified, distances are not precomputed at the beginning.

**Difficulty**: hard

**Requested by**: Damian Eads

**Seconded by**: None

**Date requested**: March 15, 2008