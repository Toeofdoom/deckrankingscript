import choix
import numpy as np

def infer_rankings(entries, f=None):
    np.set_printoptions(precision=3, suppress=True)

    parsed_entries = []
    for line in entries:
        values = line.split("\t")
        if len(values) < 4:
            print(f"match data incomplete {line}")
            continue

        a, aScore, b, bScore = values
        parsed_entries.append((a, aScore, b, bScore))

    if f:
        parsed_entries = f(parsed_entries)

    indexes = {}
    matches = []
    for a, aScore, b, bScore in parsed_entries:
        try:
            if a not in indexes:
                indexes[a] = len(indexes)
            if b not in indexes:
                indexes[b] = len(indexes)
            
            if int(aScore) > int(bScore):
                matches.append((indexes[a], indexes[b]))
            else:
                matches.append((indexes[b], indexes[a]))
        except:
            print(f"match data incomplete {line}")
    
    params = choix.ilsr_pairwise(len(indexes), matches, alpha=0.0001, max_iter=100)

    return dict([(name, 1200 + params[indexes[name]] * 120) for name in sorted(indexes, key = lambda name: -params[indexes[name]])])

def main():
    data = """Engihot	3	Ghostwriter	2
Engihot	3	Givaqueen	0
Engihot	2	Fanpenny	3
Engihot	3	Jones	2
Engihot	3	Spacehook	1
Engihot	3	Haukea	1
Engihot	2	Lysander	3
Ghostwriter	2	Fanpenny	3
Givaqueen	3	Fanpenny	1
Givaqueen	3	Spacehook	1
Givaqueen	3	Haukea	0
Givaqueen	2	Lysander	3
Fanpenny	2	Spacehook	3
Fanpenny	1	Haukea	3
"""

    rankings = infer_rankings(data.splitlines())
    for name in rankings:
        print(f'{name}, {rankings[name]}')

if __name__ == '__main__':
    main()