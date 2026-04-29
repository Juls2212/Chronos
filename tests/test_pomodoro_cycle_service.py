from chronos_core.pomodoro_cycle_service import PomodoroCycleService


def test_initial_pomodoro_phase():
    pomodoro_cycle_service = PomodoroCycleService()

    phase_snapshot = pomodoro_cycle_service.get_current_phase_snapshot()
    assert phase_snapshot["phase_name"] == "focus"
    assert phase_snapshot["remaining_seconds"] == 25 * 60
    assert pomodoro_cycle_service.is_pomodoro_running() is False


def test_start_pomodoro():
    pomodoro_cycle_service = PomodoroCycleService()

    pomodoro_cycle_service.start_pomodoro()

    assert pomodoro_cycle_service.is_pomodoro_running() is True


def test_pause_pomodoro():
    pomodoro_cycle_service = PomodoroCycleService()

    pomodoro_cycle_service.start_pomodoro()
    pomodoro_cycle_service.pause_pomodoro()

    assert pomodoro_cycle_service.is_pomodoro_running() is False


def test_reset_pomodoro():
    pomodoro_cycle_service = PomodoroCycleService(focus_duration_seconds=4, short_break_duration_seconds=2, long_break_duration_seconds=3)

    pomodoro_cycle_service.start_pomodoro()
    pomodoro_cycle_service.advance_one_second()
    pomodoro_cycle_service.move_to_next_phase()
    pomodoro_cycle_service.reset_pomodoro()

    phase_snapshot = pomodoro_cycle_service.get_current_phase_snapshot()
    assert phase_snapshot["phase_name"] == "focus"
    assert phase_snapshot["remaining_seconds"] == 4
    assert pomodoro_cycle_service.is_pomodoro_running() is False


def test_advance_one_second():
    pomodoro_cycle_service = PomodoroCycleService(focus_duration_seconds=4, short_break_duration_seconds=2, long_break_duration_seconds=3)

    pomodoro_cycle_service.start_pomodoro()
    pomodoro_cycle_service.advance_one_second()

    phase_snapshot = pomodoro_cycle_service.get_current_phase_snapshot()
    assert phase_snapshot["phase_name"] == "focus"
    assert phase_snapshot["remaining_seconds"] == 3


def test_move_to_next_phase():
    pomodoro_cycle_service = PomodoroCycleService(focus_duration_seconds=4, short_break_duration_seconds=2, long_break_duration_seconds=3)

    phase_snapshot = pomodoro_cycle_service.move_to_next_phase()

    assert phase_snapshot["phase_name"] == "short_break"
    assert phase_snapshot["remaining_seconds"] == 2


def test_circular_movement_after_long_break():
    pomodoro_cycle_service = PomodoroCycleService(focus_duration_seconds=4, short_break_duration_seconds=2, long_break_duration_seconds=3)

    for _ in range(5):
        pomodoro_cycle_service.move_to_next_phase()

    phase_snapshot = pomodoro_cycle_service.get_current_phase_snapshot()
    assert phase_snapshot["phase_name"] == "long_break"

    phase_snapshot = pomodoro_cycle_service.move_to_next_phase()
    assert phase_snapshot["phase_name"] == "focus"
    assert phase_snapshot["remaining_seconds"] == 4


def test_configurable_short_durations_for_tests():
    pomodoro_cycle_service = PomodoroCycleService(focus_duration_seconds=2, short_break_duration_seconds=1, long_break_duration_seconds=3)

    pomodoro_cycle_service.start_pomodoro()
    pomodoro_cycle_service.advance_one_second()
    assert pomodoro_cycle_service.get_current_phase_snapshot()["remaining_seconds"] == 1

    pomodoro_cycle_service.advance_one_second()
    phase_snapshot = pomodoro_cycle_service.get_current_phase_snapshot()
    assert phase_snapshot["phase_name"] == "short_break"
    assert phase_snapshot["remaining_seconds"] == 1
