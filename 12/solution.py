import numpy as np
import cv2
import matplotlib.pyplot as plt
import clipboard
import graphviz
from typing import Set


def read_file(path):
    with open(path) as f:
        return f.read()


class node:
    def single_visit_node(self):
        return self.rep.islower()

    def __init__(self, neighbours, rep):
        self.neighbours = neighbours
        self.rep = rep

    def __repr__(self):
        return f"{self.rep} Neighbours: {len(self.neighbours)}"

    def __add__(self, string: str):
        return f"{self.rep}{string}"

    def __hash__(self):
        return self.rep.__hash__()


def build_graph_from_string(string: str):
    node_map = {}
    for n in string.strip().split("\n"):
        nodes = n.strip().split("-")
        for no in nodes:
            node_map[no] = node([], no)
    for n in string.strip().split("\n"):
        nodes = n.strip().split("-")
        a, b = nodes
        node_map[a].neighbours.append(node_map[b])
        node_map[b].neighbours.append(node_map[a])
    return node_map


def vis_graph(root_node):
    g = graphviz.Digraph(comment="Caves")
    g.graph_attr["splines"] = "ortho"

    def add_edge(node, graph, edges):
        for n in node.neighbours:
            if (node.rep + "-" + n.rep) in edges:
                continue
            graph.edge(node.rep, n.rep, arrowhead="both")
            edges.append(node.rep + "-" + n.rep)
            add_edge(n, graph, edges)

    add_edge(root_node, g, [])
    g.render("graph.pdf", view=True)


def traverse(n: node, visited: Set[node], path=""):
    if n.rep == "end":
        path = path + "start"
        yield path
    else:
        for neighbour in n.neighbours:
            if neighbour.single_visit_node():
                if neighbour not in visited:
                    yield from traverse(
                        neighbour, visited | {neighbour}, neighbour + "-" + path
                    )
            else:
                yield from traverse(neighbour, visited, neighbour + "-" + path)


def double_visit_traverse(
    n: node, visited: Set[node], double_visit_exhausted: bool, path=""
):
    if n.rep == "end":
        path = path + "start"
        yield path
    else:
        for neighbour in n.neighbours:
            if neighbour.single_visit_node():
                if neighbour not in visited:
                    yield from double_visit_traverse(
                        neighbour,
                        visited | {neighbour},
                        double_visit_exhausted,
                        neighbour + "-" + path,
                    )
                elif not double_visit_exhausted and neighbour.rep not in {"start", "end"}:
                    yield from double_visit_traverse(
                        neighbour, visited, True, neighbour + "-" + path
                    )
            else:
                yield from double_visit_traverse(
                    neighbour, visited, double_visit_exhausted, neighbour + "-" + path
                )


def solve_1(data) -> int:
    paths = set()
    graph = build_graph_from_string(data)
    top_node = graph["start"]
    visited = {top_node}
    return len(list(traverse(top_node, visited)))


def solve_2(data) -> int:
    paths = set()
    graph = build_graph_from_string(data)
    top_node = graph["start"]
    visited = {top_node}
    vis_graph(top_node)
    return len(
        list(double_visit_traverse(top_node, visited, double_visit_exhausted=False))
    )


count = 0


if __name__ == "__main__":
    eval_sample = False

    sample_data = read_file("sample.txt")
    input_data = read_file("input.txt")

    width = 35
    data = sample_data if eval_sample else input_data
    if eval_sample:
        print(f"{'SAMPLE':-^{width}}")
    else:
        print(f"{'SOLUTION':-^{width}}")
    print("*:", end=" ")
    solution1 = solve_1(data)
    print(solution1)
    print("-" * width)
    print("**:", end=" ")
    solution2 = solve_2(data)
    print(solution2)
    print("-" * width)
    if not eval_sample:
        image = np.zeros((50, 400))
        image = cv2.putText(
            image,
            "Copy Solution 1 or 2 to clipboard? (1/2)",
            (20, 24),
            cv2.FONT_HERSHEY_PLAIN,
            1,
            (255, 255, 255),
            1,
        )
        image = cv2.putText(
            image,
            f"*: {solution1}",
            (20, 42),
            cv2.FONT_HERSHEY_PLAIN,
            1,
            (255, 255, 255),
            1,
        )
        image = cv2.putText(
            image,
            f"**: {solution2}",
            (200, 42),
            cv2.FONT_HERSHEY_PLAIN,
            1,
            (255, 255, 255),
            1,
        )
        cv2.imshow("Copy results?", image)
        key = cv2.waitKey()
        if key == ord("1"):
            clipboard.copy(str(solution1))
            print("* has been copied to clipboard!")
        elif key == ord("2"):
            clipboard.copy(str(solution2))
            print("** has been copied to clipboard!")
        else:
            print("Nothing copied to clipboard!")
        cv2.destroyAllWindows()
