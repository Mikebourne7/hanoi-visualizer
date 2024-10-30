"""Tower of Hanoi solver."""


def solve(disks):
    """Return the minimum moves as zero-indexed (source, target) pairs."""
    if not 1 <= disks <= 10:
        raise ValueError("Choose a disk count from 1 to 10.")

    def transfer(count, source, target, spare):
        if count:
            yield from transfer(count - 1, source, spare, target)
            yield source, target
            yield from transfer(count - 1, spare, target, source)

    return list(transfer(disks, 0, 2, 1))
