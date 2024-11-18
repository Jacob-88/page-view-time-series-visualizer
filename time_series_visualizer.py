import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
# Lower and upper quantile
lower_quantile = df['value'].quantile(0.025)
upper_quantile = df['value'].quantile(0.975)
# Filtering data
df = df[(df['value'] >= lower_quantile) & (df['value'] <= upper_quantile)]


def draw_line_plot():
    # Draw line plot
    # Create fig and ax
    fig, ax = plt.subplots(figsize=(15, 5))

    # Building a linear graph
    ax.plot(df.index, df['value'], color='red', linewidth=1)

    # Set title and labels
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # Add columns 'year' and 'month' as numerical values
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Create a mapping from month numbers to month names
    months_order = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }

    # Map month numbers to month names
    df_bar['month'] = df_bar['month'].map(months_order)

    # Ensure 'month' is a categorical variable with the correct order
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=list(months_order.values()), ordered=True)

    # Group data and calculate average
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().reset_index()

    # Optional: Check the number of bars
    # print("Number of bars in bar plot:", len(df_bar))

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='year', y='value', hue='month', data=df_bar, palette='tab10', ax=ax)

    # Labels and legend
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months', loc='upper left')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    months_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    df_box['month'] = pd.Categorical(df_box['month'], categories=months_order, ordered=True)

    # Draw box plots (using Seaborn)
    # Create figure and axes
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))
    
    # Year-wise Box Plot
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    
    # Month-wise Box Plot
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig