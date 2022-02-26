class Harf:
    def __init__(self, content: chr) -> None:
        self.content = content
        self.next_harfs: list[Harf] = []
        self.locations: list[int] = []

    def get_or_add_next_harf(self, content: chr) -> 'Harf':
        for next_harf in self.next_harfs:
            if next_harf.content == content:
                return next_harf
        self.next_harfs.append(Harf(content))
        return self.next_harfs[-1]
