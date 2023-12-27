"""
Utilities for miscellaneous tasks.
"""
from typing import Dict, List, Optional


def indent(s, nspace):
    """Gives indentation of the second line and next lines.
    It is used to format the string representation of an object.
    Which might be containing multiples objects in it.
    Usage: LinearOperator

    Parameters
    ----------
    s: str
        The string to be indented.
    nspace: int
        The number of spaces to be indented.

    Returns
    -------
    str
        The indented string.

    """
    spaces = " " * nspace
    lines = [spaces + c if i > 0 else c for i, c in enumerate(s.split("\n"))]
    return "\n".join(lines)


def shape2str(shape):
    """Convert the shape to string representation.
    It also nicely formats the shape to be readable.

    Parameters
    ----------
    shape: Sequence[int]
        The shape to be converted to string representation.

    Returns
    -------
    str
        The string representation of the shape.

    """
    return "(%s)" % (", ".join([str(s) for s in shape]))


# Warnings
class UnimplementedError(Exception):
    pass


class GetSetParamsError(Exception):
    pass


class ConvergenceWarning(Warning):
    """
    Warning to be raised if the convergence of an algorithm is not achieved
    """
    pass


class MathWarning(Warning):
    """
    Raised if there are mathematical conditions that are not satisfied
    """
    pass


class Uniquifier(object):
    """
    Identifies and tracks unique objects within a list, even if they are
    duplicates based on internal memory addresses (using id()).
    It Optimizes operations involving unique objects by avoiding redundant
    processing.

    Examples
    --------
    >>> from deepchem.utils import Uniquifier
    >>> a = 1
    >>> b = 2
    >>> c = 3
    >>> d = 1
    >>> u = Uniquifier([a, b, c, a, d])
    >>> u.get_unique_objs()
    [1, 2, 3]

    """

    def __init__(self, allobjs: List):
        """Initialize the uniquifier.

        Parameters
        ----------
        allobjs: List
            The list of objects to be uniquified.

        """
        self.nobjs = len(allobjs)

        id2idx: Dict[int, int] = {}
        unique_objs: List[int] = []
        unique_idxs: List[int] = []
        nonunique_map_idxs: List[int] = [-self.nobjs * 2] * self.nobjs
        num_unique = 0
        for i, obj in enumerate(allobjs):
            id_obj = id(obj)
            if id_obj in id2idx:
                nonunique_map_idxs[i] = id2idx[id_obj]
                continue
            id2idx[id_obj] = num_unique
            unique_objs.append(obj)
            nonunique_map_idxs[i] = num_unique
            unique_idxs.append(i)
            num_unique += 1

        self.unique_objs = unique_objs
        self.unique_idxs = unique_idxs
        self.nonunique_map_idxs = nonunique_map_idxs
        self.num_unique = num_unique
        self.all_unique = self.nobjs == self.num_unique

    def get_unique_objs(self, allobjs: Optional[List] = None) -> List:
        """Get the unique objects.

        Parameters
        ----------
        allobjs: Optional[List]
            The list of objects to be uniquified.

        Returns
        -------
        List
            The list of unique objects.

        """
        if allobjs is None:
            return self.unique_objs
        assert len(
            allobjs
        ) == self.nobjs, "The allobjs must have %d elements" % self.nobjs
        if self.all_unique:
            return allobjs
        return [allobjs[i] for i in self.unique_idxs]

    def map_unique_objs(self, uniqueobjs: List) -> List:
        """Map the unique objects to the original objects.

        Parameters
        ----------
        uniqueobjs: List
            The list of unique objects.

        """
        assert len(
            uniqueobjs
        ) == self.num_unique, "The uniqueobjs must have %d elements" % self.num_unique
        if self.all_unique:
            return uniqueobjs
        return [uniqueobjs[idx] for idx in self.nonunique_map_idxs]
