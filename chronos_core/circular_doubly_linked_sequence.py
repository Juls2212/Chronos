from __future__ import annotations

from typing import Generic, Iterable, TypeVar

from chronos_core.circular_sequence_element import CircularSequenceElement


SequenceValue = TypeVar("SequenceValue")


class CircularDoublyLinkedSequence(Generic[SequenceValue]):
    """Manual circular doubly linked sequence with an explicit selected element."""

    def __init__(self, initial_values: Iterable[SequenceValue] | None = None):
        self.first_element: CircularSequenceElement[SequenceValue] | None = None
        self.selected_element: CircularSequenceElement[SequenceValue] | None = None
        self.sequence_length = 0

        if initial_values is not None:
            for sequence_value in initial_values:
                self.append_value(sequence_value)

    def append_value(self, sequence_value: SequenceValue) -> CircularSequenceElement[SequenceValue]:
        """Append one value while preserving circular previous and next links."""

        new_element = CircularSequenceElement(value=sequence_value)

        if self.first_element is None:
            new_element.previous_reference = new_element
            new_element.next_reference = new_element
            self.first_element = new_element
            self.selected_element = new_element
        else:
            last_element = self.first_element.previous_reference
            assert last_element is not None

            new_element.previous_reference = last_element
            new_element.next_reference = self.first_element
            last_element.next_reference = new_element
            self.first_element.previous_reference = new_element

        self.sequence_length += 1
        return new_element

    def get_selected_value(self) -> SequenceValue | None:
        """Return the selected value, or None when the sequence is empty."""

        if self.selected_element is None:
            return None
        return self.selected_element.value

    def move_to_next_value(self) -> SequenceValue | None:
        """Advance to the next linked value and return the new selection."""

        if self.selected_element is None:
            return None

        assert self.selected_element.next_reference is not None
        self.selected_element = self.selected_element.next_reference
        return self.selected_element.value

    def move_to_previous_value(self) -> SequenceValue | None:
        """Move to the previous linked value and return the new selection."""

        if self.selected_element is None:
            return None

        assert self.selected_element.previous_reference is not None
        self.selected_element = self.selected_element.previous_reference
        return self.selected_element.value

    def reset_to_first_value(self) -> SequenceValue | None:
        """Reset the current selection to the first linked value."""

        if self.first_element is None:
            return None

        self.selected_element = self.first_element
        return self.selected_element.value

    def get_values_snapshot(self) -> list[SequenceValue]:
        """Return a readable ordered snapshot for debugging and assertions."""

        if self.first_element is None:
            return []

        collected_values: list[SequenceValue] = []
        selected_element = self.first_element

        for _ in range(self.sequence_length):
            collected_values.append(selected_element.value)
            assert selected_element.next_reference is not None
            selected_element = selected_element.next_reference

        return collected_values

    def get_size(self) -> int:
        """Return the number of linked elements stored in the sequence."""

        return self.sequence_length
