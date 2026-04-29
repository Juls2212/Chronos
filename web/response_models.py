from dataclasses import dataclass


@dataclass(frozen=True)
class InterfaceSectionOverview:
    main_clock_title: str
    pomodoro_title: str
    alarms_title: str
    history_title: str
    structure_explanation_title: str
