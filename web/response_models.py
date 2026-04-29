from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ClockInterfaceOverview:
    page_title: str
    page_subtitle: str
    clock_title: str
    start_button_label: str
    pause_button_label: str
    reset_button_label: str
    hour_forward_label: str
    hour_backward_label: str
    minute_forward_label: str
    minute_backward_label: str
    second_forward_label: str
    second_backward_label: str
    history_title: str
    pomodoro_title: str
    pomodoro_current_phase_label: str
    pomodoro_remaining_time_label: str
    pomodoro_start_button_label: str
    pomodoro_pause_button_label: str
    pomodoro_reset_button_label: str
    pomodoro_next_phase_button_label: str


@dataclass(frozen=True)
class ClockApiResponse:
    current_time: str
    running: bool

    def to_dictionary(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class PomodoroApiResponse:
    phase_name: str
    duration_seconds: int
    remaining_seconds: int
    running: bool

    def to_dictionary(self) -> dict[str, object]:
        return asdict(self)
