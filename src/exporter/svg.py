from dataclasses import dataclass

from graphviz import Digraph

from harf import Harf


def export(harf: Harf, dst_path: str) -> None:
    graph = build_graph(harf, 7, 2)
    graph.render(dst_path.rstrip('.svg'), format='svg', cleanup=True)


def build_graph(harf: Harf, max_depth: int, max_width: int) -> Digraph:
    graph = Digraph()
    GraphBuilder(graph, max_depth, max_width).build(harf, harf.content)
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
