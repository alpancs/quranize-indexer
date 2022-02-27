from dataclasses import dataclass
from os import path

from graphviz import Digraph

from harf import Harf


def export(harf: Harf, dst_path: str) -> None:
    graph = Digraph()
    GraphBuilder(graph, 6, 12).build(harf, '')
    file_name, extension = path.splitext(dst_path)
    graph.render(file_name, format=extension[1:], cleanup=True)


@dataclass
class GraphBuilder:
    graph: Digraph
    max_depth: int
    max_width: int

    def build(self, node: Harf, name: str, depth: int = 1) -> None:
        self.graph.node(name=name, label=f'{node.content}\n{node.locations}')
        if depth < self.max_depth:
            for child in node.next_harfs[:self.max_width]:
                self.build(child, name+child.content, depth+1)
                self.graph.edge(name, name+child.content, label=name+child.content)
