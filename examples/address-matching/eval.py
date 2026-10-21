"""Recall / precision harness for any address matcher.

positives: [{"a1", "a2"}]   pairs known to be the same property
records:   [{"id", "address", "lat", "lng"}]   one row per distinct property

Hard negatives are distinct properties 150-600m apart: close enough to share
street names and number ranges, far enough to be different buildings. A
coarse lat/lng grid keeps the neighbour search linear (an unindexed spatial
self-join in SQL timed out).

Usage: python eval.py positives.json records.json
"""
import json
import math
import sys
from collections import defaultdict

from matcher import match

CELL = 0.006  # degrees, ~660m


def haversine_m(la1, lo1, la2, lo2):
    p1, p2 = math.radians(la1), math.radians(la2)
    x = (math.sin((p2 - p1) / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lo2 - lo1) / 2) ** 2)
    return 2 * 6371000.0 * math.asin(math.sqrt(x))


def hard_negatives(records, lo=150.0, hi=600.0):
    grid = defaultdict(list)
    for r in records:
        grid[(int(r['lat'] / CELL), int(r['lng'] / CELL))].append(r)
    out = []
    for r in records:
        ci, cj = int(r['lat'] / CELL), int(r['lng'] / CELL)
        for i in (ci - 1, ci, ci + 1):
            for j in (cj - 1, cj, cj + 1):
                for s in grid.get((i, j), ()):
                    if s['id'] > r['id'] and lo <= haversine_m(r['lat'], r['lng'], s['lat'], s['lng']) <= hi:
                        out.append((r['address'], s['address']))
    return out


def recall(positives, fn=match):
    misses = [p for p in positives if not fn(p['a1'], p['a2'])[0]]
    return 1 - len(misses) / len(positives), misses


def precision(negatives, fn=match):
    false_pos = [n for n in negatives if fn(*n)[0]]
    return 1 - len(false_pos) / len(negatives), false_pos


if __name__ == '__main__':
    pos = json.load(open(sys.argv[1]))
    neg = hard_negatives(json.load(open(sys.argv[2])))
    r, misses = recall(pos)
    p, fps = precision(neg)
    print(f"recall    {r:.2%}  ({len(misses)} missed of {len(pos)})")
    print(f"precision {p:.2%}  ({len(fps)} false positives of {len(neg)} hard negatives)")
