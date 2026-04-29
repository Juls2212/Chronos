from chronos_core.clock_progression_service import ClockProgressionService


def test_initial_state():
    clock_progression_service = ClockProgressionService()

    assert clock_progression_service.get_current_time_snapshot() == "00:00:00"
    assert clock_progression_service.is_clock_running() is False


def test_start_clock():
    clock_progression_service = ClockProgressionService()

    clock_progression_service.start_clock()

    assert clock_progression_service.is_clock_running() is True


def test_pause_clock():
    clock_progression_service = ClockProgressionService()

    clock_progression_service.start_clock()
    clock_progression_service.pause_clock()

    assert clock_progression_service.is_clock_running() is False


def test_reset_clock():
    clock_progression_service = ClockProgressionService()

    clock_progression_service.start_clock()
    clock_progression_service.move_hour_forward()
    clock_progression_service.move_minute_forward()
    clock_progression_service.move_second_forward()

    clock_progression_service.reset_clock()

    assert clock_progression_service.get_current_time_snapshot() == "00:00:00"
    assert clock_progression_service.is_clock_running() is False


def test_move_seconds_forward():
    clock_progression_service = ClockProgressionService()

    clock_progression_service.move_second_forward()
    assert clock_progression_service.get_current_time_snapshot() == "00:00:01"

    clock_progression_service.move_second_forward()
    assert clock_progression_service.get_current_time_snapshot() == "00:00:02"


def test_move_seconds_backward():
    clock_progression_service = ClockProgressionService()

    clock_progression_service.move_second_backward()

    assert clock_progression_service.get_current_time_snapshot() == "00:00:59"


def test_move_minutes_forward():
    clock_progression_service = ClockProgressionService()

    clock_progression_service.move_minute_forward()

    assert clock_progression_service.get_current_time_snapshot() == "00:01:00"


def test_move_minutes_backward():
    clock_progression_service = ClockProgressionService()

    clock_progression_service.move_minute_backward()

    assert clock_progression_service.get_current_time_snapshot() == "00:59:00"


def test_move_hours_forward():
    clock_progression_service = ClockProgressionService()

    clock_progression_service.move_hour_forward()

    assert clock_progression_service.get_current_time_snapshot() == "01:00:00"


def test_move_hours_backward():
    clock_progression_service = ClockProgressionService()

    clock_progression_service.move_hour_backward()

    assert clock_progression_service.get_current_time_snapshot() == "23:00:00"


def test_transition_from_235959_to_000000():
    clock_progression_service = ClockProgressionService()

    for _ in range(23):
        clock_progression_service.move_hour_forward()
    for _ in range(59):
        clock_progression_service.move_minute_forward()
    for _ in range(59):
        clock_progression_service.move_second_forward()

    assert clock_progression_service.get_current_time_snapshot() == "23:59:59"

    clock_progression_service.advance_one_second()

    assert clock_progression_service.get_current_time_snapshot() == "00:00:00"


def test_backward_movement_from_000000_to_previous_circular_values():
    clock_progression_service = ClockProgressionService()

    clock_progression_service.move_second_backward()
    assert clock_progression_service.get_current_time_snapshot() == "00:00:59"

    clock_progression_service.reset_clock()
    clock_progression_service.move_minute_backward()
    assert clock_progression_service.get_current_time_snapshot() == "00:59:00"

    clock_progression_service.reset_clock()
    clock_progression_service.move_hour_backward()
    assert clock_progression_service.get_current_time_snapshot() == "23:00:00"
