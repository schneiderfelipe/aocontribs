import sys

import cclib

__version__ = "0.1.0"

THRESHOLD = 0.01


def main(filepath: str, atom: str, n: int):
    data = cclib.io.ccopen(filepath).parse()
    ihomo = data.homos[0] + n

    imax = len(data.moenergies[0]) - 1
    if not (0 <= ihomo <= imax):
        raise ValueError(
            f"Attempt to index MO #{ihomo} when only {0}-{imax} (inclusive) available"
        )

    homo_alpha = data.mocoeffs[0][ihomo, :]
    if n == 0:
        print(f"HOMO(α): #{ihomo}")
    elif n == 1:
        print(f"LUMO(α): #{ihomo}")
    elif n > 1:
        print(f"LUMO{n-1:+}(α): #{ihomo}")
    else:
        print(f"HOMO{n:+}(α): #{ihomo}")
    print(f"Only contributions greater than {THRESHOLD} shown")

    contribs = []
    for (i, orbital) in enumerate(data.aonames):
        if orbital.startswith(atom):
            coeff = homo_alpha[i]
            contribs.append((orbital, i, coeff, coeff**2))

    contribs = sorted(contribs, key=lambda e: -e[3])
    for (orbital, i, coeff, p) in contribs:
        if p > THRESHOLD:
            print(f"{orbital:10s} (#{i:2d}): " f"({coeff:+1.4f})² = {p:1.4f}")


def cli():
    if len(sys.argv) not in (3, 4):
        progname = sys.argv[0].split("/")[-1]
        print(f"Usage: {progname} <filepath> <atom> [<n>]")
        print("\nExamples:")
        print(f"  {progname} test/water.out O1     # HOMO by default")
        print(f"  {progname} test/water.out O1 +1  # LUMO")
        print(f"  {progname} test/water.out O1 -1  # HOMO-1")
        sys.exit(1)

    filepath = sys.argv[1]
    atom = sys.argv[2]
    if len(sys.argv) > 3:
        n = int(sys.argv[3])
    else:
        n = 0
    main(filepath, atom, n)


if __name__ == "__main__":
    cli()
