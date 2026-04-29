from chronos_core.history_recording_service import HistoryRecordingService


def test_record_single_event():
    history_recording_service = HistoryRecordingService()

    history_recording_service.record_event("Reloj iniciado")

    recorded_events = history_recording_service.get_recent_events()
    assert len(recorded_events) == 1
    assert recorded_events[0]["event_message"] == "Reloj iniciado"


def test_record_multiple_events():
    history_recording_service = HistoryRecordingService()

    history_recording_service.record_event("Reloj iniciado")
    history_recording_service.record_event("Hora avanzada")

    recorded_events = history_recording_service.get_recent_events()
    assert len(recorded_events) == 2
    assert recorded_events[0]["event_message"] == "Hora avanzada"
    assert recorded_events[1]["event_message"] == "Reloj iniciado"


def test_retrieve_recent_events():
    history_recording_service = HistoryRecordingService(maximum_event_count=3)

    history_recording_service.record_event("Reloj iniciado")
    history_recording_service.record_event("Hora avanzada")
    history_recording_service.record_event("Minuto avanzado")
    history_recording_service.record_event("Segundo avanzado")

    recorded_events = history_recording_service.get_recent_events()
    assert len(recorded_events) == 3
    assert [recorded_event["event_message"] for recorded_event in recorded_events] == [
        "Segundo avanzado",
        "Minuto avanzado",
        "Hora avanzada",
    ]


def test_clear_history():
    history_recording_service = HistoryRecordingService()

    history_recording_service.record_event("Reloj iniciado")
    history_recording_service.clear_history()

    assert history_recording_service.get_recent_events() == []


def test_event_timestamps_exist():
    history_recording_service = HistoryRecordingService()

    history_recording_service.record_event("Reloj iniciado")

    recorded_events = history_recording_service.get_recent_events()
    assert "recorded_at" in recorded_events[0]
    assert recorded_events[0]["recorded_at"]
