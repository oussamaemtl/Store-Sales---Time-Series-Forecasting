import plotly.graph_objects as go

layout = go.Layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(240,240,240,0.5)")


def plot_elasticity_vs_changepoint(df, curr, plot_width=800, plot_height=600):
    """
    Function to plot point elasticity vs. price for each group_id for a selected start date.

    Parameters:
    df (pd.DataFrame): The dataframe containing the data.
    selected_start_date (str): The start date to filter the data (format 'YYYY-MM-DD').
    plot_width (int): The width of the plot (default: 800).
    plot_height (int): The height of the plot (default: 600).
    """

    # Filter the dataframe by the selected start_date
    df_filtered = df[df["currency"] == curr]

    # Create the figure
    fig = go.Figure()

    # Plot scatter points for each group_id
    for meths in df_filtered["method"].unique():
        df_group = df_filtered[df_filtered["method"] == meths]
        # Add scatter trace for each group_id
        fig.add_trace(
            go.Scatter(
                x=df_group["start_date"],
                y=df_group["elasticity"],
                mode="markers",  # Only scatter points
                marker=dict(size=10),  # Size of scatter points
                name=f"{meths}",
            )
        )

    # Add title and labels
    fig.update_layout(
        title=f"Elasticity computed on several methods in {curr}",
        xaxis_title="change price date",
        yaxis_title="Elasticity",
        height=plot_height,  # Set size from function argument
        width=plot_width,
        legend_title="Method",
    )

    # Show the figure
    fig.show()


def plot_elasticity_vs_price(df, selected_start_date, plot_width=800, plot_height=600):
    """
    Function to plot point elasticity vs. price for each group_id for a selected start date.

    Parameters:
    df (pd.DataFrame): The dataframe containing the data.
    selected_start_date (str): The start date to filter the data (format 'YYYY-MM-DD').
    plot_width (int): The width of the plot (default: 800).
    plot_height (int): The height of the plot (default: 600).
    """

    # Filter the dataframe by the selected start_date
    df_filtered = df[df["price_change_date"] == selected_start_date]

    # Create the figure
    fig = go.Figure()

    # Plot scatter points for each group_id
    for group in df_filtered["group"].unique():
        df_group = df_filtered[df_filtered["group"] == group]
        line = df_group.line.unique()[0]
        type_ = df_group.type.unique()[0]
        # Add scatter trace for each group_id
        fig.add_trace(
            go.Scatter(
                x=df_group["price"],
                y=df_group["elasticity"],
                mode="markers",  # Only scatter points
                marker=dict(size=10),  # Size of scatter points
                name=f"{line} {type_}: {group}",
            )
        )

    # Add title and labels
    fig.update_layout(
        title=f"Elasticity vs Price for Start Date {selected_start_date}",
        xaxis_title="Price",
        yaxis_title="Elasticity",
        height=plot_height,  # Set size from function argument
        width=plot_width,
        legend_title="Group ID",
    )

    # Show the figure
    fig.show()


def plot_multiple_time_series(df, df_flag, x_axis, title, width=1000, height=600):
    """Plots all the numeric columns from a dataframe regarding the x_axis and flags dates as
        vertical bar contained in df_flag

    Keyword arguments:
    argument -- description
    Return: return_description
    """
    fig = go.Figure()
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    # Loop through each unique price_change_date to create a trace for each
    for col in numeric_cols:
        # Filter the dataframe for the current price_change_date
        df_filtered = df.copy()

        # Add a line trace for the current price_change_date
        fig.add_trace(
            go.Scatter(
                x=df_filtered[x_axis],
                y=df_filtered[col],
                mode="lines+markers",
                name=f"{col}",
            )
        )

    for date in df_flag["start_date"].unique():
        fig.add_vline(x=date, line=dict(width=2, dash="dash"))

    # Set the axis labels
    fig.update_layout(
        title=title,
        xaxis_title="merch week",
        yaxis_title="Quantities",
        legend_title="Different quantities",
        template="plotly",
        width=width,  # Set the desired width of the plot
        height=height,  # Set the desired height of the plot
    )

    # Show the figure
    fig.show()
