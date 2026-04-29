from __future__ import annotations

from threading import Timer
import webbrowser

from flask import Flask, render_template

from web.response_models import InterfaceSectionOverview


def create_application() -> Flask:
    flask_application = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
        static_url_path="/static",
    )

    @flask_application.get("/")
    def index():
        interface_sections = InterfaceSectionOverview(
            main_clock_title="Reloj principal",
            pomodoro_title="Pomodoro",
            alarms_title="Alarmas",
            history_title="Historial de eventos",
            structure_explanation_title="Explicación de la estructura de datos",
        )

        return render_template(
            "index.html",
            page_title="Chronos",
            page_subtitle="Reloj académico con listas doblemente enlazadas circulares",
            interface_sections=interface_sections,
        )

    return flask_application


def open_local_browser(application_url: str) -> None:
    Timer(1.0, lambda: webbrowser.open(application_url)).start()
