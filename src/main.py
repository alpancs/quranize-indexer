from xml.etree import ElementTree

import click
import graphviz

from harf import Harf


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


def debug(quran_index: Harf, location_map: list[tuple[int, int]]) -> None:
    graph = build_graph(quran_index, 7, 2)
    graph.render('quran_index', format='svg', cleanup=True)
    graph.render('quran_index', format='png', cleanup=True)
    print(f'len(location_map) = {len(location_map)}')


def build_graph(harf: Harf, max_depth: int, max_width: int) -> graphviz.Digraph:
    graph = graphviz.Digraph()
    _build_graph(harf, harf.content, 1, max_depth, max_width, graph)
    return graph


def _build_graph(node: Harf, name: str, depth: int, max_depth: int, max_width: int, graph: graphviz.Digraph) -> None:
    graph.node(name=name, label=f'{node.content}\n{len(node.locations)}')
    if depth < max_depth:
        for child in node.next_harfs[:max_width]:
            _build_graph(child, name+child.content, depth+1, max_depth, max_width, graph)
            graph.edge(name, name+child.content, label=name+child.content)


if __name__ == '__main__':
    main()
