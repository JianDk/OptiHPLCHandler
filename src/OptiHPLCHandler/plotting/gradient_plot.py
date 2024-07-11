import plotly.graph_objects as go
import numpy as np


def plot_gradient_table(x, y) -> go.Figure:
    """
    Plots a gradient table. Doesn't take into account curve.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Flow", fill="tozeroy"))

    return fig


def standardise_gradient_table_types(gradient_table: list[dict]) -> list[dict]:
    for row in gradient_table:
        for key, value in row.items():
            if key == "Time":
                if value == "Initial":
                    continue
                row[key] = float(value)
            elif key == "Curve":
                if value == "Initial":
                    continue
                row[key] = int(value)
            else:
                row[key] = float(value)
    return gradient_table


def replace_initial_str(gradient_table: list[dict]) -> list[dict]:
    for row in gradient_table:
        for key, value in row.items():
            if value == "Initial":
                row[key] = 0
    return gradient_table


def generate_coordinates(
    gradient_table: list[dict], row_key
) -> tuple[list[float], list[float]]:
    """
    Generates x and y coordinates for the gradient table.
    """

    curve_dict = {  # the powers for each curve value
        2: 1 / 5,
        3: 1 / 4,
        4: 1 / 3,
        5: 1 / 2,
        6: 1,
        7: 2,
        8: 3,
        9: 4,
        10: 5,
    }

    gradient_table = standardise_gradient_table_types(gradient_table)
    gradient_table = replace_initial_str(gradient_table)
    x = []
    y = []
    for row in gradient_table:
        curve = row["Curve"]
        time = row["Time"]
        current_y = row[row_key]
        if curve == 0:
            # initial conditions
            pass

        elif curve == 11:
            # Stepwise at end
            # add a point prior to the step with the same composition as previous
            x.append(time - 0.01)
            y.append(previous_y)

        elif curve == 1:
            # stepwise at start
            # add a point prior to the step with the same composition as previous
            x.append(previous_time + 0.01)
            y.append(current_y)
        else:
            # numerically calculated gradient
            initial_condition = previous_y
            final_condition = current_y
            end_gradient_time_interval = time
            x_curve_to_add = np.linspace(
                previous_time + 0.01, time - 0.01, int((time - previous_time) / 0.1)
            )
            y_curve_to_add = [
                initial_condition
                + (final_condition - initial_condition)
                * (
                    (time - previous_time)
                    / (end_gradient_time_interval - previous_time)
                )
                ** curve_dict[curve]
                for time in x_curve_to_add
            ]
            x.extend(x_curve_to_add)
            y.extend(y_curve_to_add)

        previous_time = time
        previous_y = current_y
        x.append(time)
        y.append(current_y)

    return x, y
