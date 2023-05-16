import pandas as pd
import plotly.express as px


# factor, timeframe, top, mkt cap
# query respective factor table with these vars and gets records
def cumulative_returns(df: pd.DataFrame):
    returns_col = [c for c in df.columns
                   if c.split('_')[-1] == 'return'
                   ][0]

    records = df[['pricing_date', returns_col]].to_records(index=False)

    res = []
    temp_rtn = 1
    for record in records:
        if record[1] != 0:
            temp_rtn = temp_rtn * (1 + record[1])
            res.append((record[0], temp_rtn))

    r_df = pd.DataFrame.from_records(res, columns=['date', 'return'])

    fig = px.line(r_df,
                  x='date',
                  y='return',
                  title=returns_col.replace("_", " "))

    fig.update_xaxes(
        title='date',
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
    )
    fig.update_yaxes(
        title='return',
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    fig.update_layout(plot_bgcolor='white')

    fig.show()


# factor, timeframe, top, mkt cap
# query respective factor table with these vars and gets records
def long_short(df):
    x = 'pricing_date'
    y1 = [c for c in df.columns
          if c.split('_')[-1] == 'long'
          ][0]
    y2 = [c for c in df.columns
          if c.split('_')[-1] == 'short'
          ][0]
    fig = px.line(
        df,
        x=df[x],
        y=df[y1],
        title=f'{y1.replace("_", " ")} | {y2.replace("_", " ")}'
    )
    fig.add_scatter(x=df[x], y=df[y2], mode='lines')

    fig.update_xaxes(
        title='date',
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
    )
    fig.update_yaxes(
        title='return',
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )

    fig.show()
