class Harf:
    def __init__(self, content: chr):
        self.content = content
        self.next_harfs: list[Harf] = []
        self.locations: list[int] = []

    def get_or_add_next_harf(self, harf: chr) -> 'Harf':
        next_harf = self.get_next_harf(harf)
        if next_harf is None:
            next_harf = Harf(harf)
            self.next_harfs.append(next_harf)
        return next_harf

    def get_next_harf(self, harf: chr) -> 'Harf':
        for next_harf in self.next_harfs:
            if next_harf.content == harf:
                return next_harf

    from sys import setrecursionlimit
    setrecursionlimit(10000)

    def size(self) -> int:
        return sum([h.size() for h in self.next_harfs], start=1)

    def __repr__(self):
        return f'"{self.content}", {self.locations}, {self.next_harfs}'
