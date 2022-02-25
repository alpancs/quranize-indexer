from xml.etree import ElementTree

import click

from harf import Harf


@click.command()
@click.argument('xml-path', type=click.Path(dir_okay=False))
def main(xml_path: str):
    from datetime import datetime
    quran = ElementTree.parse(xml_path).getroot()
    t1 = datetime.now()
    quran_index = build_suffix_tree(quran)
    t2 = datetime.now()
    print(t2-t1)
    print(quran_index.size()/1e6)
    print(datetime.now()-t2)
    build_location_map(quran)


def build_suffix_tree(quran: ElementTree.Element) -> Harf:
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
                    node.add_location(location)


def build_location_map(quran: ElementTree.Element) -> list[tuple[int, int]]:
    return [
        (int(sura.get('index')), int(aya.get('index')))
        for sura in quran for aya in sura
    ]


if __name__ == '__main__':
    main()
