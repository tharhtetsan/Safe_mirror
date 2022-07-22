"""Solution to safe problem."""

import argparse
import operator

from binary_search_tree import *
from constants import *
from utils import *


parser = argparse.ArgumentParser(description='Safe problem')
parser.add_argument('--input', default='input.txt',
                    help='path to input text file')
args = parser.parse_args()


class LaserBeam:
    """Laser beam.

    Attributes:
        last_point_visited (tuple): last point visited by beam during trace.
        direction (str): direction of laser beam.
        horizontal_segments (list): list of horizontal segments from trace.
        vertical_segments (list): list of vertical segments from trace.

    """

    def __init__(self):
        """Constructor."""
        self.last_point_visited = None
        self.direction = None
        self.horizontal_segments = []
        self.vertical_segments = []

    def update_direction(self, direction):
        """Update direction of beam.

        Args:
            direction (str): direction of laser beam.

        """
        self.direction = direction

    def update_last_point_visited(self, point):
        """Update last point visited attribute.

        Args:
            point (tuple): position in grid.

        """
        self.last_point_visited = point

    def add_horizontal_segment(self, segment):
        """Add segment to list of horizontal segments.

        Args:
            segment (list): horizontal segment represented as list i.e [start, stop].

        """
        segment.sort(key=operator.itemgetter(1))
        self.horizontal_segments.append(segment)

    def add_vertical_segment(self, segment):
        """Add segment to list of vertical segments.

        Args:
            segment (list): vertical segment represented as list i.e [start, stop].

        """
        row_range = tuple(sorted([segment[0][0], segment[1][0]]))
        col = segment[0][1]
        self.vertical_segments.append(((row_range), col))


class Safe:
    r"""Safe with mirrors, specified by config.

    Attributes:
        rows (int): number of rows in the safe grid.
        cols (int): number of columns in the safe grid.
        m (int): number of mirrors in / config.
        n (int): number of mirrors in \ config.
        row_mirror_positions (dict): for a given row, column locations with mirrors.
        col_mirror_positions (dict): for a given column, row locations with mirrors.
        bst (BinarySearchTree): binary search tree.

    """

    def __init__(self, rows, cols, m, n):
        """Constructor."""
        self.rows = rows
        self.cols = cols
        self.m = m
        self.n = n
        self.row_mirror_positions = {}
        self.col_mirror_positions = {}
        self.bst = BinarySearchTree()

    def create_events_queue(self, horizontal_segments, vertical_segments):
        """Create a queue of events to process.

        Args:
            horizontal_segments (list): list of horizontal segments.
            vertical_segments (list): list of vertical segments.

        Returns:
            events (list): list of events to process.

        """
        events = []
        for segment in horizontal_segments:
            start, stop = segment

            # Markers for start and stop events.
            start.append(0)
            stop.append(1)

            events.append(start)
            events.append(stop)

        for segment in vertical_segments:
            events.append(segment)

        events.sort(key=operator.itemgetter(1)) # O(N * log(N)).

        return events

    def solve(self):
        """Solve safe.

        Returns:
            (str): solution after solving safe.

        """
        done, forward_trace = self.trace_forward()

        if done:
            return 0 # We are done, no mirror to be inserted.
        else:
            backward_trace = self.trace_backward()

        intersection_points, lexi_candidates = [], []
        # Sweep horizontal lines from forward trace.
        events = self.create_events_queue(forward_trace.horizontal_segments,
                                          backward_trace.vertical_segments)
        intersections = self.compute_intersections(events)

        if len(intersections) > 0:
            lexi_candidates.append(intersections[0])
        intersection_points.extend(intersections)

        # Sweep horizontal lines from backward trace.
        events = self.create_events_queue(backward_trace.horizontal_segments,
                                          forward_trace.vertical_segments)
        intersections = self.compute_intersections(events)

        if len(intersections) > 0:
            lexi_candidates.append(intersections[0])
        intersection_points.extend(intersections)

        n_intersections = len(intersection_points)
        if n_intersections > 0:
            if len(lexi_candidates) > 1:
                lexi_first = self.get_lexi_first(lexi_candidates)
            else:
                lexi_first = lexi_candidates[0]
        else:
            return "impossible"

        result = str(n_intersections) + " " + str(lexi_first[0]) + \
            " " + str(lexi_first[1])

        return result

    def get_lexi_first(self, lexi_candidates):
        """Get lexicographically first point out of two.

        Args:
            lexi_candidates (list): list of two points that could be
            lexicographically first from the two line sweeps.

        Returns:
            (list): lexicographically first point.

        """
        point_a, point_b = lexi_candidates

        if (point_a[0] < point_b[0]):
            return point_a
        elif (point_a[0] == point_b[0]):
            if (point_a[1] < point_b[1]):
                return point_a
        else:
            return point_b

    def compute_intersections(self, events):
        """Compute intersection points.

        Args:
            events (list): list of events to process.

        Returns:
            intersections (list): list of intersection points.

        """
        intersections = []
        for event in events:
            if type(event) is not tuple:
                x, y, event_flag = event
                if event_flag == 0:
                    self.bst[x] = x
                elif event_flag == 1:
                    try:
                        del self.bst[x]
                    except:
                        print("Degeneracy case. Just overlapping segments, don't worry!")
            else:
                x_range, y = event
                for i in range(x_range[0] + 1, x_range[1]):
                    if self.bst[i] is not None:
                        intersections.append((self.bst[i], y))

        return intersections

    def run_trace(self, laser_beam_trace, end):
        """Run trace of laser beam and return points that form line segments.

        Args:
            laser_beam_trace (LaserBeam): laser beam object.
            end (list): end point.

        Returns:
            (tuple): tuple with flag if beam reached end point, laser beam object.

        """
        done = False
        while True:
            next_point_trace, mirror_orientation, laser_beam_trace = \
                self.get_next_point_trace(laser_beam_trace)
            laser_beam_trace.update_last_point_visited(next_point_trace)
           
            if (next_point_trace == end):
                done = True
                break
            elif (next_point_trace[0] > self.rows) or (next_point_trace[1] > self.cols) \
                or (next_point_trace[0] < 1) or (next_point_trace[1] < 1):
                break
            else:
                
                new_direction = compute_direction(laser_beam_trace.direction, mirror_orientation)
                laser_beam_trace.update_direction(new_direction)
                print("#### new direction : ",new_direction)
                print(".........................................................")


        return done, laser_beam_trace

    def trace_forward(self):
        """Trace path of the laser from the source.

        Returns:
            (bool, list): flag if beam reached detector, list of points in path.

        """
        start = [1, 0]
        end = [self.rows, self.cols + 1]
        direction = RIGHT

        forward_trace = LaserBeam()
        forward_trace.update_last_point_visited(start)
        forward_trace.update_direction(direction)

        done, forward_trace = self.run_trace(forward_trace, end)
        print("trace_forward : ",done)
        return done, forward_trace

    def trace_backward(self):
        """Trace path of the laser from the detector back.

        Returns:
            (list): list of points in path.

        """

        start = [self.rows, self.cols + 1]
        end = [1, 0]
        direction = LEFT

        backward_trace = LaserBeam()
        backward_trace.update_last_point_visited(start)
        backward_trace.update_direction(direction)

        _, backward_trace = self.run_trace(backward_trace, end)

        return backward_trace

    def insert_range(self, list_mirrors, end):
        """Insert the bounds of the safe grid into list.

        Args:
            list_mirrors (list): list of tuples indicating positions, orientation of mirrors.
            end (int): rows or cols depending on list.

        Returns:
            (list): list of tuples of mirror locations, or bounds of grid.

        """
        list_mirrors = [item for item in list_mirrors]
        list_mirrors.insert(0, (0, None))
        list_mirrors.append((end, None))

        return list_mirrors

    def get_next_point_trace(self, laser_beam_trace):
        """Get next point in the path of laser beam.

        Tracing the path of beam, we find the next mirror it will hit or the
        end of the grid.

        Args:
            laser_beam_trace (LaserBeam): laser beam object.

        Returns:
            (tuple): next point in the laser beam path, orientation of last mirror
            encountered, laser beam object.

        """
        current_point_trace = laser_beam_trace.last_point_visited
        print("current_point_trace : ",current_point_trace)
        mirror_orientation = None

        cols_with_mirrors = self.row_mirror_positions.get(current_point_trace[0], [])
        cols_with_mirrors.sort(key=operator.itemgetter(0))
        cols_with_mirrors = self.insert_range(cols_with_mirrors, self.cols + 1)
       
        rows_with_mirrors = self.col_mirror_positions.get(current_point_trace[1], [])
        rows_with_mirrors.sort(key=operator.itemgetter(0))
        rows_with_mirrors = self.insert_range(rows_with_mirrors, self.rows + 1)
        
        print("col_mirror_positions : ",)
        print("row_mirror_positions : ",self.row_mirror_positions)
        print("cols_with_mirrors : ",cols_with_mirrors)
        print("rows_with_mirrors : ",rows_with_mirrors)

        
        if (laser_beam_trace.direction == RIGHT) or (laser_beam_trace.direction == LEFT):
            # Search along a row, beam travelling horizontally.
            if cols_with_mirrors is not None:
                cols_with_mirrors_pos = [tup[0] for tup in cols_with_mirrors]
                closest_mirror_interval = run_binary_search(cols_with_mirrors_pos,
                                                            current_point_trace[1])

                
                if laser_beam_trace.direction == RIGHT:
                    next_point_trace = [current_point_trace[0],
                                        cols_with_mirrors_pos[closest_mirror_interval + 1]]
                    mirror_orientation = cols_with_mirrors[closest_mirror_interval + 1][1]
                    


                elif laser_beam_trace.direction == LEFT:
                    next_point_trace = [current_point_trace[0],
                                        cols_with_mirrors_pos[closest_mirror_interval - 1]]
                    mirror_orientation = cols_with_mirrors[closest_mirror_interval - 1][1]
                    
                    print("closest_mirror_interval : ",closest_mirror_interval)
            else:
                # Laser leaves grid.
                next_point_trace = [current_point_trace[0], self.cols]

            # Append to list of segments.
            laser_beam_trace.add_horizontal_segment([current_point_trace, next_point_trace])
        else:
            # Search along a col, beam travelling vertically.
            if rows_with_mirrors is not None:
                rows_with_mirrors_pos = [tup[0] for tup in rows_with_mirrors]
                closest_mirror_interval = run_binary_search(rows_with_mirrors_pos,
                                                            current_point_trace[0])
                if laser_beam_trace.direction == DOWN:
                    next_point_trace = [rows_with_mirrors_pos[closest_mirror_interval + 1],
                                        current_point_trace[1]]
                    mirror_orientation = rows_with_mirrors[closest_mirror_interval + 1][1]
                elif laser_beam_trace.direction == UP:
                    next_point_trace = [rows_with_mirrors_pos[closest_mirror_interval - 1],
                                        current_point_trace[1]]
                    mirror_orientation = rows_with_mirrors[closest_mirror_interval - 1][1]
            else:
                # Laser leaves grid.
                next_point_trace = [self.rows, current_point_trace[1]]

            # Append to list of segments.
            laser_beam_trace.add_vertical_segment([current_point_trace, next_point_trace])
        
        print("mirror_orientation : ",mirror_orientation)
        print("cur direction : ",laser_beam_trace.direction)
        print("next_point : ",next_point_trace)
        return next_point_trace, mirror_orientation, laser_beam_trace


def run_binary_search(list_nums, target):
    """Do binary search over a list to find an element location.

    Args:
        list_nums (list): list of sorted numbers.
        target (int): number to find in the list.

    Returns:
        (int): index of found number.

    """
    lower = 0
    upper = len(list_nums)
    while lower < upper:
        mid = lower + (upper - lower) // 2
        val = list_nums[mid]
        if target == val:
            return mid
        elif target > val:
            if lower == mid:
                break
            lower = mid
        elif target < val:
            upper = mid


def compute_direction(direction_laser, mirror_orientation):
    r"""Compute new direction of laser beam.

    Given current direction of laser beam and mirror orientation, compute new
    direction.

    Args:
        direction_laser (str): current direction of laser beam.
        mirror_orientation (int): 0 to signify /, 1 to signify \.

    """
    if direction_laser == RIGHT:
        if mirror_orientation == 0:
            direction = UP
        elif mirror_orientation == 1:
            direction = DOWN
    elif direction_laser == LEFT:
        if mirror_orientation == 0:
            direction = DOWN
        elif mirror_orientation == 1:
            direction = UP
    elif direction_laser == DOWN:
        if mirror_orientation == 0:
            direction = LEFT
        elif mirror_orientation == 1:
            direction = RIGHT
    elif direction_laser == UP:
        if mirror_orientation == 0:
            direction = RIGHT
        elif mirror_orientation == 1:
            direction = LEFT

    return direction


def fill_mirror_position(safe, position, orientation):
    r"""Fill mirror position in the rows and columns of the safe.

    Args:
        safe (Safe): safe object.
        position (list): position of mirror i.e. [row, col].
        orientation (int): 0 to signify /, 1 to signify \

    """
    row, col = position

    if safe.row_mirror_positions.get(row) is None:
        safe.row_mirror_positions[row] = []
    safe.row_mirror_positions[row].append((col, orientation))
    if safe.col_mirror_positions.get(col) is None:
        safe.col_mirror_positions[col] = []

    safe.col_mirror_positions[col].append((row, orientation))

    return safe


def prepare_safes_to_solve(config):
    """Initialise safes based on input file.

    Args:
        config: (list): list of lines read from input file.

    Returns:
        safes_to_solve (list): list of Safe.

    """
    safes_to_solve = []
    for line in config:
        line_contents = [int(item) for item in line.split(' ')]
        if len(line_contents) == 4:
            rows, cols, m, n = line_contents
            safe = Safe(rows, cols, m, n)
            safes_to_solve.append(safe)
            count = 0
        else:
            if count < m:
                safe = fill_mirror_position(safe, line_contents, 0)
            else:
                safe = fill_mirror_position(safe, line_contents, 1)
            count += 1
        print(safe.row_mirror_positions)
        print(safe.col_mirror_positions)
        print("##################################")
    return safes_to_solve


def main():
    """Run main function."""
    input_config = read_input(args.input)
    safes_to_solve = prepare_safes_to_solve(input_config)
    results_to_write = []
    for idx, safe in enumerate(safes_to_solve):
        result = safe.solve()
        result_string = "Case {}: {}".format(idx, result)
        print(result_string)
        results_to_write.append(result_string)
    write_to_file(results_to_write)


if __name__=='__main__':
    main()
