from __future__ import annotations

from datetime import datetime
from threading import Timer
import webbrowser

from flask import Flask, jsonify, render_template

from chronos_core.clock_progression_service import ClockProgressionService
from chronos_core.history_recording_service import HistoryRecordingService
from chronos_core.pomodoro_cycle_service import PomodoroCycleService
from web.response_models import ClockApiResponse, ClockInterfaceOverview, PomodoroApiResponse


def create_application() -> Flask:
    flask_application = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
        static_url_path="/static",
    )
    clock_progression_service = ClockProgressionService()
    pomodoro_cycle_service = PomodoroCycleService()
    history_recording_service = HistoryRecordingService()
    last_clock_synchronization_timestamp = datetime.now()
    last_pomodoro_synchronization_timestamp = datetime.now()

    def synchronize_clock_state() -> None:
        nonlocal last_clock_synchronization_timestamp

        if not clock_progression_service.is_clock_running():
            last_clock_synchronization_timestamp = datetime.now()
            return

        current_timestamp = datetime.now()
        elapsed_seconds = int((current_timestamp - last_clock_synchronization_timestamp).total_seconds())

        for _ in range(max(elapsed_seconds, 0)):
            clock_progression_service.advance_one_second()

        if elapsed_seconds > 0:
            last_clock_synchronization_timestamp = current_timestamp

    def synchronize_pomodoro_state() -> None:
        nonlocal last_pomodoro_synchronization_timestamp

        if not pomodoro_cycle_service.is_pomodoro_running():
            last_pomodoro_synchronization_timestamp = datetime.now()
            return

        current_timestamp = datetime.now()
        elapsed_seconds = int((current_timestamp - last_pomodoro_synchronization_timestamp).total_seconds())

        for _ in range(max(elapsed_seconds, 0)):
            pomodoro_cycle_service.advance_one_second()

        if elapsed_seconds > 0:
            last_pomodoro_synchronization_timestamp = current_timestamp

    def build_clock_response() -> ClockApiResponse:
        synchronize_clock_state()
        return ClockApiResponse(
            current_time=clock_progression_service.get_current_time_snapshot(),
            running=clock_progression_service.is_clock_running(),
        )

    def build_pomodoro_response() -> PomodoroApiResponse:
        synchronize_pomodoro_state()
        pomodoro_snapshot = pomodoro_cycle_service.get_current_phase_snapshot()
        return PomodoroApiResponse(
            phase_name=str(pomodoro_snapshot["phase_name"]),
            duration_seconds=int(pomodoro_snapshot["duration_seconds"]),
            remaining_seconds=int(pomodoro_snapshot["remaining_seconds"]),
            running=bool(pomodoro_snapshot["running"]),
        )

    def build_history_response() -> list[dict[str, str]]:
        return history_recording_service.get_recent_events()

    @flask_application.get("/")
    def index():
        interface_overview = ClockInterfaceOverview(
            page_title="Chronos",
            page_subtitle="Reloj académico con listas doblemente enlazadas circulares",
            clock_title="Reloj principal",
            start_button_label="Iniciar",
            pause_button_label="Pausar",
            reset_button_label="Reiniciar",
            hour_forward_label="Avanzar hora",
            hour_backward_label="Retroceder hora",
            minute_forward_label="Avanzar minuto",
            minute_backward_label="Retroceder minuto",
            second_forward_label="Avanzar segundo",
            second_backward_label="Retroceder segundo",
            history_title="Historial de eventos",
            pomodoro_title="Pomodoro",
            pomodoro_current_phase_label="Fase actual",
            pomodoro_remaining_time_label="Tiempo restante",
            pomodoro_start_button_label="Iniciar Pomodoro",
            pomodoro_pause_button_label="Pausar Pomodoro",
            pomodoro_reset_button_label="Reiniciar Pomodoro",
            pomodoro_next_phase_button_label="Siguiente fase",
        )

        return render_template(
            "index.html",
            interface_overview=interface_overview,
            clock_state=build_clock_response(),
            pomodoro_state=build_pomodoro_response(),
            history_events=build_history_response(),
        )

    @flask_application.get("/api/clock")
    def get_clock_state():
        return jsonify(build_clock_response().to_dictionary())

    @flask_application.get("/api/pomodoro")
    def get_pomodoro_state():
        return jsonify(build_pomodoro_response().to_dictionary())

    @flask_application.get("/api/history")
    def get_history():
        return jsonify({"events": build_history_response()})

    @flask_application.post("/api/clock/start")
    def start_clock():
        nonlocal last_clock_synchronization_timestamp
        synchronize_clock_state()
        clock_progression_service.start_clock()
        history_recording_service.record_event("Reloj iniciado")
        last_clock_synchronization_timestamp = datetime.now()
        return jsonify(build_clock_response().to_dictionary())

    @flask_application.post("/api/clock/pause")
    def pause_clock():
        synchronize_clock_state()
        clock_progression_service.pause_clock()
        history_recording_service.record_event("Reloj pausado")
        return jsonify(build_clock_response().to_dictionary())

    @flask_application.post("/api/clock/reset")
    def reset_clock():
        nonlocal last_clock_synchronization_timestamp
        clock_progression_service.reset_clock()
        history_recording_service.record_event("Reloj reiniciado")
        last_clock_synchronization_timestamp = datetime.now()
        return jsonify(build_clock_response().to_dictionary())

    @flask_application.post("/api/clock/hour/forward")
    def move_hour_forward():
        synchronize_clock_state()
        clock_progression_service.move_hour_forward()
        history_recording_service.record_event("Hora avanzada")
        return jsonify(build_clock_response().to_dictionary())

    @flask_application.post("/api/clock/hour/backward")
    def move_hour_backward():
        synchronize_clock_state()
        clock_progression_service.move_hour_backward()
        history_recording_service.record_event("Hora retrocedida")
        return jsonify(build_clock_response().to_dictionary())

    @flask_application.post("/api/clock/minute/forward")
    def move_minute_forward():
        synchronize_clock_state()
        clock_progression_service.move_minute_forward()
        history_recording_service.record_event("Minuto avanzado")
        return jsonify(build_clock_response().to_dictionary())

    @flask_application.post("/api/clock/minute/backward")
    def move_minute_backward():
        synchronize_clock_state()
        clock_progression_service.move_minute_backward()
        history_recording_service.record_event("Minuto retrocedido")
        return jsonify(build_clock_response().to_dictionary())

    @flask_application.post("/api/clock/second/forward")
    def move_second_forward():
        synchronize_clock_state()
        clock_progression_service.move_second_forward()
        history_recording_service.record_event("Segundo avanzado")
        return jsonify(build_clock_response().to_dictionary())

    @flask_application.post("/api/clock/second/backward")
    def move_second_backward():
        synchronize_clock_state()
        clock_progression_service.move_second_backward()
        history_recording_service.record_event("Segundo retrocedido")
        return jsonify(build_clock_response().to_dictionary())

    @flask_application.post("/api/pomodoro/start")
    def start_pomodoro():
        nonlocal last_pomodoro_synchronization_timestamp
        synchronize_pomodoro_state()
        pomodoro_cycle_service.start_pomodoro()
        history_recording_service.record_event("Pomodoro iniciado")
        last_pomodoro_synchronization_timestamp = datetime.now()
        return jsonify(build_pomodoro_response().to_dictionary())

    @flask_application.post("/api/pomodoro/pause")
    def pause_pomodoro():
        synchronize_pomodoro_state()
        pomodoro_cycle_service.pause_pomodoro()
        history_recording_service.record_event("Pomodoro pausado")
        return jsonify(build_pomodoro_response().to_dictionary())

    @flask_application.post("/api/pomodoro/reset")
    def reset_pomodoro():
        nonlocal last_pomodoro_synchronization_timestamp
        pomodoro_cycle_service.reset_pomodoro()
        history_recording_service.record_event("Pomodoro reiniciado")
        last_pomodoro_synchronization_timestamp = datetime.now()
        return jsonify(build_pomodoro_response().to_dictionary())

    @flask_application.post("/api/pomodoro/next-phase")
    def move_to_next_phase():
        synchronize_pomodoro_state()
        pomodoro_cycle_service.move_to_next_phase()
        history_recording_service.record_event("Fase de Pomodoro cambiada")
        return jsonify(build_pomodoro_response().to_dictionary())

    return flask_application


def open_local_browser(application_url: str) -> None:
    Timer(1.0, lambda: webbrowser.open(application_url)).start()
