import sys

import cclib

__version__ = "0.1.0"


def main(filepath: str, atom: str):
    data = cclib.io.ccopen(filepath).parse()

    ihomo = data.homos[0]
    homo_alpha = data.mocoeffs[0][ihomo, :]
    print(f"HOMO(α): #{ihomo}")
    print("Only non-zero contributions shown")

    contribs = []
    for (i, orbital) in enumerate(data.aonames):
        if orbital.startswith(atom):
            coeff = homo_alpha[i]
            contribs.append((orbital, i, coeff))

    contribs = sorted(contribs, key=lambda e: -e[2] ** 2)
    for (orbital, i, coeff) in contribs:
        if coeff**2 > 0:
            print(f"{orbital:10s} (#{i:2d}): " f"({coeff:+1.4f})² = {coeff**2:1.4f}")


def cli():
    if len(sys.argv) != 3:
        progname = sys.argv[0].split("/")[-1]
        print(f"Usage: {progname} <filepath> <atom>")
        print("\nExample:")
        print(f"  {progname} test/water.out O1")
        sys.exit(1)

    filepath = sys.argv[1]
    atom = sys.argv[2]
    main(filepath, atom)


if __name__ == "__main__":
    cli()
