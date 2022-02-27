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

    def build(self, harf: Harf, depth: int = 1) -> None:
        self.dst.write(f"{'  '*(depth-1)}Harf {{'{harf.content}', vec![")
        if harf.next_harfs:
            self.dst.write('\n')
            for next_harf in harf.next_harfs:
                self.build(next_harf, depth+1)
                self.dst.write(',\n')
            self.dst.write(f"{'  '*(depth-1)}], vec!{harf.locations}}}")
        else:
            self.dst.write(f"], vec!{harf.locations}}}")
