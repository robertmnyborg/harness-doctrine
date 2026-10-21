"""Deterministic US street-address matcher (the "v3" normalizer from the eval).

match(a1, a2) -> (bool, reason)

Rules, in order:
  1. Normalize: strip accents, punctuation and trailing unit designators,
     expand street suffixes (St -> street), ordinals (34th -> 34, first -> 1).
  2. Split directionals (N, NE, North...) out of the core.
  3. Any difference in the numeric tokens is a different property (34th vs 39th).
  4. Cores must be equal or fuzzy-equal (token_sort_ratio >= 90).
  5. Directionals conflict only when BOTH sides have them and neither set
     contains the other. A directional present on one side only is fine.
"""
import re
import unicodedata

from rapidfuzz import fuzz

SUFFIX = {
    'st': 'street', 'str': 'street', 'ave': 'avenue', 'av': 'avenue', 'blvd': 'boulevard',
    'rd': 'road', 'dr': 'drive', 'ln': 'lane', 'ct': 'court', 'cir': 'circle', 'pl': 'place',
    'pkwy': 'parkway', 'pky': 'parkway', 'pkw': 'parkway', 'hwy': 'highway', 'ter': 'terrace',
    'trl': 'trail', 'sq': 'square', 'plz': 'plaza', 'cv': 'cove', 'xing': 'crossing',
    'pt': 'point', 'expy': 'expressway', 'expwy': 'expressway', 'fwy': 'freeway',
    'tpke': 'turnpike', 'bnd': 'bend', 'crk': 'creek', 'vw': 'view', 'vlg': 'village',
    'mnr': 'manor', 'frst': 'forest', 'gln': 'glen', 'rdg': 'ridge', 'spgs': 'springs',
    'hls': 'hills', 'lndg': 'landing', 'grn': 'green', 'gdns': 'gardens', 'cmn': 'common',
    'ctr': 'center', 'ctre': 'center', 'pointe': 'point', 'hts': 'heights', 'mt': 'mount',
    'ft': 'fort',
}
ORDINAL = {'first': '1', 'second': '2', 'third': '3', 'fourth': '4', 'fifth': '5',
           'sixth': '6', 'seventh': '7', 'eighth': '8', 'ninth': '9', 'tenth': '10'}
DIRECTION = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west',
             'ne': 'northeast', 'nw': 'northwest', 'se': 'southeast', 'sw': 'southwest'}
DIRECTIONS = set(DIRECTION) | set(DIRECTION.values())
UNIT = re.compile(r'\b(apt|apartment|unit|ste|suite|bldg|building|#)\s*[\w-]*\.?$', re.I)


def tokens(address):
    a = unicodedata.normalize('NFKD', address or '').encode('ascii', 'ignore').decode()
    a = a.lower().replace('.', ' ').replace(',', ' ')
    a = UNIT.sub(' ', a)
    a = re.sub(r'[^a-z0-9 ]', ' ', a)
    out = []
    for t in a.split():
        t = SUFFIX.get(t, t)
        t = re.sub(r'^(\d+)(st|nd|rd|th)$', r'\1', t)
        out.append(ORDINAL.get(t, t))
    return out


def core_and_directions(address):
    core, dirs = [], set()
    for t in tokens(address):
        if t in DIRECTIONS:
            dirs.add(DIRECTION.get(t, t))
        else:
            core.append(t)
    return core, dirs


def match(a1, a2):
    c1, d1 = core_and_directions(a1)
    c2, d2 = core_and_directions(a2)
    if [t for t in c1 if t.isdigit()] != [t for t in c2 if t.isdigit()]:
        return False, 'number-differs'
    s1, s2 = ' '.join(c1), ' '.join(c2)
    if s1 != s2 and fuzz.token_sort_ratio(s1, s2) < 90:
        return False, 'core-differs'
    if d1 and d2 and not (d1 <= d2 or d2 <= d1):
        return False, 'directional-conflict'
    return True, 'ok'
