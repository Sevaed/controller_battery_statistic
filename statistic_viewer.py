#!/home/sevaed/.config/projects/small/controller_battery_statistic/venv/bin/python
import matplotlib.pyplot as plt
import numpy as np
import click
import time
import datetime
from dateutil.relativedelta import relativedelta

log_file = "/home/sevaed/.config/projects/small/controller_battery_statistic/log.txt"

with open(log_file, "r") as file:
    sas = file.read()


def parse_log_file(log_data):
    answer = []
    for log_string in log_data:
        data = log_string.split(" ")
        if data[0].replace(":", "") != "":
            log_time = float(data[0].replace(":", ""))
            is_connected = data[1] == "True"
            if is_connected:
                procentage = int(data[2])
                is_charging = data[3] == "True"
                answer.append((log_time, is_connected, procentage, is_charging))
            else:
                answer.append((log_time, is_connected))
    return tuple(answer)


def get_coordinates(data: tuple, type_of_graph: str) -> tuple:
    if not data:
        exit("Not enough data")
    answer = []

    relevant_data = []
    if "procentage" in type_of_graph or "charged" in type_of_graph:
        for log_entry in data:
            if log_entry[1]:
                relevant_data.append(log_entry)
    else:
        relevant_data = list(data)
    if len(relevant_data) < 2:
        exit("Not enough relevant data")
    check_time = (
        time.localtime(relevant_data[0][0]),
        time.localtime(relevant_data[-1][0]),
    )

    same_year = check_time[0].tm_year == check_time[1].tm_year
    same_month = check_time[0].tm_mon == check_time[1].tm_mon
    same_day = check_time[0].tm_mday == check_time[1].tm_mday
    same_hour = check_time[0].tm_hour == check_time[1].tm_hour
    same_minute = check_time[0].tm_min == check_time[1].tm_min

    for log_data in data:
        formatted_time, is_connected = (
            time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(log_data[0])).split("-"),
            log_data[1],
        )

        if "time" in type_of_graph:
            if not same_year:
                time_variable = f"{formatted_time[-6]}:{formatted_time[-5]}:{formatted_time[-4]}:{formatted_time[-3]}:{formatted_time[-2]}:{formatted_time[-1]}"
            elif not same_month:
                time_variable = f"{formatted_time[-5]}:{formatted_time[-4]}:{formatted_time[-3]}:{formatted_time[-2]}:{formatted_time[-1]}"
            elif not same_day:
                time_variable = f"{formatted_time[-4]}:{formatted_time[-3]}:{formatted_time[-2]}:{formatted_time[-1]}"
            elif not same_hour:
                time_variable = (
                    f"{formatted_time[-3]}:{formatted_time[-2]}:{formatted_time[-1]}"
                )
            elif not same_minute:
                time_variable = f"{formatted_time[-2]}:{formatted_time[-1]}"
            else:
                time_variable = f"{formatted_time[-1]}"
            if type_of_graph == "time_procentage" and is_connected:
                answer.append((time_variable, log_data[2]))
            if type_of_graph == "time_connected":
                answer.append((time_variable, log_data[1]))
            if type_of_graph == "time_charged" and is_connected:
                answer.append((time_variable, log_data[3]))
    coordinates = [[], []]
    for option in answer:
        coordinates[0].append(option[0])
        coordinates[1].append(option[1])
    return tuple(coordinates)


def get_data_from_log_file(
    log_file_path: str, time_limit: tuple[float, float]
) -> tuple:
    start, end = time_limit
    data = []
    with open(log_file_path, "r") as file:
        file_content = file.read()
    for string in file_content.split("\n"):
        if string and string != "\n":
            if end == -1.0:
                if start <= float(string.split(":")[0]):
                    data.append(string)
            else:
                if start <= float(string.split(":")[0]) <= end:
                    data.append(string)
    return tuple(data)


@click.command()
@click.argument("type_of_graph", nargs=1)
@click.argument("interval", nargs=1)
@click.option("-s", "--start", "start", nargs=1)
def main(type_of_graph: str, interval: str, start):
    interval_type = interval[-1]
    interval_amount = int(interval[:-1])
    if interval_type not in ["h", "d", "w", "m", "y"]:
        raise ValueError("interval must end with h/d/w/m/y")
    if not start:
        start = datetime.datetime.now()
        end = -1.0
        if interval_type == "y":
            start = start - relativedelta(year=interval_amount)
        if interval_type == "m":
            start = start - relativedelta(months=interval_amount)
        if interval_type == "w":
            start = start - relativedelta(weeks=interval_amount)
        if interval_type == "d":
            start = start - relativedelta(days=interval_amount)
        if interval_type == "h":
            start = start - relativedelta(hours=interval_amount)
    else:
        start = datetime.datetime.fromtimestamp(float(start))
        if interval_type == "y":
            end = start + relativedelta(years=interval_amount)
        elif interval_type == "m":
            end = start + relativedelta(months=interval_amount)
        elif interval_type == "w":
            end = start + relativedelta(weeks=interval_amount)
        elif interval_type == "d":
            end = start + relativedelta(days=interval_amount)
        elif interval_type == "h":
            end = start + relativedelta(hours=interval_amount)
        else:
            exit()
        end = end.timestamp()

    start = start.timestamp()
    coordinates = get_coordinates(
        parse_log_file(get_data_from_log_file(log_file, (start, end))), type_of_graph
    )
    fig, ax = plt.subplots()  # Create a figure containing a single Axes.
    ax.plot(coordinates[0], coordinates[1])
    plt.show()  # Show the figure.


def test():
    coordinates = get_coordinates(
        parse_log_file(get_data_from_log_file(log_file, (0.0, -1.0))),
        "time_procentage",
    )
    fig, ax = plt.subplots()  # Create a figure containing a single Axes.
    ax.plot(coordinates[0], coordinates[1])
    plt.show()  # Show the figure.


main()
