import plotly.express as  px
import plotly.graph_objects as go

from plotly.subplots import make_subplots

def plot_interval(gantt_table):
    gantt_fig = px.timeline(
        gantt_table, 
        x_start='start', 
        x_end='end', 
        y='index'
    )
    
    gantt_fig.update_layout(title='資料集起迄時間')
    gantt_fig.update_yaxes(title='醫院名稱')
    gantt_fig.update_xaxes(title='日期')
    
    return gantt_fig

def plot_time_series(data, x='', cols=[], title=''):
    fig = px.line(data, x=x, y=cols)
    fig.update_layout(title=title)
    return fig

def plot_stl(timestamp, stl_result, column_name=''):

    fig = make_subplots(
        rows=4, 
        cols=1,
    )

    fig.add_trace(
        go.Scatter(
            x=timestamp,
            y=stl_result.observed,
            name='observation',
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=timestamp,
            y=stl_result.trend,
            name='trend',
        ),
        row=2,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=timestamp,
            y=stl_result.seasonal,
            name='seasonal',
        ),
        row=3,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=timestamp,
            y=stl_result.resid,
            name='resid',
        ),
        row=4,
        col=1,
    )

    fig.update_layout(
        title=f"{column_name} STL Decompose Result.",
        height=800,
    )

    fig.update_xaxes(title='Datetime', row=4, col=1)

    fig.update_yaxes(title_text='Observation', row=1, col=1)
    fig.update_yaxes(title_text='Trend', row=2, col=1)
    fig.update_yaxes(title_text='Seasonal', row=3, col=1)
    fig.update_yaxes(title_text='Residual', row=4, col=1)

    return fig

def plot_acf(acf_values, bounds):
    indeces = [idx for idx in range(len(acf_values))]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=indeces,
            y=acf_values,
            name='ACF value',
            width=0.8,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=indeces[1:],
            y=bounds[0],
            fill='tonexty',
            line_color='green'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=indeces[1:],
            y=bounds[1],
            fill='tonexty',
            line_color='green'
        )
    )

    fig.update_layout(
        title='ACF plot'
    )

    fig.update_xaxes(
        title='lags'
    )

    fig.update_yaxes(
        title='ACF value'
    )
    
    return fig
    
def plot_pacf(pacf_values, bounds):
    indeces = [idx for idx in range(len(pacf_values))]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=indeces,
            y=pacf_values,
            name='PACF value',
            width=0.8,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=indeces[1:],
            y=bounds[0],
            fill='tonexty',
            line_color='green'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=indeces[1:],
            y=bounds[1],
            fill='tonexty',
            line_color='green'
        )
    )

    fig.update_layout(
        title='PACF plot'
    )

    fig.update_xaxes(
        title='lags'
    )

    fig.update_yaxes(
        title='PACF value'
    )
    return fig