from __future__ import annotations

from collections import deque
from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass(frozen=True)
class RecordedEvent:
    event_message: str
    recorded_at: str

    def to_dictionary(self) -> dict[str, str]:
        return asdict(self)


class HistoryRecordingService:
    """Stores recent system events independently from the interface layer."""

    def __init__(self, maximum_event_count: int = 20):
        self._recorded_events: deque[RecordedEvent] = deque(maxlen=maximum_event_count)

    def record_event(self, event_message: str) -> None:
        """Store one event with a creation timestamp."""

        recorded_event = RecordedEvent(
            event_message=event_message,
            recorded_at=datetime.now().strftime("%H:%M:%S"),
        )
        self._recorded_events.appendleft(recorded_event)

    def get_recent_events(self) -> list[dict[str, str]]:
        """Return recent events in reverse chronological order."""

        return [recorded_event.to_dictionary() for recorded_event in self._recorded_events]

    def clear_history(self) -> None:
        """Remove every previously recorded event."""

        self._recorded_events.clear()
