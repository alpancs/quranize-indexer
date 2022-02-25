from xml.etree import ElementTree

import click

from harf import Harf


@click.command()
@click.argument('xml-path', type=click.Path(dir_okay=False))
def main(xml_path: str):
    quran = ElementTree.parse(xml_path).getroot()
    print(build_suffix_tree(quran).size()/1e6)
    print(len(build_location_map(quran)))


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
