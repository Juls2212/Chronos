from __future__ import annotations

from dataclasses import dataclass

from chronos_core.circular_doubly_linked_sequence import CircularDoublyLinkedSequence


@dataclass(frozen=True)
class PomodoroPhaseDefinition:
    phase_name: str
    duration_seconds: int


class PomodoroCycleService:
    """Controls a circular Pomodoro phase sequence and its remaining time."""

    def __init__(
        self,
        focus_duration_seconds: int = 25 * 60,
        short_break_duration_seconds: int = 5 * 60,
        long_break_duration_seconds: int = 15 * 60,
    ):
        self._phase_sequence = CircularDoublyLinkedSequence(
            (
                PomodoroPhaseDefinition("focus", focus_duration_seconds),
                PomodoroPhaseDefinition("short_break", short_break_duration_seconds),
                PomodoroPhaseDefinition("focus", focus_duration_seconds),
                PomodoroPhaseDefinition("short_break", short_break_duration_seconds),
                PomodoroPhaseDefinition("focus", focus_duration_seconds),
                PomodoroPhaseDefinition("long_break", long_break_duration_seconds),
            )
        )
        selected_phase = self._require_selected_phase()
        self._remaining_seconds = selected_phase.duration_seconds
        self._pomodoro_running = False

    def _require_selected_phase(self) -> PomodoroPhaseDefinition:
        selected_phase = self._phase_sequence.get_selected_value()
        if selected_phase is None:
            raise ValueError("Pomodoro phase sequence must contain at least one phase.")
        return selected_phase

    def start_pomodoro(self) -> None:
        self._pomodoro_running = True

    def pause_pomodoro(self) -> None:
        self._pomodoro_running = False

    def reset_pomodoro(self) -> None:
        self._phase_sequence.reset_to_first_value()
        self._remaining_seconds = self._require_selected_phase().duration_seconds
        self._pomodoro_running = False

    def move_to_next_phase(self) -> dict[str, object]:
        self._phase_sequence.move_to_next_value()
        selected_phase = self._require_selected_phase()
        self._remaining_seconds = selected_phase.duration_seconds
        return self.get_current_phase_snapshot()

    def advance_one_second(self) -> dict[str, object]:
        if not self._pomodoro_running:
            return self.get_current_phase_snapshot()

        if self._remaining_seconds > 1:
            self._remaining_seconds -= 1
            return self.get_current_phase_snapshot()

        self._phase_sequence.move_to_next_value()
        selected_phase = self._require_selected_phase()
        self._remaining_seconds = selected_phase.duration_seconds
        return self.get_current_phase_snapshot()

    def get_current_phase_snapshot(self) -> dict[str, object]:
        selected_phase = self._require_selected_phase()
        return {
            "phase_name": selected_phase.phase_name,
            "duration_seconds": selected_phase.duration_seconds,
            "remaining_seconds": self._remaining_seconds,
            "running": self._pomodoro_running,
        }

    def is_pomodoro_running(self) -> bool:
        return self._pomodoro_running
