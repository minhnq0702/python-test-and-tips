""" Module add testing:
# Segment:
# start: int, end: int
# x belong (a, b] --> a < x <= b
# Input array of segments, and a query segment
# Output: is array of segments that intersect with the query segment or not
# If not, insert segment into the array
# sample
# (1, 2], (2, 4], (7, 9] -> does not overlap
# query: (4, 5] -> does not overlap
# query: (6, 7] -> does not overlap with (7, 9]
"""

import bisect
from collections import namedtuple

Segment = namedtuple('segment', ['start', 'end'])


def is_overlap(segment: Segment, query: Segment):
    """Check if the query segment intersects with the segment
    Args:
        segment (Segment): _description_
        query (Segment): _description_
    """
    if query.start < segment.end and query.end > segment.start:
        return True
    return False


def check_segement_overlap(segments: list[Segment], query: list[Segment]):
    """Input array of segments, and a query segment
    Check if the query segment intersects with any of the segments in the array
    Args:
        segment (list[Segment]): _description_
        query (list[Segment], optional): _description_. Defaults to [].
    """

    # create segment set sort by start
    segments.sort(key=lambda x: x.start)
    print(segments)
    for q in query:
        prev = None
        idx = None
        q_insertion_idx = bisect.bisect(segments, q)
        if q_insertion_idx == 0:
            idx = q_insertion_idx
            prev = None
        elif q_insertion_idx == len(segments):
            idx = q_insertion_idx - 1
            prev = None
        else:
            idx = q_insertion_idx
            prev = idx - 1

        seg_to_check = segments[idx]
        pre_seg_to_check = segments[prev] if prev is not None else None
        if is_overlap(seg_to_check, q) or (pre_seg_to_check is not None and is_overlap(pre_seg_to_check, q)):
            print(q, '--> overlap with', pre_seg_to_check, '<-->', seg_to_check)
        else:
            print(q, '--> no overlap', pre_seg_to_check, '<-->', seg_to_check)
            segments.insert(q_insertion_idx, q)


if __name__ == '__main__':
    check_segement_overlap(
        [
            Segment(1, 2),
            Segment(3, 4),
            Segment(3, 5),
            Segment(-2, 0),
            Segment(-20, -9)
        ],
        [Segment(2, 3), Segment(2, 3),  Segment(-10, -2), Segment(4, 5), Segment(99,100)]
    )

    check_segement_overlap(
        [
            Segment(1, 2),
        ],
        [
            Segment(0, 1),
        ]
    )
