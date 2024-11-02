import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

layout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(240,240,240,0.5)'
    )

def plot_time_serie(graph_data, time_axis, y_axis, graph_title, df_bar, time_axis_df_bar, height = 600, width = 1000):
   """This functions plot a time serie with relevant flag date that appeared as vertical lines
   
   Keyword arguments:
   argument -- graph_data : time_serie to plot
               df_bar: dataframe containing flag dates that will appear as vertical lines
   Return: plot of graph_data with vertical bar that flags some dates
   """
   
   fig = go.Figure( layout=layout)

   fig.add_trace(
       go.Scatter(
          x= graph_data[time_axis],
          y= graph_data[y_axis], 
          mode='lines',
          ),
    )

   if df_bar is not None:
      for date_ in df_bar[time_axis_df_bar].unique():
         fig.add_vline(date_)

   fig.update_layout(
      title_text=graph_title,
      autosize=False,
      width=width,
      height=height,
      plot_bgcolor='white',  # Fond blanc
      paper_bgcolor='white',  # Fond blanc extérieur
      xaxis=dict(
         showgrid=True,
         gridcolor='black',  # Quadrillage noir
         gridwidth=1,
         tickmode='auto',
      ),
      yaxis=dict(
         showgrid=True,
         gridcolor='black',  # Quadrillage noir
         gridwidth=1,
         autorange=True,  # Ajustement automatique des ordonnées
         rangemode='tozero',  # S'ajuste aux valeurs sans marge en bas
      ),
   )

   fig.show()