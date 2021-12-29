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
    root = False
    neighbours = None
    is_small = False
    rep = ""
    visitable = True

    def is_single_visit(self):
        return self.rep.islower()

    def __init__(self, neighbours, rep, root=False):
        self.neighbours = neighbours
        self.rep = rep
        self.root = root

    def __repr__(self):
        return f"{self.rep} Neighbours: {len(self.neighbours)}"


def build_graph_from_string(string: str):
    node_map = {}
    for n in string.strip().split("\n"):
        nodes = n.strip().split("-")
        for no in nodes:
            node_map[no] = node([], no)
    node_map["start"].root = True
    for n in string.strip().split("\n"):
        nodes = n.strip().split("-")
        a, b = nodes
        node_map[a].neighbours.append(node_map[b])
        node_map[b].neighbours.append(node_map[a])
    return node_map["start"]


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
    g.render("test.pdf", view=True)



def traverse(n: node, visited: Set[node], path: str = ""):
    global count
    if n.is_single_visit():
        visited.add(n)
    if n.rep == "end":
        count += 1
        #print((path + "-end")[1:])
        return
    for neighbour in n.neighbours:
        if neighbour not in visited:
            visited_c = visited.copy()
            if neighbour.is_single_visit():
                visited_c.add(neighbour)
            traverse(neighbour, visited_c, path + "-" + n.rep)


def solve_1(data) -> int:
    node = build_graph_from_string(data)
    # vis_graph(node)
    visited = set()
    traverse(node, visited)
    return count


def solve_2(data) -> int:
    return 25


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
