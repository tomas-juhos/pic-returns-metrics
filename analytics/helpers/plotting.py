import pandas as pd
import plotly.graph_objects as go


def cumulative_return(returns: pd.Series):
    """Calculates total cumulative returns.

    A cumulative return on an investment is the aggregate amount that the
    investment has gained or lost over time, independent of the amount of time
    involved.

    The cumulative return is expressed as a percentage, and it is the raw
    mathematical return of the following calculation:
        (current_price - original_price) / original_price

    Args:
        returns: Daily returns.

    Returns:
        Cumulative returns.
    """
    return returns.add(1).prod() - 1


def group_returns(returns: pd.Series) -> pd.Series:
    """Groups returns by group_by value.

    Args:
        returns: returns pd.Series.

    Returns:
        returns pd.Series grouped by group_by element.
    """
    return returns.groupby(pd.Grouper(freq='M')).apply(cumulative_return)


def portfolio_returns(portfolio, benchmark, file_name):
    pcr = portfolio

    # CURRENTLY USING MOCKUP BENCHMARK
    bcr = benchmark

    figure = go.Figure(data=go.Scatter(
        x=pcr.index,
        y=pcr['Rtn'],
        name='Strategy',
        line=dict(color='firebrick'), showlegend=True
    ))
    figure.add_trace(go.Scatter(
        x=pcr.index,
        y=pcr['Net_Rtn'],
        name='Strategy (Net)',
        line=dict(color='crimson'), showlegend=True
    ))
    figure.add_trace(go.Scatter(
        x=bcr.index,
        y=bcr['Rtn'],
        name='Benchmark',
        line=dict(color='rgba(100,100,100,1)'),
        showlegend=True
    ))
    figure.update_layout(
        height=227 * 2,
        width=491 * 2,
        margin=dict(l=40, r=20, t=0, b=0),  # add padding
        xaxis=dict(
            tickfont=dict(size=10),
            tickangle=45,
            tickmode='auto',
            nticks=10,
            tickformat='%Y'
        ),
        yaxis=dict(
            tickfont=dict(size=10),
            tickformat=".1%",
            rangemode='tozero',
            zeroline=True,
            zerolinecolor='lightgrey'
        ),
        legend=dict(x=0, y=1),
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x'
    )
    figure.update_layout(
        plot_bgcolor='white',
    )

    figure.update_xaxes(
        mirror=False,
        ticks='outside',
        showline=True,
        linecolor='black',
    )
    figure.update_yaxes(
        mirror=False,
        showline=True,
        ticks='outside',
        gridcolor='lightgrey',
        linecolor='black',
    )

    figure.write_image(f"images/{file_name}.png")


def histogram(portfolio, benchmark, file_name, strat_bins):
    portfolio_monthly_returns = group_returns(portfolio)
    benchmark_monthly_returns = group_returns(benchmark)

    avg_portfolio_return = portfolio_monthly_returns['Net_Rtn'].mean()
    avg_benchmark_return = benchmark_monthly_returns['Net_Rtn'].mean()

    figure = go.Figure()
    figure.add_trace(go.Histogram(
        name='Benchmark',
        x=benchmark_monthly_returns['Net_Rtn'],
        autobinx=False,
        nbinsx=20,
        marker=dict(color='rgba(100,100,100,1)')
    ))
    figure.add_trace(go.Histogram(
        name='Strategy',
        x=portfolio_monthly_returns['Net_Rtn'],
        autobinx=False,
        nbinsx=strat_bins,
        marker=dict(color='crimson')
    ))
    # Overlay both histograms
    figure.update_layout(barmode='overlay')
    # Reduce opacity to see both histograms
    figure.update_traces(opacity=0.6)
    figure.update_layout(
        plot_bgcolor='white',
        height=227 * 2,
        width=491 * 2,
        margin=dict(l=40, r=20, t=0, b=0),  # add padding
        legend=dict(x=0, y=1),
        hovermode='x'
    )

    figure.add_shape(
        type="line",
        x0=avg_portfolio_return,
        y0=0,
        x1=avg_portfolio_return,
        y1=20,
        line=dict(color='darkred', dash='dot'),
    )
    figure.add_shape(
        type="line",
        x0=avg_benchmark_return,
        y0=0,
        x1=avg_benchmark_return,
        y1=20,
        line=dict(color='black', dash='dot'),
    )

    figure.update_xaxes(
        mirror=False,
        ticks='outside',
        showline=True,
        linecolor='black',
    )
    figure.update_yaxes(
        mirror=False,
        showline=True,
        ticks='outside',
        gridcolor='lightgrey',
        linecolor='black',
    )

    figure.write_image(f"images/{file_name}.png")


def calendar_returns(df, file_name):
    figure = go.Figure()
    figure.add_trace(go.Bar(
        x=df['Year'],
        y=df['Strategy (%)'],
        name='Strategy',
        marker=dict(color='crimson'),
    ))
    figure.add_trace(go.Bar(
        x=df['Year'],
        y=df['Benchmark (%)'],
        name='Benchmark',
        marker=dict(color='rgba(100,100,100,1)'),
    ))

    # add horizontal line for average of Strategy column
    avg_strategy = df['Strategy (%)'].mean()
    figure.add_shape(
        type="line",
        x0=df['Year'].min(), y0=avg_strategy,
        x1=df['Year'].max(), y1=avg_strategy,
        line=dict(color="gray", width=1, dash="dot")
    )
    figure.add_annotation(
        x=df['Year'].min(), y=avg_strategy,
        text=f"{avg_strategy:.2f}%",
        showarrow=False, yshift=10
    )

    figure.update_layout(
        barmode='group',
        # FIGURE SIZE HERE
        height=204 * 2,
        width=453 * 2,
        margin=dict(l=40, r=20, t=0, b=0),  # add padding
        xaxis=dict(
            tickfont=dict(size=10),
            tickangle=45,
            tickmode='linear',
            tick0=df['Year'].min(),
            dtick=1,
            tickvals=df['Year'],
            ticktext=df['Year'],
        ),
        yaxis=dict(
            title='Returns (%)',
            tickfont=dict(size=10),
            zeroline=True,
            zerolinecolor='lightgrey'
        ),
        legend=dict(x=0, y=1, traceorder='normal', font=dict(size=10)),
    )
    figure.update_layout(
        plot_bgcolor='white',
    )

    figure.update_xaxes(
        mirror=False,
        ticks='outside',
        showline=True,
        linecolor='black',
    )
    figure.update_yaxes(
        mirror=False,
        showline=True,
        ticks='outside',
        gridcolor='lightgrey',
        linecolor='black',
    )

    figure.write_image(f"images/{file_name}.png")


def average_daily_return(df, file_name):
    pr = df
    avg_daily_return = pr['Net_Rtn'].mean()
    figure = go.Figure(data=go.Scatter(
        x=pr.index,
        y=pr['Rtn'],
        name='Strategy',
        line=dict(color='crimson', width=1),
        showlegend=True,
    ))

    figure.add_shape(
        type="line",
        x0=pr.index[0],
        y0=avg_daily_return,
        x1=pr.index[-1],
        y1=avg_daily_return,
        line=dict(color='black', dash='dot'),
    )

    figure.add_annotation(
        x=pr.index[0],
        y=avg_daily_return,
        text=f"Average Daily Return: {avg_daily_return:.2f}%",
        showarrow=False,
        xanchor='left',
        yanchor='bottom',
        xshift=5,
        font=dict(size=10),
    )

    figure.update_layout(
        height=204 * 2,
        width=453 * 2,
        margin=dict(l=40, r=20, t=0, b=0),
        xaxis=dict(
            tickfont=dict(size=10),
            tickangle=45,
            tickmode='auto',
            nticks=10,
            tickformat='%Y'
        ),
        yaxis=dict(
            zeroline=True,
            zerolinecolor='lightgrey'
        ),
        legend=dict(x=0.9, y=1),
    )
    figure.update_layout(
        plot_bgcolor='white',
    )

    figure.update_xaxes(
        mirror=False,
        ticks='outside',
        showline=True,
        linecolor='black',
    )
    figure.update_yaxes(
        mirror=False,
        showline=True,
        ticks='outside',
        gridcolor='lightgrey',
        linecolor='black',
    )

    figure.write_image(f"images/{file_name}.png")




