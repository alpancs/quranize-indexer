from xml.etree import ElementTree

import click

from harf import Harf
from debug import debug


@click.command()
@click.argument('quran-xml-path', type=click.Path(dir_okay=False))
def main(quran_xml_path: str) -> None:
    quran = ElementTree.parse(quran_xml_path).getroot()
    quran_index = build_quran_index(quran)
    location_map = build_location_map(quran)
    debug(quran_index, location_map)


def build_quran_index(quran: ElementTree.Element) -> Harf:
    root = Harf('')
    location = 0
    for sura in quran:
        for aya in sura:
            update_tree(root, location, aya.get('text'))
            location += 1
    return root


def update_tree(root: Harf, location: int, aya: str):
    for i in range(len(aya)):
        if i == 0 or aya[i-1] == ' ':
            node = root
            for j in range(i, len(aya)):
                node = node.get_or_add_next_harf(aya[j])
                if j == len(aya)-1 or aya[j+1] == ' ':
                    node.locations.append(location)


def build_location_map(quran: ElementTree.Element) -> list[tuple[int, int]]:
    return [
        (int(sura.get('index')), int(aya.get('index')))
        for sura in quran for aya in sura
    ]


if __name__ == '__main__':
    main()
