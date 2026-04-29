from __future__ import annotations

from typing import Generic, Iterable, TypeVar

from chronos_core.circular_sequence_element import CircularSequenceElement


SequenceValue = TypeVar("SequenceValue")


class CircularDoublyLinkedSequence(Generic[SequenceValue]):
    def __init__(self, initial_values: Iterable[SequenceValue] | None = None):
        self.first_element: CircularSequenceElement[SequenceValue] | None = None
        self.sequence_length = 0

        if initial_values is not None:
            for sequence_value in initial_values:
                self.append_value(sequence_value)

    def append_value(self, sequence_value: SequenceValue) -> CircularSequenceElement[SequenceValue]:
        new_element = CircularSequenceElement(value=sequence_value)

        if self.first_element is None:
            new_element.previous_reference = new_element
            new_element.next_reference = new_element
            self.first_element = new_element
        else:
            last_element = self.first_element.previous_reference
            assert last_element is not None

            new_element.previous_reference = last_element
            new_element.next_reference = self.first_element
            last_element.next_reference = new_element
            self.first_element.previous_reference = new_element

        self.sequence_length += 1
        return new_element

    def iterate_values(self) -> list[SequenceValue]:
        if self.first_element is None:
            return []

        collected_values: list[SequenceValue] = []
        current_element = self.first_element

        for _ in range(self.sequence_length):
            collected_values.append(current_element.value)
            assert current_element.next_reference is not None
            current_element = current_element.next_reference

        return collected_values
