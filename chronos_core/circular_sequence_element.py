from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar


SequenceValue = TypeVar("SequenceValue")


@dataclass
class CircularSequenceElement(Generic[SequenceValue]):
    """Represents one element inside a circular doubly linked sequence."""

    value: SequenceValue
    previous_reference: "CircularSequenceElement[SequenceValue] | None" = None
    next_reference: "CircularSequenceElement[SequenceValue] | None" = None
