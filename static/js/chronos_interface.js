const clockDisplayElement = document.getElementById("clock-display");
const clockStatusElement = document.getElementById("clock-status");
const hourHandElement = document.getElementById("hour-hand");
const minuteHandElement = document.getElementById("minute-hand");
const secondHandElement = document.getElementById("second-hand");
const pomodoroPhaseLabelElement = document.getElementById("pomodoro-phase-label");
const pomodoroTimeLabelElement = document.getElementById("pomodoro-time-label");
const pomodoroStatusElement = document.getElementById("pomodoro-status");
const historyListElement = document.getElementById("history-list");
const clockControlButtonElements = document.querySelectorAll("[data-clock-action]");
const pomodoroControlButtonElements = document.querySelectorAll("[data-pomodoro-action]");

function extractTimeParts(timeLabel) {
    const [hourLabel, minuteLabel, secondLabel] = timeLabel.split(":");
    return {
        hourValue: Number.parseInt(hourLabel, 10),
        minuteValue: Number.parseInt(minuteLabel, 10),
        secondValue: Number.parseInt(secondLabel, 10),
    };
}

function mapPomodoroPhaseLabel(phaseName) {
    if (phaseName === "focus") {
        return "Enfoque";
    }
    if (phaseName === "short_break") {
        return "Descanso corto";
    }
    return "Descanso largo";
}

function formatDurationLabel(totalSeconds) {
    const minuteValue = Math.floor(totalSeconds / 60);
    const secondValue = totalSeconds % 60;
    return `${String(minuteValue).padStart(2, "0")}:${String(secondValue).padStart(2, "0")}`;
}

function updateAnalogClock(timeLabel) {
    const { hourValue, minuteValue, secondValue } = extractTimeParts(timeLabel);

    const secondRotation = secondValue * 6;
    const minuteRotation = minuteValue * 6 + secondValue * 0.1;
    const normalizedHourValue = hourValue % 12;
    const hourRotation = normalizedHourValue * 30 + minuteValue * 0.5;

    hourHandElement.style.transform = `translateX(-50%) rotate(${hourRotation}deg)`;
    minuteHandElement.style.transform = `translateX(-50%) rotate(${minuteRotation}deg)`;
    secondHandElement.style.transform = `translateX(-50%) rotate(${secondRotation}deg)`;
}

function renderClockState(clockState) {
    clockDisplayElement.textContent = clockState.current_time;
    clockStatusElement.textContent = clockState.running ? "En ejecución" : "En pausa";
    updateAnalogClock(clockState.current_time);
}

function renderPomodoroState(pomodoroState) {
    pomodoroPhaseLabelElement.textContent = mapPomodoroPhaseLabel(pomodoroState.phase_name);
    pomodoroTimeLabelElement.textContent = formatDurationLabel(pomodoroState.remaining_seconds);
    pomodoroStatusElement.textContent = pomodoroState.running ? "En ejecución" : "En pausa";
}

function renderHistory(historyEvents) {
    historyListElement.innerHTML = "";

    historyEvents.forEach((historyEvent) => {
        const historyEntryElement = document.createElement("li");
        const historyTimeElement = document.createElement("span");
        const historyMessageElement = document.createElement("span");

        historyEntryElement.className = "history-entry";
        historyTimeElement.className = "history-time";
        historyMessageElement.className = "history-message";

        historyTimeElement.textContent = historyEvent.recorded_at;
        historyMessageElement.textContent = historyEvent.event_message;

        historyEntryElement.appendChild(historyTimeElement);
        historyEntryElement.appendChild(historyMessageElement);
        historyListElement.appendChild(historyEntryElement);
    });
}

async function refreshClockState() {
    const response = await fetch("/api/clock");
    const clockState = await response.json();
    renderClockState(clockState);
}

async function refreshPomodoroState() {
    const response = await fetch("/api/pomodoro");
    const pomodoroState = await response.json();
    renderPomodoroState(pomodoroState);
}

async function refreshHistory() {
    const response = await fetch("/api/history");
    const historyState = await response.json();
    renderHistory(historyState.events);
}

async function refreshInterface() {
    await Promise.all([refreshClockState(), refreshPomodoroState(), refreshHistory()]);
}

async function sendClockAction(actionRoute) {
    const response = await fetch(actionRoute, {
        method: "POST",
    });
    const clockState = await response.json();
    renderClockState(clockState);
    await refreshHistory();
}

async function sendPomodoroAction(actionRoute) {
    const response = await fetch(actionRoute, {
        method: "POST",
    });
    const pomodoroState = await response.json();
    renderPomodoroState(pomodoroState);
    await refreshHistory();
}

clockControlButtonElements.forEach((buttonElement) => {
    buttonElement.addEventListener("click", async () => {
        await sendClockAction(buttonElement.dataset.clockAction);
    });
});

pomodoroControlButtonElements.forEach((buttonElement) => {
    buttonElement.addEventListener("click", async () => {
        await sendPomodoroAction(buttonElement.dataset.pomodoroAction);
    });
});

refreshInterface();
window.setInterval(refreshInterface, 500);
