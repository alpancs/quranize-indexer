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
        self.dst.write(r'struct Harf {content: char, next_harfs: Vec<Harf>, locations: Vec<u16>}')
        self.dst.write('\n\nlet quran_index = ')

    def build(self, harf: Harf) -> None:
        self.dst.write("Harf{'%s',vec![" % harf.content)
        for i, next_harf in enumerate(harf.next_harfs):
            if i > 0:
                self.dst.write(',')
            self.build(next_harf)
        self.dst.write('],vec![')
        for i, location in enumerate(harf.locations):
            if i > 0:
                self.dst.write(',')
            self.dst.write(str(location))
        self.dst.write(']}')
