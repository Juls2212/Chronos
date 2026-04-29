# Chronos

Chronos is a local web clock application built with Python and Flask for academic study. The project runs in the browser on `localhost` and is designed around the manual implementation of circular doubly linked lists.

## Academic Focus

The central academic topic of Chronos is the use of circular doubly linked lists. Future project phases will use this structure for time progression, Pomodoro phases, alarm scheduling, theme switching, and event history navigation.

Each linked element is intended to keep:

- `value`
- `previous_reference`
- `next_reference`

## Language Rules

- All internal code is written in English.
- Folder names, file names, classes, methods, variables, and technical documentation are written in English.
- Only visible user interface texts are written in Spanish.

## Run The Project

1. Install the dependencies:

```bash
pip install -r requirements.txt
```

2. Start the local Flask application:

```bash
python app.py
```

3. Open the browser at:

```text
http://127.0.0.1:5000
```

The application is configured to open the browser automatically when it starts.

## Current Scope

This initial base only provides the clean project structure and a running Flask interface with placeholder sections. It does not yet implement the full clock, Pomodoro cycle, alarms, theme behavior, or event history logic.
