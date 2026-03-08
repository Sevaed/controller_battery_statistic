import subprocess
import time

log_file = "/home/sevaed/.config/projects/small/controller_battery_statistic/log.txt"
buffer = ""


def is_controller_connected() -> bool:
    try:
        subprocess.check_output(["dualsensectl", "battery"])
    except subprocess.CalledProcessError:
        return False
    else:
        return True


def get_battery_status() -> tuple[int, bool]:
    output = subprocess.check_output(
        ["dualsensectl", "battery"], universal_newlines=True
    ).split(" ")
    procentage = int(output[0])
    is_charging = None
    if output[1] == "discharging\n":
        is_charging = False
    else:
        is_charging = True
    return (procentage, is_charging)


with open(log_file, "a") as file:
    while True:
        if is_controller_connected():
            battery_status = get_battery_status()
            data = f"True {battery_status[0]} {battery_status[1]}\n"
        else:
            data = f"False\n"
        if buffer != data:
            buffer = data
            print(str(time.time()) + ": " + buffer)
            file.write(str(time.time()) + ": " + buffer)
            file.flush()
