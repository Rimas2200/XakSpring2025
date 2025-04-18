import json
from pathlib import Path


def load_logs(log_dir):
    log_dir = Path(log_dir)
    log_files = list(log_dir.rglob("trainer_state.json"))
    if not log_files:
        raise FileNotFoundError("Файл trainer_state.json не найден в директории логов.")

    log_file = log_files[0]
    print(f"Загружен файл логов: {log_file}")

    with open(log_file, "r", encoding="utf-8") as f:
        logs = json.load(f)
    return logs["log_history"]


def analyze_jumps(logs, threshold_loss=0.1, threshold_grad_norm=1.0):
    jumps = []
    for i in range(1, len(logs)):
        prev_step = logs[i - 1]
        current_step = logs[i]

        if "loss" in current_step and "loss" in prev_step:
            loss_jump = abs(current_step["loss"] - prev_step["loss"])
            if loss_jump > threshold_loss:
                jumps.append({
                    "step": current_step.get("step", i),
                    "metric": "loss",
                    "value": current_step["loss"],
                    "jump": loss_jump
                })

        if "grad_norm" in current_step and "grad_norm" in prev_step:
            grad_norm_jump = abs(current_step["grad_norm"] - prev_step["grad_norm"])
            if grad_norm_jump > threshold_grad_norm:
                jumps.append({
                    "step": current_step.get("step", i),
                    "metric": "grad_norm",
                    "value": current_step["grad_norm"],
                    "jump": grad_norm_jump
                })

    return jumps


try:
    logs = load_logs("")
except FileNotFoundError as e:
    print(e)
    exit()

jumps = analyze_jumps(logs)

if jumps:
    print("Обнаружены скачки:")
    for jump in jumps:
        print(f"Шаг: {jump['step']}, Метрика: {jump['metric']}, "
              f"Значение: {jump['value']:.4f}, Скачок: {jump['jump']:.4f}")
else:
    print("Скачки не обнаружены.")