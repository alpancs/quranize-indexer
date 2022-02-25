from xml.etree import ElementTree

import click

import harf


@click.command()
@click.argument('xml-path', type=click.Path(dir_okay=False))
def main(xml_path: str):
    quran = ElementTree.parse(xml_path).getroot()
    quran_index = build_suffix_tree(quran)
    print(f'quran_index.content = "{quran_index.content}"')
    for next_harf in quran_index.next_harfs:
        print(f'    next_harf.content = "{next_harf.content}", len(next_harf.locations) = {len(next_harf.locations)}')
    print(f'quran_index.size() = {quran_index.size()}')
    location_map = build_location_map(quran)
    print(f'len(location_map) = {len(location_map)}')


def build_suffix_tree(quran: ElementTree.Element) -> harf.Harf:
    root = harf.Harf('')
    location = 0
    for sura in quran:
        for aya in sura:
            update_tree(root, location, aya.get('text'))
            location += 1
    return root


def update_tree(root: harf.Harf, location: int, aya: str):
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
