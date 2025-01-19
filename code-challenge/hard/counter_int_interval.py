import bisect
from collections import namedtuple
from operator import itemgetter

Interval = namedtuple("Interval", ["start", "end"])


class CountIntervals:
    """List intervals"""
    intervals: list[Interval]
    _count: int
    starts: list[int]

    def __init__(self):
        self.intervals = []
        self._count = 0

    def _check_collapse(self, source_int: Interval, dest_int: Interval):
        if source_int.end >= dest_int.start and dest_int.end >= source_int.start:
            return True
        return False

    def add(self, left: int, right: int) -> None:
        """add new interval

        Args:
            left (int): _description_
            right (int): _description_
        """
        new_interval = Interval(left, right)
        index = max(bisect.bisect_left(self.intervals, new_interval), 0)

        # check collapse before insert
        check_interval = new_interval

        def _add(_i: int, _interval: Interval):
            self.intervals.insert(_i, _interval)
            self._count += (_interval.end+1 - _interval.start)

        def _remove(_interval: Interval):
            self.intervals.remove(_interval)
            self._count -= (_interval.end+1 - _interval.start)

        while index < len(self.intervals):
            # * check right
            overlap = self._check_collapse(
                self.intervals[index], check_interval)
            if overlap:
                check_interval = Interval(
                    check_interval.start,
                    max(check_interval.end, self.intervals[index].end)
                )
                _remove(self.intervals[index])
            else:
                break

        while index > 0:
            # * check left
            overlap = self._check_collapse(
                self.intervals[index - 1], check_interval)
            if overlap:
                check_interval = Interval(
                    self.intervals[index - 1].start,
                    max(check_interval.end, self.intervals[index - 1].end)
                )
                _remove(self.intervals[index - 1])
                index -= 1
            else:
                break
        _add(index, check_interval)

    def add_new(self, start: int, end: int) -> None:
        """Enhance solution

        Args:
            start (int): _description_
            end (int): _description_
        """

        def _add(from_idx, to_idx: int, _interval: Interval):
            for _ in self.intervals[from_idx:to_idx]:
                self._count -= _.end - _.start + 1
            self.intervals[from_idx:to_idx] = [_interval]
            self._count += _interval.end - _interval.start + 1

        if not self.intervals:
            _add(0, 0, Interval(start, end))
            return

        start_idx = bisect.bisect_left(self.intervals, start, key=itemgetter(1))
        end_idx = bisect.bisect_right(self.intervals, end, key=itemgetter(0))

        len_arr = len(self.intervals)

        if start_idx == len_arr and end_idx == len_arr:
            _add(len_arr, len_arr, Interval(start, end))
            return

        if start_idx == 0 and end_idx == 0:
            _add(0, 0, Interval(start, end))
            return

        new_interval_start = min(self.intervals[start_idx].start, start)
        new_interval_end = max(self.intervals[end_idx - 1].end, end)
        _add(start_idx, end_idx, Interval(new_interval_start, new_interval_end))

        return None

    def count(self) -> int:
        """Count the item exists in only one interval

        Returns:
            int: _description_
        """
        return self._count


# Your CountIntervals object will be instantiated and called as such:
obj = CountIntervals()
for interval in [[],[10,27],[46,50],[15,35],[12,32],[7,15],[49,49],[]]:
    if interval:
        # obj.add(interval[0], interval[1])
        obj.add_new(interval[0], interval[1])
        # print("[minhne]", f"{None}")
    else:
        print("[minhne]", f"{obj.count()}")

print(obj.intervals)
