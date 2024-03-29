"""
Justin Baum
20 October 2020
curve_types.py
Gets rid of circular dependencies
"""
from typing import TypeVar, Tuple

TPoint = TypeVar('TPoint')
TCurve = TypeVar('TCurve')
TPairPoint = Tuple[TPoint, TPoint]
