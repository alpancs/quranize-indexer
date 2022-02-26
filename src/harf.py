from dataclasses import dataclass, field


@dataclass
class Harf:
    content: chr
    next_harfs: list['Harf'] = field(default_factory=list)
    locations: list[int] = field(default_factory=list)

    def get_or_add_next_harf(self, content: chr) -> 'Harf':
        for next_harf in self.next_harfs:
            if next_harf.content == content:
                return next_harf
        self.next_harfs.append(Harf(content))
        return self.next_harfs[-1]
