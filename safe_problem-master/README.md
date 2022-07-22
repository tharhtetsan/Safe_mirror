# Safe Problem

https://icpc.baylor.edu/worldfinals/problems

## Problem Description

A safe with an optical closure mechanism, has a rectangular grid with several
mirrors. The grid consists of `r` rows and  `c` columns. There are `m` mirrors
with orientation `/`, and `n` mirrors with orientation `\`. This is illustrated
below.

<p float="left">
  <img src="/figs/setup.png" width="640" />
</p>

When the laser is activated, a beam enters the top row of the grid horizontally from the left.
The beam is reflected by every mirror that it hits. Each mirror has a `45` degree diagonal
orientation, either `/` or `\`. If the beam exits the bottom row of the grid horizontally
to the right, it is detected and the safe opens (see the left side of the figure above).
Otherwise the safe remains closed and an alarm is raised.

Each safe has a missing mirror, which prevents the laser beam from traveling successfully
through the grid (see the right side of the figure above).
The safe has a mechanism that enables the user to drop a single mirror
into any empty grid cell. A legitimate user knows the correct position and
orientation of the missing mirror (`/` in row `4` column `3` above)
and can thus open the safe. Without this knowledge the user has to
guess correctly, which can be difficult for safes with large grids.

The problem is to determine if particular safes are actually secure.
A secure safe does not open right away without inserting a mirror,
and there is at least one valid location and orientation for the missing mirror.
There may indeed be multiple such locations and orientations.

#### Input

Each test case describes a single safe and starts with a line containing
four integer numbers `r`, `c` ,` m`, and `n` where `(1 ≤ r , c ≤ 1000000 and 0 ≤ m, n ≤ 200000)`.

The mechanisms grid has `r` rows and `c` columns.
Each of the next `m` lines contains two integer numbers `ri` and `ci` `(1 ≤ ri ≤ r and 1 ≤ ci ≤ c)`
specifying that there is a `/` mirror in row `ri` column `ci`. The following `n`
lines specify the positions of the `\` mirrors in the same way.
The `m + n` positions of the mirrors are pairwise distinct.

#### Output

* For each test case, display its case number followed by: `0` if the safe opens without inserting a mirror.

* `k r c` if the safe does not open without inserting a mirror, there are
exactly `k` positions where inserting a mirror opens the safe, and `(r, c)` is the
lexicographically smallest such row, column position. A position where
both a `/` and a `\` mirror open the safe counts just once.

* `impossible` if the safe cannot be opened with or without inserting a mirror.


## Approach and Analysis

#### Algorithm Description and Time Complexity

* Firstly, we need to trace the path of the laser beam from the source
to see which mirrors it encounters. If the laser reaches the detector without needing
to place an additional mirror, we can directly return `0`.

* One way to trace the path of the beam is to create a path along the direction of the
beam and check each grid cell if a mirror exists and change direction according to
the mirror orientation. However in the worst case, this could mean checking every
single grid cell, and hence (`O(M * N)` runtime complexity, where `M` and `N` are
the number of rows and columns).

* But then, given the current direction of the laser beam, we need to check
only that row or column where the next mirror is, so that we can change the direction
in that grid cell. For this, we can maintain dictionaries with locations of mirrors for each
row and column respectively so that we can look up the dictionaries to find the closest mirror.
Finding the index of the current position of the laser beam in this list can be done using binary
search with `O(log(N))` time complexity, if we pre-sort the list of row/column indices which
are the locations of mirrors. We can assume `O(N * log(N))` time complexity for sorting,
where `N` is the average number of mirrors in a row or column. We however need to do this
for every row/column where a mirror is encountered.

* With the index and direction, we can find the index of the next mirror and hence its position.
The result is that we end up with the path of the laser beam as a set of points that
form line segments. So, if the total number of mirrors is `N` where `N = m + n`,
then we can trace the path of the laser beam with `O(N * log(N))` time complexity.
Note that this is the worst case, if the beam hits every mirror.

* If the forward laser beam trace does not reach the detector, we need to find the
locations where a mirror can be placed. This can be computed if we ran a backward laser beam
trace from the detector. The points of intersection of the backward trace with the
forward trace are possible locations where a mirror can be placed to open the safe.

* So, if the forward laser beam trace does not reach the detector, we run a backward
trace, which adds another `O(N * log(N))` time complexity.

* Now we end up with sets of horizontal and vertical line segments from the two
traces. We need to compute intersection points of these segments.

* We realise that we need to check the horizontal segments from the forward trace,
with the vertical segments of the backward trace and vice versa, for intersection
points. A naive way is to compare each segment with every other segment for intersections.
But this would result in `O(N * M)` time complexity in the worst case, where `N` and `M` are the
number of horizontal and vertical line segments. This quadratic complexity is pretty bad.

* But we can do better, if we use a sweep-line approach. The idea is that we scan horizontally
from left to right and record events. The possible events are:

  * horizontal line segment start
  * horizontal line segment end
  * vertical line segment

* Whenever a horizontal line segment start is reached, we use a marker and add the
row coordinate as a node to a binary search tree. When we reach a horizontal line segment end
we remove that node from the tree. If we encounter a vertical segment, we do 1-D range
search in the binary tree for the row coordinate that intersects with potential
active horizontal segments. This is illustrated in the figure below.

<p float="left">
  <img src="/figs/sweep_line.png" width="640" />
</p>

* We need to pre-sort the events based on the column coordinate. We assume `O(N * log(N))`
for this. `N` here corresponds to events which are the horizontal segment start/end points
or vertical lines.

* All insertions into the binary search tree would take `O(N * log(N))` time complexity,
assuming `N` nodes in the tree.

* All deletions from the binary search tree would also take `O(N * log(N))` time complexity,
assuming `N` nodes in the tree.

* The 1-D range search would take `O(M * log(N))` time complexity assuming `N` possible searches,
where `N` is the range of a vertical segment (points between the end of points of the segment,
assuming closed line segments) and `M` is the number of vertical segments.

* Note that we assume `log(N)` time complexity for the various operations of the binary
search tree (insertion, deletion, search) which is the average case time complexity in general.
But for the given problem, since we will rarely have a worst case (fully unbalanced tree),
the average case time complexity is more apt to consider over the space of possible mirror
configurations. The worst case can occur if we encounter horizontal segments successively
increasing in row coordinate in which we will have `O(N)` for all tree operations, where `N`
is the number of nodes in the tree.

* We also assume that steps where sorting is involved, this is done using merge sort,
which would give `O(N * log(N))` time complexity. In python `timsort` algorithm is used
when calling `sorted()` function. https://arxiv.org/pdf/1805.08612.pdf.

* During the sweep-line, since we process the events which are sorted along column
coordinate and the range search also is done from top to bottom (row coordinate), the
first intersection point is the lexicographical one.

*  We run sweep-line twice, and if we get two lexicographical intersection points
from the sweeps, we compare them to resolve to the final one.

#### Space Complexity

* As for space, we had to store the row or column indices of each mirror
for every row and column. In the worst case, if there is atleast 1 mirror in every row/column,
then we have `O(M)` + `O(N)` space complexity for the dictionaries that we populate,
where `M` and `N` are the number of rows and columns. Each row or column can have different
number of mirrors, so we can assume an average number of mirrors per row/column which would
give `O(M * C)` + `O(N * C)` space complexity, where `C` can be approximately `(m + n) / r`
or `(m + n) / c`. This can still be regarded as `O(M)` + `O(N)`.
This space complexity is unavoidable for any algorithm.

* For the binary search tree, we have `O(N)` memory needed to store `N` possible events
(horizontal segment starts).

* We also store the horizontal and vertical segments. If there are `N` mirrors, there are `N + 1`
segments. So thats still `O(N)` space complexity.

## How to run

```bash
python main.py --input <path_to_input_file>
```

* Tested with python `3.6.3` on linux and OSX.
