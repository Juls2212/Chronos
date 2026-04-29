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


@dataclass(frozen=True)
class ClockApiResponse:
    current_time: str
    running: bool

    def to_dictionary(self) -> dict[str, object]:
        return asdict(self)
