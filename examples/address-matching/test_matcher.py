import json
import os
import unittest

from eval import hard_negatives, precision, recall
from matcher import match

HERE = os.path.dirname(os.path.abspath(__file__))
PAIRS = json.load(open(os.path.join(HERE, 'fixtures', 'pairs.json')))


class MatcherTest(unittest.TestCase):
    def test_fixture_pairs(self):
        for p in PAIRS:
            with self.subTest(case=p['case']):
                ok, why = match(p['a1'], p['a2'])
                expected = bool(p['label']) and not p.get('known_miss')
                self.assertEqual(ok, expected)
                self.assertEqual(why, p['why'])

    def test_symmetric(self):
        for p in PAIRS:
            self.assertEqual(match(p['a1'], p['a2'])[0], match(p['a2'], p['a1'])[0])


class EvalTest(unittest.TestCase):
    def test_hard_negatives_keep_only_150_to_600m(self):
        # 0.001 deg latitude is ~111m
        records = [
            {'id': 1, 'address': '10 Quillfeather St', 'lat': 0.0000, 'lng': 0.0},
            {'id': 2, 'address': '10 Quillfeather Street', 'lat': 0.0005, 'lng': 0.0},  # ~56m: too close
            {'id': 3, 'address': '40 Quillfeather St', 'lat': 0.0030, 'lng': 0.0},      # ~333m: kept
            {'id': 4, 'address': '90 Quillfeather St', 'lat': 0.0100, 'lng': 0.0},      # ~1.1km: too far
        ]
        negs = hard_negatives(records)
        self.assertEqual(sorted(negs), sorted([('10 Quillfeather St', '40 Quillfeather St'),
                                               ('10 Quillfeather Street', '40 Quillfeather St')]))
        self.assertEqual(precision(negs)[0], 1.0)

    def test_recall_counts_known_miss(self):
        positives = [p for p in PAIRS if p['label'] == 1]
        r, misses = recall(positives)
        self.assertEqual(len(misses), 1)
        self.assertTrue(misses[0]['known_miss'])


if __name__ == '__main__':
    unittest.main()
