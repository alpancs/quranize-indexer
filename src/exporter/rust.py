import typing

from harf import Harf


def export(harf: Harf, dst_path: str) -> None:
    with open(dst_path, 'w') as dst_file:
        builder = RustBuilder(dst_file)
        builder.build(harf)
        builder.dst.write(';\n')


class RustBuilder:
    def __init__(self, dst: typing.TextIO) -> None:
        self.dst = dst
        self.dst.write('struct Harf {content: char, next_harfs: Vec<Harf>, locations: Vec<u16>}\n\n')
        self.dst.write('let quran_index = ')

    def build(self, harf: Harf) -> None:
        self.dst.write(f"Harf {{'{harf.content}', vec![")
        for i, next_harf in enumerate(harf.next_harfs):
            if i > 0:
                self.dst.write(', ')
            self.build(next_harf)
        self.dst.write(f"], vec!{harf.locations}}}")
