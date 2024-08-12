from hop.ch4.iterator import Iterator

from dataclasses import astuple, dataclass
from enum import Enum
from typing import Generic, Literal, Optional, TypeVar

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

def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n-2) + fib(n-1)

def fib_v2(n: int) -> int:
    if n <= 1:
        return n

    # IP: compute_f_2
    f2 = fib(n-2)
    
    # IP: compute_f_1
    f1 = fib(n-1)

    # IP: sum_and_ret
    return f2 + f1

InstPtr = Enum("InstPtr", ["check_base_case", "compute_f_2", "compute_f_1", "sum_and_ret"])

@dataclass
class Frame:
    n: int
    ip: InstPtr = InstPtr.check_base_case
    f2: Optional[int] = None
    f1: Optional[int] = None

def fib_v3(n: int) -> int:
    stack: list[Frame] = [Frame(n)]
    retval = -1

    def inc_rip():
        match stack[-1].ip:
            case InstPtr.check_base_case:
                stack[-1].ip = InstPtr.compute_f_2
            case InstPtr.compute_f_2:
                stack[-1].ip = InstPtr.compute_f_1
            case InstPtr.compute_f_1:
                stack[-1].ip = InstPtr.sum_and_ret
            case InstPtr.sum_and_ret:
                raise Exception(f"Can't increment RIP after sum_and_ret: state: {stack[-1]}")

    def call(n):
        inc_rip()
        stack.append(Frame(n))

    def ret(n):
        nonlocal retval
        stack.pop()
        retval = n

    while len(stack) > 0:
        f = stack[-1]
        match f:
            case Frame(n, InstPtr.check_base_case, None, None) if n <= 1:
                ret(n)
            case Frame(n, InstPtr.check_base_case, None, None):
                inc_rip()
            
            case Frame(n, InstPtr.compute_f_2, None, None):
                call(n-2)

            case Frame(n, InstPtr.compute_f_1, None, None):
                f.f2 = retval
            case Frame(n, InstPtr.compute_f_1, f2, None) if f2 is not None:
                call(n-1)

            case Frame(n, InstPtr.sum_and_ret, f2, None) if f2 is not None:
                f.f1 = retval
            case Frame(n, InstPtr.sum_and_ret, f2, f1) if f2 is not None and f1 is not None:
                ret(f2 + f1)

            case n, rip, f2, f1:
                raise Exception(f"{n} {rip} {f2} {f1}")

    return retval


@dataclass
class FrameOpto:
    n: int
    ip: int = 1
    f2: int = 42
    f1: int = 42

def fib_v3_opto(n: int) -> int:
    stack: list[FrameOpto] = [FrameOpto(n)]
    retval = -1

    def inc_rip():
        stack[-1].ip += 1

    def call(n):
        inc_rip()
        stack.append(FrameOpto(n))

    def ret(n):
        nonlocal retval
        stack.pop()
        retval = n

    while len(stack) > 0:
        f = stack[-1]

        if f.ip == 1:
            if f.n <= 1:
                ret(f.n)
            else:
                inc_rip()
        elif f.ip == 2:
            call(f.n-2)
        elif f.ip == 3:
            f.f2 = retval
            call(f.n-1)
        elif f.ip == 4:
            f.f1 = retval
            ret(f.f2 + f.f1)
        else:
            raise Exception(f)

    return retval

