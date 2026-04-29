from __future__ import annotations

from chronos_core.circular_doubly_linked_sequence import CircularDoublyLinkedSequence


class ClockProgressionService:
    """Controls clock time through circular doubly linked hour, minute, and second sequences."""

    def __init__(self):
        self.hour_sequence = CircularDoublyLinkedSequence(range(24))
        self.minute_sequence = CircularDoublyLinkedSequence(range(60))
        self.second_sequence = CircularDoublyLinkedSequence(range(60))
        self._clock_running = False

    def start_clock(self) -> None:
        """Mark the clock as running."""

        self._clock_running = True

    def pause_clock(self) -> None:
        """Mark the clock as paused."""

        self._clock_running = False

    def reset_clock(self) -> None:
        """Return the clock to 00:00:00 and pause it."""

        self.hour_sequence.reset_to_first_value()
        self.minute_sequence.reset_to_first_value()
        self.second_sequence.reset_to_first_value()
        self._clock_running = False

    def move_hour_forward(self) -> int | None:
        """Move the selected hour to its next linked value."""

        return self.hour_sequence.move_to_next_value()

    def move_hour_backward(self) -> int | None:
        """Move the selected hour to its previous linked value."""

        return self.hour_sequence.move_to_previous_value()

    def move_minute_forward(self) -> int | None:
        """Move the selected minute to its next linked value."""

        return self.minute_sequence.move_to_next_value()

    def move_minute_backward(self) -> int | None:
        """Move the selected minute to its previous linked value."""

        return self.minute_sequence.move_to_previous_value()

    def move_second_forward(self) -> int | None:
        """Move the selected second to its next linked value."""

        return self.second_sequence.move_to_next_value()

    def move_second_backward(self) -> int | None:
        """Move the selected second to its previous linked value."""

        return self.second_sequence.move_to_previous_value()

    def advance_one_second(self) -> str:
        """Advance the clock by one second with proper minute and hour rollover."""

        current_second = self.second_sequence.get_selected_value()
        current_minute = self.minute_sequence.get_selected_value()

        self.second_sequence.move_to_next_value()

        if current_second == 59:
            self.minute_sequence.move_to_next_value()
            if current_minute == 59:
                self.hour_sequence.move_to_next_value()

        return self.get_current_time_snapshot()

    def get_current_time_snapshot(self) -> str:
        """Return the current clock time in HH:MM:SS format."""

        selected_hour = self.hour_sequence.get_selected_value()
        selected_minute = self.minute_sequence.get_selected_value()
        selected_second = self.second_sequence.get_selected_value()

        if selected_hour is None or selected_minute is None or selected_second is None:
            raise ValueError("Clock sequences must contain hour, minute, and second values.")

        return f"{selected_hour:02d}:{selected_minute:02d}:{selected_second:02d}"

    def is_clock_running(self) -> bool:
        """Return whether the clock is currently marked as running."""

        return self._clock_running
