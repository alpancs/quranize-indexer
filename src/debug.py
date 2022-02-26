from graphviz import Digraph

from harf import Harf


def debug(quran_index: Harf, location_map: list[tuple[int, int]]) -> None:
    graph = build_graph(quran_index, 7, 2)
    graph.render('debug/quran_index', format='svg', cleanup=True)
    graph.render('debug/quran_index', format='png', cleanup=True)
    print(f'len(location_map) = {len(location_map)}')


def build_graph(harf: Harf, max_depth: int, max_width: int) -> Digraph:
    graph = Digraph()
    _build_graph(harf, harf.content, 1, max_depth, max_width, graph)
    return graph


def _build_graph(node: Harf, name: str, depth: int, max_depth: int, max_width: int, graph: Digraph) -> None:
    graph.node(name=name, label=f'{node.content}\n{len(node.locations)}')
    if depth < max_depth:
        for child in node.next_harfs[:max_width]:
            _build_graph(child, name+child.content, depth+1, max_depth, max_width, graph)
            graph.edge(name, name+child.content, label=name+child.content)
