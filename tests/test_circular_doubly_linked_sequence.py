from chronos_core.circular_doubly_linked_sequence import CircularDoublyLinkedSequence


def test_empty_sequence():
    time_sequence = CircularDoublyLinkedSequence()

    assert time_sequence.get_size() == 0
    assert time_sequence.get_selected_value() is None
    assert time_sequence.move_to_next_value() is None
    assert time_sequence.move_to_previous_value() is None
    assert time_sequence.reset_to_first_value() is None
    assert time_sequence.get_values_snapshot() == []


def test_sequence_with_one_value():
    time_sequence = CircularDoublyLinkedSequence([12])

    assert time_sequence.get_size() == 1
    assert time_sequence.get_selected_value() == 12
    assert time_sequence.first_element is not None
    assert time_sequence.first_element.previous_reference is time_sequence.first_element
    assert time_sequence.first_element.next_reference is time_sequence.first_element
    assert time_sequence.move_to_next_value() == 12
    assert time_sequence.move_to_previous_value() == 12


def test_sequence_with_several_values():
    time_sequence = CircularDoublyLinkedSequence([3, 7, 11, 19])

    assert time_sequence.get_size() == 4
    assert time_sequence.get_selected_value() == 3
    assert time_sequence.get_values_snapshot() == [3, 7, 11, 19]


def test_circular_forward_movement():
    time_sequence = CircularDoublyLinkedSequence([1, 2, 3])

    assert time_sequence.move_to_next_value() == 2
    assert time_sequence.move_to_next_value() == 3
    assert time_sequence.move_to_next_value() == 1


def test_circular_backward_movement():
    time_sequence = CircularDoublyLinkedSequence([1, 2, 3])

    assert time_sequence.move_to_previous_value() == 3
    assert time_sequence.move_to_previous_value() == 2
    assert time_sequence.move_to_previous_value() == 1


def test_previous_and_next_references_are_correctly_connected():
    time_sequence = CircularDoublyLinkedSequence(["focus", "short break", "long break"])

    first_element = time_sequence.first_element
    assert first_element is not None

    second_element = first_element.next_reference
    assert second_element is not None

    third_element = second_element.next_reference
    assert third_element is not None

    assert first_element.previous_reference is third_element
    assert first_element.next_reference is second_element
    assert second_element.previous_reference is first_element
    assert second_element.next_reference is third_element
    assert third_element.previous_reference is second_element
    assert third_element.next_reference is first_element


def test_get_values_snapshot_returns_readable_representation():
    time_sequence = CircularDoublyLinkedSequence(["day", "night"])

    assert time_sequence.get_values_snapshot() == ["day", "night"]

    time_sequence.move_to_next_value()
    assert time_sequence.get_values_snapshot() == ["day", "night"]
