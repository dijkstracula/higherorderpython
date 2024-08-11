from hop.ch4.iterator import Iterator

from dataclasses import dataclass

from typing import Generic, Optional, TypeVar

T = TypeVar("T")

def gcd(m: int, n: int) -> int:
    if n == 0:
        return m
    return gcd(n, m % n)

def gcd_tc(m: int, n: int) -> int:
    while n != 0:
        m, n = n, m % n
    return m

@dataclass
class BinTreeNode(Generic[T]):
    left: Optional["BinTreeNode[T]"]
    elem: T
    right: Optional["BinTreeNode[T]"]

def flatten_tree(tree: Optional[BinTreeNode[T]]) -> list[T]:
    if tree is None:
        return []
    ret = []
    ret.extend(flatten_tree(tree.left))
    ret.append(tree.elem)
    ret.extend(flatten_tree(tree.right))
    return ret

def flatten_tree_v2(tree: Optional[BinTreeNode[T]]) -> list[T]:
    ret = []
    curr: Optional[BinTreeNode[T]] = tree
    while curr is not None:
        ret.extend(flatten_tree(curr.left))
        ret.append(curr.elem)
        curr = curr.right
    return ret

def flatten_tree_v3(tree: BinTreeNode[T]) -> list[T]:
    ret: list[T] = []
    stack: list[tuple[BinTreeNode[T], bool]] = [(tree, False)]

    while len(stack) > 0:
        (curr, visited_left) = stack.pop()
        if not visited_left and curr.left is not None:
            stack.append((curr, True))
            stack.append((curr.left, False))
        else:
            ret.append(curr.elem)
            if curr.right is not None:
                stack.append((curr.right, False))
             
    return ret

def binary(n: int) -> str:
    if n <= 1:
        return str(n)
    return binary(n // 2) + str(n % 2)

def binary_acc(n: int, acc="") -> str:
    acc = str(n % 2) + acc
    if n <= 1:
        return acc
    return binary_acc(n//2, acc)
