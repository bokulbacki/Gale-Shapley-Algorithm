# Name: pa1.py
# Author(s): Ben Berube and Bo Kulbacki
# Date: 02.20.2023
# Description: Implementation of the Gale-Shapley stable matching algorithm.


def gale_shapley(filename):
    """
    Runs Gale-Shapley algorithm on input
    from file filename.  Format of input file
    given in problem statement.
    Returns a list containing hospitals assigned to each
    student, or None if a student is not assigned to a hospital.

    Runs in O(n^2) worst-case time and space (n = max(hospitals, students)),
    i.e. O(H + S + P) with P the total preference-list length (P <= 2n^2): every
    hospital proposes to each student at most once, and every proposal is
    resolved with O(1) dictionary/array lookups.
    """

    # ----PRE PROCESSING----
    with open(filename, "r") as f:
        lines = f.read().split("\n")

    def row(i):
        # Preference lists may be empty, so index by line rather than by token.
        return lines[i].split() if i < len(lines) else []

    header = row(0)
    num_hospitals = int(header[0])
    num_students = int(header[1])

    # remaining[h]: open positions left at hospital h
    remaining = [int(c) for c in row(1)[:num_hospitals]]

    # hospital_prefs[h]: students in h's preference order; next_idx[h] is the
    # next student h will propose to (replaces O(n) list.pop(0)).
    hospital_prefs = [[int(s) for s in row(2 + h)] for h in range(num_hospitals)]
    next_idx = [0] * num_hospitals

    # student_rank[s][h]: rank of hospital h for student s (lower is better);
    # missing key means h is unacceptable to s. Built in O(len(list)) instead of
    # calling list.index() once per hospital.
    student_rank = []
    base = 2 + num_hospitals
    for s in range(num_students):
        student_rank.append({int(h): r for r, h in enumerate(row(base + s))})

    final_pairing = [None] * num_students  # student as index

    # ----GALE SHAPLEY STARTS NOW----
    # Only hospitals that can still propose are placed on the stack.
    free = [h for h in range(num_hospitals) if remaining[h] > 0 and hospital_prefs[h]]

    while free:
        h = free.pop()
        prefs = hospital_prefs[h]
        n = len(prefs)
        i = next_idx[h]
        # Propose until h is full or has exhausted its list; no re-queueing needed.
        while remaining[h] > 0 and i < n:
            s = prefs[i]
            i += 1
            rank = student_rank[s]
            if h not in rank:
                continue  # student finds h unacceptable
            cur = final_pairing[s]
            if cur is None:
                final_pairing[s] = h
                remaining[h] -= 1
            elif rank[h] < rank[cur]:
                # Student prefers h: switch, freeing a seat at the old hospital.
                final_pairing[s] = h
                remaining[h] -= 1
                remaining[cur] += 1
                if next_idx[cur] < len(hospital_prefs[cur]):
                    free.append(cur)
        next_idx[h] = i

    return final_pairing
