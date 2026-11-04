import os
import random
import tempfile
import unittest

from pa1 import gale_shapley

HERE = os.path.dirname(os.path.abspath(__file__))


def write_instance(path, caps, hosp_prefs, stud_prefs):
    lines = [f"{len(caps)} {len(stud_prefs)}", " ".join(map(str, caps))]
    lines += [" ".join(map(str, p)) for p in hosp_prefs]
    lines += [" ".join(map(str, p)) for p in stud_prefs]
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def random_instance(rng, partial):
    H, S = rng.randint(1, 8), rng.randint(1, 12)
    caps = [rng.randint(0, 4) for _ in range(H)]
    hp = [rng.sample(range(S), rng.randint(0, S) if partial else S) for _ in range(H)]
    sp = [rng.sample(range(H), rng.randint(0, H) if partial else H) for _ in range(S)]
    return caps, hp, sp


def is_stable(caps, hp, sp, match):
    """Valid (capacity, mutual acceptability) and no blocking pair."""
    H = len(caps)
    assigned = [[s for s, h in enumerate(match) if h == hh] for hh in range(H)]
    for h in range(H):
        if len(assigned[h]) > caps[h]:
            return False
    for s, h in enumerate(match):
        if h is not None and (h not in sp[s] or s not in hp[h]):
            return False
    for h in range(H):
        for s in hp[h]:
            if h not in sp[s] or match[s] == h:
                continue
            # student s prefers h to current match (or is unmatched)?
            s_prefers = match[s] is None or sp[s].index(h) < sp[s].index(match[s])
            if not s_prefers:
                continue
            # hospital h has a free seat or prefers s to a current student?
            if len(assigned[h]) < caps[h]:
                return False
            if any(hp[h].index(s) < hp[h].index(t) for t in assigned[h]):
                return False
    return True


class TestGaleShapley(unittest.TestCase):
    def test_sample(self):
        with open(os.path.join(HERE, "solution8.txt")) as f:
            expected = [int(x) for x in f.read().split()]
        self.assertEqual(gale_shapley(os.path.join(HERE, "input8.txt")), expected)

    def test_random_instances_are_stable(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "in.txt")
            for seed in range(300):
                rng = random.Random(seed)
                inst = random_instance(rng, partial=bool(seed % 2))
                write_instance(path, *inst)
                self.assertTrue(is_stable(*inst, gale_shapley(path)), f"seed {seed}")


if __name__ == "__main__":
    unittest.main()
