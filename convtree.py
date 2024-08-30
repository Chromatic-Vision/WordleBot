from __future__ import annotations

import os
from dataclasses import dataclass, field


with open('tree') as file:
    raw = file.read()


out = []


def remove_start(s: str, amount: int) -> str:
    s2 = []
    for string in s.split('\n'):
        if not string:
            continue
        s3 = string[amount:]
        if not s3:
            raise ValueError(repr(string))
        s2.append(s3)
    s = s2
    del s2, s3, string
    return '\n'.join(s)


def keep_start(s: str, amount: int) -> str:
    s2 = []
    for string in s.split('\n'):
        if not string:
            continue
        s3 = string[:amount].replace(' ', '')
        if not s3:
            continue
        s2.append(s3)
    return '\n'.join(s2)


@dataclass
class Node:
    word: str | None
    children: dict[str, Node] = field(default_factory=dict)


# def write(s: str, offset: int) -> list[str]:
#     out = []
#     word = s[:5]
#     s = remove_start(s, 6)
#
#     out.append(word)
#
#     # print(keep_start(s, 5))
#     lhs, rhs = keep_start(s, 5)
#     for i in range(len(lhs)):
#         print(lhs[i], rhs[i])
#
#     return out


def parse(raw: str) -> Node:
    tree = None
    for line in raw.split('\n'):
        if not line:
            continue
        split = line.split(' ')
        node = tree
        for word, value in zip(split[::2], split[1::2]):
            value = value[:-1]
            if tree is None:
                node = Node(word)
                tree = node
            elif node.word is None:
                node.word = word
            elif node.word != word:
                raise ValueError()

            if value != 'GGGGG':
                if value not in node.children:
                    node.children[value] = Node(None)
                node = node.children[value]
            else:
                pass
    return tree


# write(raw, 0)
# print(keep_start(remove_start(raw, 6), 5))
tree = parse(raw)

INDEX_SIZE = 10


def index_str(idx: int):
    s = str(idx).rjust(INDEX_SIZE, '0')
    if len(s) > INDEX_SIZE:
        raise ValueError()
    return s


def write(tree: Node, file) -> int:
    ret = file.tell()
    file.write(tree.word + '\n')
    tells = {}
    for node in tree.children:
        tells[node] = file.tell()
        file.write(node + index_str(0) + '\n')
    # file.write(''.join(line + index_str(69) + '\n' for line in tree.children))

    for node in tree.children:
        i = write(tree.children[node], file)
        file.seek(tells[node] + 5)
        file.write(index_str(i))
        file.seek(0, os.SEEK_END)

    return ret


with open('tarse.tree', 'w') as file:
    write(tree, file)
