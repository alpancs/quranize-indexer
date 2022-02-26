from dataclasses import dataclass

from graphviz import Digraph

from harf import Harf


def debug(quran_index: Harf, location_map: list[tuple[int, int]]) -> None:
    graph = build_graph(quran_index, 7, 2)
    graph.render('debug/quran_index', format='svg', cleanup=True)
    graph.render('debug/quran_index', format='png', cleanup=True)
    print(f'len(location_map) = {len(location_map)}')


def build_graph(harf: Harf, max_depth: int, max_width: int) -> Digraph:
    graph = Digraph()
    GraphBuilder(graph, 7, 2).build(harf, harf.content)
    return graph


@dataclass
class GraphBuilder:
    graph: Digraph
    max_depth: int
    max_width: int

    def build(self, node: Harf, name: str, depth: int = 1) -> None:
        self.graph.node(name=name, label=f'{node.content}\n{len(node.locations)}')
        if depth < self.max_depth:
            for child in node.next_harfs[:self.max_width]:
                self.build(child, name+child.content, depth+1)
                self.graph.edge(name, name+child.content, label=name+child.content)
