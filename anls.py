import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # Set backend before importing pyplot
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns
import ctypes
from ctypes import wintypes

# Prevent matplotlib from showing default figures
plt.ioff()  # Turn off interactive mode

# Load and prepare data
import os
# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'UM_C19_2021.csv')

# Check if file exists
if not os.path.exists(csv_path):
    print(f"Error: CSV file not found at {csv_path}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script directory: {script_dir}")
    print("Available files in script directory:")
    for file in os.listdir(script_dir):
        if file.endswith('.csv'):
            print(f"  - {file}")
    exit(1)

df = pd.read_csv(csv_path)
df['Date'] = pd.to_datetime(df['Date'])

# Separate residential and non-residential data
residential_data = df[df['residence'].str.contains('Residential', na=False)]
non_residential_data = df[~df['residence'].str.contains('Residential', na=False)]

# Separate Students and Faculty/Staff
students_data = df[df['Type'].astype(str).str.contains('Students', na=False)]
faculty_staff_data = df[df['Type'].astype(str).str.contains('Faculty/Staff', na=False)]

# Create daily summaries for each group
residential_daily = residential_data.groupby('Date')[['Positive', 'Negative']].sum()
non_residential_daily = non_residential_data.groupby('Date')[['Positive', 'Negative']].sum()

# Create daily summaries for Students vs Faculty/Staff
students_daily = students_data.groupby('Date')[['Positive', 'Negative']].sum()
faculty_staff_daily = faculty_staff_data.groupby('Date')[['Positive', 'Negative']].sum()

# Calculate cumulative sums
residential_daily['Cumulative_Positive'] = residential_daily['Positive'].cumsum()
non_residential_daily['Cumulative_Positive'] = non_residential_daily['Positive'].cumsum()


students_daily['Cumulative_Positive'] = students_daily['Positive'].cumsum()
faculty_staff_daily['Cumulative_Positive'] = faculty_staff_daily['Positive'].cumsum()

# Combined daily summary (for backward compatibility)
daily_summary = df.groupby('Date')[['Positive', 'Negative']].sum()
daily_summary['Cumulative_Positive'] = daily_summary['Positive'].cumsum()

# Create 30-day aggregated data
def create_30day_aggregated_data(daily_data):
    """Aggregate daily data into 30-day periods"""
    # Reset index to work with dates
    data = daily_data.reset_index()
    
    # Create 30-day periods using a more reliable method
    # Calculate days since first date and group by 30-day intervals
    data['Days_Since_Start'] = (data['Date'] - data['Date'].min()).dt.days
    data['Period_Group'] = data['Days_Since_Start'] // 30
    
    # Group by 30-day periods and sum
    aggregated = data.groupby('Period_Group').agg({
        'Positive': 'sum',
        'Negative': 'sum',
        'Date': 'first'  # Take the first date of each period
    }).reset_index()
    
    # Set the first date of each period as the index
    aggregated.set_index('Date', inplace=True)
    aggregated['Cumulative_Positive'] = aggregated['Positive'].cumsum()
    
    # Remove the Period_Group column
    aggregated = aggregated.drop('Period_Group', axis=1)
    
    return aggregated

# Create different time period aggregated data
def create_weekly_aggregated_data(daily_data):
    """Aggregate daily data into weekly periods"""
    data = daily_data.reset_index()
    data['Week'] = data['Date'].dt.to_period('W')
    aggregated = data.groupby('Week').agg({
        'Positive': 'sum',
        'Negative': 'sum',
        'Date': 'first'
    }).reset_index()
    aggregated.set_index('Date', inplace=True)
    aggregated['Cumulative_Positive'] = aggregated['Positive'].cumsum()
    return aggregated

def create_monthly_aggregated_data(daily_data):
    """Aggregate daily data into monthly periods"""
    data = daily_data.reset_index()
    data['Month'] = data['Date'].dt.to_period('M')
    aggregated = data.groupby('Month').agg({
        'Positive': 'sum',
        'Negative': 'sum',
        'Date': 'first'
    }).reset_index()
    aggregated.set_index('Date', inplace=True)
    aggregated['Cumulative_Positive'] = aggregated['Positive'].cumsum()
    return aggregated

# Create all time period summaries
daily_summary_30d = create_30day_aggregated_data(daily_summary)
residential_daily_30d = create_30day_aggregated_data(residential_daily)
non_residential_daily_30d = create_30day_aggregated_data(non_residential_daily)

# Students / Faculty 30-day aggregated summaries
students_daily_30d = create_30day_aggregated_data(students_daily)
faculty_staff_daily_30d = create_30day_aggregated_data(faculty_staff_daily)

# Weekly data
daily_summary_weekly = create_weekly_aggregated_data(daily_summary)
residential_daily_weekly = create_weekly_aggregated_data(residential_daily)
non_residential_daily_weekly = create_weekly_aggregated_data(non_residential_daily)

students_daily_weekly = create_weekly_aggregated_data(students_daily)
faculty_staff_daily_weekly = create_weekly_aggregated_data(faculty_staff_daily)

# Monthly data
daily_summary_monthly = create_monthly_aggregated_data(daily_summary)
residential_daily_monthly = create_monthly_aggregated_data(residential_daily)
non_residential_daily_monthly = create_monthly_aggregated_data(non_residential_daily)

students_daily_monthly = create_monthly_aggregated_data(students_daily)
faculty_staff_daily_monthly = create_monthly_aggregated_data(faculty_staff_daily)

# Debug: Print information about the aggregated data
print("30-Day Aggregated Data Summary:")
print(f"Daily data points: {len(daily_summary)}")
print(f"30-day aggregated points: {len(daily_summary_30d)}")
print(f"Date range: {daily_summary_30d.index.min()} to {daily_summary_30d.index.max()}")
print(f"Total positive cases (30-day): {daily_summary_30d['Positive'].sum()}")
print(f"Total positive cases (daily): {daily_summary['Positive'].sum()}")
print("\nFirst few 30-day periods:")
print(daily_summary_30d.head())

# Analysis Functions
def analyze_peak_infection_period(data, window_days=7, top_n=3):
    """
    Analyze peak infection time periods by finding the highest infection rates
    over rolling windows.
    
    Parameters:
    - data: DataFrame with Date index and Positive column
    - window_days: Number of days for rolling window (default: 7)
    - top_n: Number of top peak periods to return (default: 3)
    
    Returns:
    - Dictionary with peak periods information
    """
    # Calculate rolling average for the specified window
    data['Rolling_Avg'] = data['Positive'].rolling(window=window_days, center=True).mean()
    
    # Find the top peak periods
    peak_periods = data.nlargest(top_n, 'Rolling_Avg')
    
    results = {
        'window_days': window_days,
        'peak_periods': [],
        'overall_stats': {
            'max_daily_cases': data['Positive'].max(),
            'max_rolling_avg': data['Rolling_Avg'].max(),
            'total_positive_cases': data['Positive'].sum(),
            'date_range': f"{data.index.min().strftime('%Y-%m-%d')} to {data.index.max().strftime('%Y-%m-%d')}"
        }
    }
    
    for i, (date, row) in enumerate(peak_periods.iterrows(), 1):
        peak_info = {
            'rank': i,
            'date': date.strftime('%Y-%m-%d'),
            'daily_cases': row['Positive'],
            'rolling_avg': round(row['Rolling_Avg'], 2),
            'week_start': (date - timedelta(days=window_days//2)).strftime('%Y-%m-%d'),
            'week_end': (date + timedelta(days=window_days//2)).strftime('%Y-%m-%d')
        }
        results['peak_periods'].append(peak_info)
    
    return results

def analyze_growth_trends(data, periods=30):
    """
    Analyze growth trends by comparing different time periods.

    Parameters:
    - data: DataFrame with Date index and Positive column
    - periods: Number of days to compare (default: 30)

    Returns:
    - Dictionary with growth analysis
    """
    total_days = len(data)
    results = {
        'period_days': periods,
        'growth_analysis': []
    }

    # Split data into periods
    for i in range(0, total_days, periods):
        period_data = data.iloc[i:i+periods]
        if len(period_data) > 0:
            period_info = {
                'period': f"Period {i//periods + 1}",
                'start_date': period_data.index[0].strftime('%Y-%m-%d'),
                'end_date': period_data.index[-1].strftime('%Y-%m-%d'),
                'total_cases': period_data['Positive'].sum(),
                'avg_daily_cases': round(period_data['Positive'].mean(), 2),
                'max_daily_cases': period_data['Positive'].max(),
                'growth_rate': round(period_data['Positive'].sum() / len(period_data), 2)
            }
            results['growth_analysis'].append(period_info)

    return results

def analyze_seasonal_patterns(data):
    """
    Analyze seasonal patterns in COVID-19 data by examining monthly and seasonal trends.

    Parameters:
    - data: DataFrame with Date index and Positive column

    Returns:
    - Dictionary with seasonal analysis including monthly patterns, seasonal comparisons,
      and peak/low seasons
    """
    import calendar

    # Create seasonal categories
    seasons = {
        'Winter': [12, 1, 2],
        'Spring': [3, 4, 5],
        'Summer': [6, 7, 8],
        'Fall': [9, 10, 11]
    }

    results = {
        'monthly_analysis': [],
        'seasonal_analysis': {},
        'seasonal_insights': {},
        'yearly_comparison': []
    }

    # Monthly analysis
    monthly_data = data.groupby(data.index.month).agg({
        'Positive': ['sum', 'mean', 'max', 'count']
    }).round(2)

    monthly_data.columns = ['total_cases', 'avg_daily', 'peak_daily', 'days_counted']

    for month in range(1, 13):
        if month in monthly_data.index:
            month_data = monthly_data.loc[month]
            month_info = {
                'month': calendar.month_name[month],
                'month_num': month,
                'total_cases': int(month_data['total_cases']),
                'avg_daily_cases': round(month_data['avg_daily'], 2),
                'peak_daily_cases': int(month_data['peak_daily']),
                'days_counted': int(month_data['days_counted'])
            }
            results['monthly_analysis'].append(month_info)

    # Seasonal analysis
    for season_name, season_months in seasons.items():
        season_data = data[data.index.month.isin(season_months)]

        if len(season_data) > 0:
            seasonal_stats = {
                'total_cases': int(season_data['Positive'].sum()),
                'avg_daily_cases': round(season_data['Positive'].mean(), 2),
                'peak_daily_cases': int(season_data['Positive'].max()),
                'days_counted': len(season_data),
                'case_density': round(season_data['Positive'].sum() / len(season_data), 2)
            }
            results['seasonal_analysis'][season_name] = seasonal_stats

    # Seasonal insights
    if results['seasonal_analysis']:
        seasonal_totals = {season: stats['total_cases']
                          for season, stats in results['seasonal_analysis'].items()}

        peak_season = max(seasonal_totals, key=seasonal_totals.get)
        low_season = min(seasonal_totals, key=seasonal_totals.get)

        results['seasonal_insights'] = {
            'peak_season': {
                'season': peak_season,
                'total_cases': seasonal_totals[peak_season],
                'avg_daily': results['seasonal_analysis'][peak_season]['avg_daily_cases']
            },
            'low_season': {
                'season': low_season,
                'total_cases': seasonal_totals[low_season],
                'avg_daily': results['seasonal_analysis'][low_season]['avg_daily_cases']
            },
            'seasonal_variation': round(
                (seasonal_totals[peak_season] - seasonal_totals[low_season]) /
                seasonal_totals[low_season] * 100, 1
            )
        }

    # Yearly comparison (if data spans multiple years)
    if len(data) > 365:  # Only if we have more than a year of data
        yearly_data = data.groupby(data.index.year).agg({
            'Positive': ['sum', 'mean', 'max']
        }).round(2)

        yearly_data.columns = ['total_cases', 'avg_daily', 'peak_daily']

        for year in yearly_data.index:
            year_info = {
                'year': int(year),
                'total_cases': int(yearly_data.loc[year, 'total_cases']),
                'avg_daily_cases': round(yearly_data.loc[year, 'avg_daily'], 2),
                'peak_daily_cases': int(yearly_data.loc[year, 'peak_daily'])
            }
            results['yearly_comparison'].append(year_info)

    return results

def plot_seasonal_patterns(data, title="Seasonal COVID-19 Patterns"):
    """
    Create a comprehensive seasonal analysis plot showing monthly and seasonal trends.

    Parameters:
    - data: DataFrame with Date index and Positive column
    - title: Title for the plot

    Returns:
    - matplotlib figure with seasonal analysis
    """
    import calendar
    import matplotlib.pyplot as plt

    # Create seasonal categories
    seasons = {
        'Winter': [12, 1, 2],
        'Spring': [3, 4, 5],
        'Summer': [6, 7, 8],
        'Fall': [9, 10, 11]
    }

    # Set up the plot with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(title, fontsize=16, fontweight='bold')

    # 1. Monthly cases plot
    monthly_data = data.groupby(data.index.month)['Positive'].sum()
    month_labels = [calendar.month_abbr[i] for i in range(1, 13)]
    ax1.bar(range(1, 13), monthly_data.values, color='skyblue', alpha=0.7)
    ax1.set_title('Monthly Case Distribution')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Total Cases')
    ax1.set_xticks(range(1, 13))
    ax1.set_xticklabels(month_labels, rotation=45)
    ax1.grid(True, alpha=0.3)

    # 2. Seasonal cases plot
    seasonal_totals = {}
    for season_name, season_months in seasons.items():
        season_data = data[data.index.month.isin(season_months)]
        seasonal_totals[season_name] = season_data['Positive'].sum()

    colors = ['lightblue', 'lightgreen', 'orange', 'lightcoral']
    ax2.bar(seasonal_totals.keys(), seasonal_totals.values(), color=colors, alpha=0.7)
    ax2.set_title('Seasonal Case Distribution')
    ax2.set_xlabel('Season')
    ax2.set_ylabel('Total Cases')
    ax2.grid(True, alpha=0.3)

    # Add value labels on bars
    for i, (season, total) in enumerate(seasonal_totals.items()):
        ax2.text(i, total + max(seasonal_totals.values()) * 0.02,
                f'{total:,}', ha='center', va='bottom', fontweight='bold')

    # 3. Average daily cases by month
    monthly_avg = data.groupby(data.index.month)['Positive'].mean()
    ax3.plot(range(1, 13), monthly_avg.values, 'o-', color='darkblue',
             linewidth=2, markersize=6, markerfacecolor='lightblue')
    ax3.fill_between(range(1, 13), monthly_avg.values, alpha=0.3, color='lightblue')
    ax3.set_title('Average Daily Cases by Month')
    ax3.set_xlabel('Month')
    ax3.set_ylabel('Average Daily Cases')
    ax3.set_xticks(range(1, 13))
    ax3.set_xticklabels(month_labels, rotation=45)
    ax3.grid(True, alpha=0.3)

    # 4. Year-over-year comparison (if available)
    if len(data) > 365:
        yearly_data = data.groupby(data.index.year)['Positive'].sum()
        ax4.bar(yearly_data.index.astype(str), yearly_data.values,
                color='coral', alpha=0.7)
        ax4.set_title('Year-over-Year Case Totals')
        ax4.set_xlabel('Year')
        ax4.set_ylabel('Total Cases')
        ax4.grid(True, alpha=0.3)

        # Add value labels
        for i, (year, total) in enumerate(yearly_data.items()):
            ax4.text(i, total + max(yearly_data.values) * 0.02,
                    f'{total:,}', ha='center', va='bottom', fontweight='bold')
    else:
        # If not enough data for yearly comparison, show daily pattern
        daily_pattern = data.groupby(data.index.dayofweek)['Positive'].mean()
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        ax4.plot(range(7), daily_pattern.values, 'o-', color='purple',
                 linewidth=2, markersize=6, markerfacecolor='violet')
        ax4.fill_between(range(7), daily_pattern.values, alpha=0.3, color='violet')
        ax4.set_title('Average Cases by Day of Week')
        ax4.set_xlabel('Day of Week')
        ax4.set_ylabel('Average Daily Cases')
        ax4.set_xticks(range(7))
        ax4.set_xticklabels(days)
        ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

def plot_residential_comparison(residential_data, non_residential_data):
    """
    Create side-by-side plots comparing residential vs non-residential statistics.
    
    Parameters:
    - residential_data: DataFrame with residential cases
    - non_residential_data: DataFrame with non-residential cases
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), sharey=True)
    
    # Plot 1: Residential Cases
    ax1.plot(residential_data.index, residential_data['Positive'], 
             label='Daily Positive Cases', color='blue', alpha=0.7, marker='o', markersize=3)
    ax1.plot(residential_data.index, residential_data['Cumulative_Positive'], 
             label='Cumulative Positive Cases', color='darkblue', linewidth=2)
    ax1.plot(residential_data.index, residential_data['Negative'], 
             label='Daily Negative Cases', color='lightblue', alpha=0.7, marker='s', markersize=3)
    
    ax1.set_title('Residential Cases', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Number of Cases')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Add statistics text box for residential
    res_stats = f"""Residential Statistics:
Total Positive: {residential_data['Positive'].sum():,}
Total Negative: {residential_data['Negative'].sum():,}
Max Daily Positive: {residential_data['Positive'].max():,}
Avg Daily Positive: {residential_data['Positive'].mean():.1f}"""
    ax1.text(0.02, 0.98, res_stats, transform=ax1.transAxes, fontsize=9,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Plot 2: Non-Residential Cases
    ax2.plot(non_residential_data.index, non_residential_data['Positive'], 
             label='Daily Positive Cases', color='red', alpha=0.7, marker='o', markersize=3)
    ax2.plot(non_residential_data.index, non_residential_data['Cumulative_Positive'], 
             label='Cumulative Positive Cases', color='darkred', linewidth=2)
    ax2.plot(non_residential_data.index, non_residential_data['Negative'], 
             label='Daily Negative Cases', color='lightcoral', alpha=0.7, marker='s', markersize=3)
    
    ax2.set_title('Non-Residential Cases', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Number of Cases')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Add statistics text box for non-residential
    non_res_stats = f"""Non-Residential Statistics:
Total Positive: {non_residential_data['Positive'].sum():,}
Total Negative: {non_residential_data['Negative'].sum():,}
Max Daily Positive: {non_residential_data['Positive'].max():,}
Avg Daily Positive: {non_residential_data['Positive'].mean():.1f}"""
    ax2.text(0.02, 0.98, non_res_stats, transform=ax2.transAxes, fontsize=9,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
    
    plt.suptitle('COVID-19 Cases: Residential vs Non-Residential Comparison', 
                 fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    # Removed plt.show() to avoid spawning extra figure windows; figures are embedded in Tkinter.

def plot_peak_analysis(data, peak_results):
    """
    Create a visualization showing peak infection periods.
    
    Parameters:
    - data: DataFrame with Date index and Positive column
    - peak_results: Results from analyze_peak_infection_period function
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    
    # Plot 1: Daily cases with rolling average
    ax1.plot(data.index, data['Positive'], alpha=0.6, label='Daily Cases', color='lightblue')
    ax1.plot(data.index, data['Rolling_Avg'], label=f'{peak_results["window_days"]}-day Rolling Average', 
             color='red', linewidth=2)
    
    # Highlight peak periods
    for peak in peak_results['peak_periods']:
        peak_date = pd.to_datetime(peak['date'])
        ax1.axvline(x=peak_date, color='orange', linestyle='--', alpha=0.7)
        ax1.annotate(f"Peak {peak['rank']}\n{peak['date']}", 
                    xy=(peak_date, peak['rolling_avg']), 
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    ax1.set_title('Daily COVID-19 Cases with Peak Periods Highlighted')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Number of Cases')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Bar chart of top peak periods
    peak_dates = [peak['date'] for peak in peak_results['peak_periods']]
    peak_values = [peak['rolling_avg'] for peak in peak_results['peak_periods']]
    
    bars = ax2.bar(range(len(peak_dates)), peak_values, color=['red', 'orange', 'yellow'][:len(peak_dates)])
    ax2.set_title('Top Peak Infection Periods (Rolling Average)')
    ax2.set_xlabel('Peak Period Rank')
    ax2.set_ylabel('Average Cases per Day')
    ax2.set_xticks(range(len(peak_dates)))
    ax2.set_xticklabels([f"Peak {i+1}\n{date}" for i, date in enumerate(peak_dates)])
    
    # Add value labels on bars
    for bar, value in zip(bars, peak_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(peak_values)*0.01,
                f'{value}', ha='center', va='bottom')
    
# Removed global plt.show() to prevent extra figure windows when using Tkinter embedding.
plt.tight_layout()

def print_analysis_summary(peak_results, growth_results):
    """
    Print a formatted summary of the analysis results.
    """
    print("="*60)
    print("COVID-19 INFECTION ANALYSIS SUMMARY")
    print("="*60)
    
    # Overall statistics
    stats = peak_results['overall_stats']
    print(f"\n📊 OVERALL STATISTICS:")
    print(f"   Date Range: {stats['date_range']}")
    print(f"   Total Positive Cases: {stats['total_positive_cases']:,}")
    print(f"   Maximum Daily Cases: {stats['max_daily_cases']:,}")
    print(f"   Maximum {peak_results['window_days']}-day Average: {stats['max_rolling_avg']:.2f}")
    
    # Peak periods
    print(f"\n🔥 TOP {len(peak_results['peak_periods'])} PEAK INFECTION PERIODS:")
    for peak in peak_results['peak_periods']:
        print(f"   Peak {peak['rank']}: {peak['date']}")
        print(f"      • Daily Cases: {peak['daily_cases']:,}")
        print(f"      • {peak_results['window_days']}-day Average: {peak['rolling_avg']:.2f}")
        print(f"      • Period: {peak['week_start']} to {peak['week_end']}")
    
    # Growth trends
    print(f"\n📈 GROWTH TREND ANALYSIS ({growth_results['period_days']}-day periods):")
    for period in growth_results['growth_analysis']:
        print(f"   {period['period']} ({period['start_date']} to {period['end_date']}):")
        print(f"      • Total Cases: {period['total_cases']:,}")
        print(f"      • Average Daily: {period['avg_daily_cases']:.2f}")
        print(f"      • Peak Daily: {period['max_daily_cases']:,}")

# Create the interactive dashboard
def create_dashboard():
    """Create and run the interactive COVID-19 dashboard with beautiful modern UI"""
    # Close any existing matplotlib figures to prevent empty windows
    plt.close('all')
    
    # Set DPI awareness for Windows to fix blurry fonts
    try:
        # For Windows 10/11
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        try:
            # For older Windows versions
            ctypes.windll.user32.SetProcessDPIAware()
        except:
            pass
    
    root = tk.Tk()
    root.title("🦠 COVID-19 Analysis Dashboard - Advanced Data Visualization")
    
    # Modern color scheme
    COLORS = {
        'primary': '#2E3440',      # Dark blue-gray
        'secondary': '#3B4252',    # Medium blue-gray
        'accent': '#5E81AC',       # Blue
        'success': '#A3BE8C',      # Green
        'warning': '#EBCB8B',      # Yellow
        'danger': '#BF616A',       # Red
        'text': '#ECEFF4',         # Light gray
        'text_secondary': '#D8DEE9', # Medium gray
        'background': '#1E1E1E',   # Very dark gray
        'surface': '#2D2D2D',      # Dark gray
        'border': '#4C566A'        # Medium gray
    }
    
    # Configure root window with modern styling
    root.configure(bg=COLORS['background'])
    root.geometry("1400x900")
    root.minsize(1200, 800)
    
    # Set window icon (if available)
    try:
        root.iconbitmap(default='icon.ico')
    except:
        pass
    
    # Modern window styling
    root.attributes('-alpha', 0.98)  # Slight transparency for modern look
    
    # Get screen dimensions and center window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 1400) // 2
    y = (screen_height - 900) // 2
    root.geometry(f"1400x900+{x}+{y}")
    
    # Make window resizable
    root.resizable(True, True)

    # Function to handle window resize and update plot sizes
    def on_window_resize(event):
        if event.widget == root:
            # Get new window size
            new_width = root.winfo_width()
            new_height = root.winfo_height()

            # Update plot figure sizes proportionally
            if hasattr(root, 'update_plot1'):
                try:
                    # Update figure sizes based on new window dimensions
                    fig1.set_size_inches(new_width * 0.3 / 100, new_height * 0.4 / 100)
                    fig2.set_size_inches(new_width * 0.3 / 100, new_height * 0.4 / 100)
                    fig3.set_size_inches(new_width * 0.3 / 100, new_height * 0.4 / 100)
                    fig_detail.set_size_inches(new_width * 0.6 / 100, new_height * 0.6 / 100)

                    # Redraw plots
                    update_plot1()
                    update_plot2()
                    update_plot3()
                    if 'update_detail_plot' in globals():
                        update_detail_plot()

                except Exception as e:
                    pass  # Ignore resize errors

    # Bind resize event (will be called after functions are defined)
    
    # Configure matplotlib for better DPI handling
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 100
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    plt.rcParams['legend.fontsize'] = 9
    
    # Bring window to front immediately
    try:
        root.update_idletasks()
        root.lift()
        root.attributes('-topmost', True)
        root.after(200, lambda: root.attributes('-topmost', False))
        root.focus_force()
    except Exception:
        pass

    # Prepare data
    peak_analysis = analyze_peak_infection_period(daily_summary, window_days=7, top_n=3)
    growth_analysis = analyze_growth_trends(daily_summary, periods=30)
    
    # Create modern header
    header_frame = tk.Frame(root, bg=COLORS['primary'], height=80)
    header_frame.pack(fill=tk.X, padx=0, pady=0)
    header_frame.pack_propagate(False)
    
    # Header content
    header_content = tk.Frame(header_frame, bg=COLORS['primary'])
    header_content.pack(expand=True, fill=tk.BOTH, padx=30, pady=15)
    
    # Title with icon
    title_frame = tk.Frame(header_content, bg=COLORS['primary'])
    title_frame.pack(side=tk.LEFT)
    
    title_label = tk.Label(title_frame, text="🦠 COVID-19 Analysis Dashboard", 
                          font=('Segoe UI', 24, 'bold'), 
                          fg=COLORS['text'], bg=COLORS['primary'])
    title_label.pack(anchor=tk.W)
    
    subtitle_label = tk.Label(title_frame, text="Advanced Data Visualization & Analytics", 
                             font=('Segoe UI', 12), 
                             fg=COLORS['text_secondary'], bg=COLORS['primary'])
    subtitle_label.pack(anchor=tk.W)
    
    # Stats summary in header
    stats_frame = tk.Frame(header_content, bg=COLORS['primary'])
    stats_frame.pack(side=tk.RIGHT)
    
    # Quick stats
    total_cases = daily_summary['Positive'].sum()
    max_daily = daily_summary['Positive'].max()
    date_range = f"{daily_summary.index.min().strftime('%Y-%m-%d')} to {daily_summary.index.max().strftime('%Y-%m-%d')}"
    
    stats_text = f"📊 Total Cases: {total_cases:,} | 🔥 Peak Daily: {max_daily:,} | 📅 Period: {date_range}"
    stats_label = tk.Label(stats_frame, text=stats_text, 
                          font=('Segoe UI', 11), 
                          fg=COLORS['text_secondary'], bg=COLORS['primary'])
    stats_label.pack(anchor=tk.E)
    
    # Create main interface with modern styling
    main_frame = tk.Frame(root, bg=COLORS['background'])
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Configure ttk styles for modern look
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure notebook style
    style.configure('TNotebook', background=COLORS['background'], borderwidth=0)
    style.configure('TNotebook.Tab', 
                   background=COLORS['secondary'], 
                   foreground=COLORS['text'],
                   padding=[20, 10],
                   font=('Segoe UI', 11, 'bold'))
    style.map('TNotebook.Tab', 
              background=[('selected', COLORS['accent']), ('active', COLORS['secondary'])],
              foreground=[('selected', COLORS['text']), ('active', COLORS['text'])])
    
    # Configure button styles
    style.configure('Modern.TButton',
                   background=COLORS['accent'],
                   foreground=COLORS['text'],
                   font=('Segoe UI', 10, 'bold'),
                   borderwidth=0,
                   focuscolor='none',
                   padding=[15, 8])
    style.map('Modern.TButton',
              background=[('active', COLORS['success']), ('pressed', COLORS['warning'])])
    
    style.configure('Secondary.TButton',
                   background=COLORS['secondary'],
                   foreground=COLORS['text'],
                   font=('Segoe UI', 10),
                   borderwidth=1,
                   focuscolor='none',
                   padding=[12, 6])
    style.map('Secondary.TButton',
              background=[('active', COLORS['accent']), ('pressed', COLORS['primary'])])
    
    # Create notebook for tabs
    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill=tk.BOTH, expand=True)
    
    # Tab 1: Overview with 3 plots
    overview_tab = tk.Frame(notebook, bg=COLORS['background'])
    notebook.add(overview_tab, text="📊 Overview")
    
    # Control panel for overview with modern styling
    control_frame = tk.Frame(overview_tab, bg=COLORS['surface'], relief=tk.RAISED, bd=1)
    control_frame.pack(fill=tk.X, padx=10, pady=10)
    
    # Control panel content
    control_content = tk.Frame(control_frame, bg=COLORS['surface'])
    control_content.pack(fill=tk.X, padx=15, pady=10)
    
    def show_summary():
        summary_text = f"""
COVID-19 INFECTION ANALYSIS SUMMARY
{'='*60}

📊 OVERALL STATISTICS:
   Date Range: {peak_analysis['overall_stats']['date_range']}
   Total Positive Cases: {peak_analysis['overall_stats']['total_positive_cases']:,}
   Maximum Daily Cases: {peak_analysis['overall_stats']['max_daily_cases']:,}
   Maximum 7-day Average: {peak_analysis['overall_stats']['max_rolling_avg']:.2f}

🏠 RESIDENTIAL BREAKDOWN:
   Residential Total Positive: {residential_daily['Positive'].sum():,}
   Non-Residential Total Positive: {non_residential_daily['Positive'].sum():,}
   Residential Max Daily: {residential_daily['Positive'].max():,}
   Non-Residential Max Daily: {non_residential_daily['Positive'].max():,}
"""
        messagebox.showinfo("Summary Statistics", summary_text)
    
    def show_seasonal_visualization():
        """Show seasonal patterns visualization in a new window"""
        fig_seasonal = plot_seasonal_patterns(daily_summary,
                                            "COVID-19 Seasonal Patterns Analysis")
        fig_seasonal.show()

    # Modern control buttons
    ttk.Button(control_content, text="📈 Summary Statistics", style='Modern.TButton',
              command=show_summary).pack(side=tk.LEFT, padx=5)
    ttk.Button(control_content, text="🌤️ Seasonal Patterns", style='Modern.TButton',
              command=show_seasonal_visualization).pack(side=tk.LEFT, padx=5)
    ttk.Button(control_content, text="🔄 Refresh Plots", style='Secondary.TButton',
              command=lambda: refresh_plots()).pack(side=tk.LEFT, padx=5)
    
    # Add export button
    def export_data():
        """Export analysis data to CSV"""
        try:
            from tkinter import filedialog
            import datetime
            
            # Generate default filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"covid_analysis_{timestamp}.csv"
            
            # Ask user for save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=default_filename,
                title="Export COVID-19 Analysis Data"
            )
            
            if file_path:
                # Export daily summary data
                daily_summary.to_csv(file_path)
                messagebox.showinfo("Export Successful", 
                                   f"Data exported successfully!\n\nFile: {file_path}")
                print(f"Data exported: {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data:\n\n{str(e)}")
    
    ttk.Button(control_content, text="💾 Export Data", style='Secondary.TButton',
              command=export_data).pack(side=tk.RIGHT, padx=5)
    
    # Create scrollable frame for plots with modern styling
    canvas_overview = tk.Canvas(overview_tab, bg=COLORS['background'], highlightthickness=0)
    v_scrollbar_overview = ttk.Scrollbar(overview_tab, orient="vertical", command=canvas_overview.yview)
    h_scrollbar_overview = ttk.Scrollbar(overview_tab, orient="horizontal", command=canvas_overview.xview)
    scrollable_frame_overview = tk.Frame(canvas_overview, bg=COLORS['background'])
    
    scrollable_frame_overview.bind(
        "<Configure>",
        lambda e: canvas_overview.configure(scrollregion=canvas_overview.bbox("all"))
    )
    
    canvas_overview.create_window((0, 0), window=scrollable_frame_overview, anchor="nw")
    canvas_overview.configure(yscrollcommand=v_scrollbar_overview.set, xscrollcommand=h_scrollbar_overview.set)
    
    # Pack scrollable area
    canvas_overview.pack(side="left", fill="both", expand=True)
    v_scrollbar_overview.pack(side="right", fill="y")
    h_scrollbar_overview.pack(side="bottom", fill="x")
    
    # Create 3 plot frames stacked vertically with modern styling
    plots_frame = tk.Frame(scrollable_frame_overview, bg=COLORS['background'])
    plots_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    # Plot 1: Cumulative Cases with modern styling
    plot1_container = tk.Frame(plots_frame, bg=COLORS['surface'], relief=tk.RAISED, bd=2)
    plot1_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Plot 1 header
    plot1_header = tk.Frame(plot1_container, bg=COLORS['accent'], height=50)
    plot1_header.pack(fill=tk.X)
    plot1_header.pack_propagate(False)
    
    plot1_title = tk.Label(plot1_header, text="📈 Cumulative Positive Cases", 
                          font=('Segoe UI', 14, 'bold'), 
                          fg=COLORS['text'], bg=COLORS['accent'])
    plot1_title.pack(side=tk.LEFT, padx=15, pady=12)
    
    # Time mode buttons for Plot 1 with modern styling
    plot1_control_frame = tk.Frame(plot1_container, bg=COLORS['surface'])
    plot1_control_frame.pack(fill=tk.X, padx=10, pady=8)

    plot1_mode = tk.StringVar(value="daily")
    
    # Modern radio buttons
    radio_frame = tk.Frame(plot1_control_frame, bg=COLORS['surface'])
    radio_frame.pack(side=tk.LEFT)
    
    ttk.Radiobutton(radio_frame, text="📅 Daily", variable=plot1_mode, value="daily",
                   command=lambda: update_plot1()).pack(side=tk.LEFT, padx=5)
    ttk.Radiobutton(radio_frame, text="📊 Weekly", variable=plot1_mode, value="weekly",
                   command=lambda: update_plot1()).pack(side=tk.LEFT, padx=5)
    ttk.Radiobutton(radio_frame, text="📈 Monthly", variable=plot1_mode, value="monthly",
                   command=lambda: update_plot1()).pack(side=tk.LEFT, padx=5)

    # Save button for Plot 1
    ttk.Button(plot1_control_frame, text="💾 Save PNG", style='Secondary.TButton',
              command=lambda: save_plot_png(fig1, "cumulative_cases")).pack(side=tk.RIGHT, padx=5)
    
    # Plot 1 content area
    plot1_content = tk.Frame(plot1_container, bg=COLORS['surface'])
    plot1_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Configure matplotlib for modern dark theme
    plt.style.use('dark_background')
    fig1 = Figure(figsize=(14, 6), dpi=100, facecolor=COLORS['surface'])
    fig1.patch.set_facecolor(COLORS['surface'])
    
    canvas1 = FigureCanvasTkAgg(fig1, plot1_content)
    canvas1.get_tk_widget().configure(bg=COLORS['surface'])
    canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Plot 2: Daily Cases with modern styling
    plot2_container = tk.Frame(plots_frame, bg=COLORS['surface'], relief=tk.RAISED, bd=2)
    plot2_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Plot 2 header
    plot2_header = tk.Frame(plot2_container, bg=COLORS['success'], height=50)
    plot2_header.pack(fill=tk.X)
    plot2_header.pack_propagate(False)
    
    plot2_title = tk.Label(plot2_header, text="📊 Cases Trend Analysis", 
                          font=('Segoe UI', 14, 'bold'), 
                          fg=COLORS['text'], bg=COLORS['success'])
    plot2_title.pack(side=tk.LEFT, padx=15, pady=12)
    
    # Time mode buttons for Plot 2 with modern styling
    plot2_control_frame = tk.Frame(plot2_container, bg=COLORS['surface'])
    plot2_control_frame.pack(fill=tk.X, padx=10, pady=8)

    plot2_mode = tk.StringVar(value="daily")
    
    # Modern radio buttons
    radio_frame2 = tk.Frame(plot2_control_frame, bg=COLORS['surface'])
    radio_frame2.pack(side=tk.LEFT)
    
    ttk.Radiobutton(radio_frame2, text="📅 Daily", variable=plot2_mode, value="daily",
                   command=lambda: update_plot2()).pack(side=tk.LEFT, padx=5)
    ttk.Radiobutton(radio_frame2, text="📊 Weekly", variable=plot2_mode, value="weekly",
                   command=lambda: update_plot2()).pack(side=tk.LEFT, padx=5)
    ttk.Radiobutton(radio_frame2, text="📈 Monthly", variable=plot2_mode, value="monthly",
                   command=lambda: update_plot2()).pack(side=tk.LEFT, padx=5)

    # Save button for Plot 2
    ttk.Button(plot2_control_frame, text="💾 Save PNG", style='Secondary.TButton',
              command=lambda: save_plot_png(fig2, "cases_trend")).pack(side=tk.RIGHT, padx=5)
    
    # Plot 2 content area
    plot2_content = tk.Frame(plot2_container, bg=COLORS['surface'])
    plot2_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    fig2 = Figure(figsize=(14, 6), dpi=100, facecolor=COLORS['surface'])
    fig2.patch.set_facecolor(COLORS['surface'])
    
    canvas2 = FigureCanvasTkAgg(fig2, plot2_content)
    canvas2.get_tk_widget().configure(bg=COLORS['surface'])
    canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Plot 3: Residential Comparison with modern styling
    plot3_container = tk.Frame(plots_frame, bg=COLORS['surface'], relief=tk.RAISED, bd=2)
    plot3_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Plot 3 header
    plot3_header = tk.Frame(plot3_container, bg=COLORS['warning'], height=50)
    plot3_header.pack(fill=tk.X)
    plot3_header.pack_propagate(False)
    
    plot3_title = tk.Label(plot3_header, text="🏠 Residential vs Non-Residential Analysis", 
                          font=('Segoe UI', 14, 'bold'), 
                          fg=COLORS['primary'], bg=COLORS['warning'])
    plot3_title.pack(side=tk.LEFT, padx=15, pady=12)
    
    # Time mode buttons for Plot 3 with modern styling
    plot3_control_frame = tk.Frame(plot3_container, bg=COLORS['surface'])
    plot3_control_frame.pack(fill=tk.X, padx=10, pady=8)

    plot3_mode = tk.StringVar(value="daily")
    
    # Modern radio buttons
    radio_frame3 = tk.Frame(plot3_control_frame, bg=COLORS['surface'])
    radio_frame3.pack(side=tk.LEFT)
    
    ttk.Radiobutton(radio_frame3, text="📅 Daily", variable=plot3_mode, value="daily",
                   command=lambda: update_plot3()).pack(side=tk.LEFT, padx=5)
    ttk.Radiobutton(radio_frame3, text="📊 Weekly", variable=plot3_mode, value="weekly",
                   command=lambda: update_plot3()).pack(side=tk.LEFT, padx=5)
    ttk.Radiobutton(radio_frame3, text="📈 Monthly", variable=plot3_mode, value="monthly",
                   command=lambda: update_plot3()).pack(side=tk.LEFT, padx=5)

    # Save button for Plot 3
    ttk.Button(plot3_control_frame, text="💾 Save PNG", style='Secondary.TButton',
              command=lambda: save_plot_png(fig3, "residential_comparison")).pack(side=tk.RIGHT, padx=5)
    
    # Plot 3 content area
    plot3_content = tk.Frame(plot3_container, bg=COLORS['surface'])
    plot3_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    fig3 = Figure(figsize=(14, 6), dpi=100, facecolor=COLORS['surface'])
    fig3.patch.set_facecolor(COLORS['surface'])
    
    canvas3 = FigureCanvasTkAgg(fig3, plot3_content)
    canvas3.get_tk_widget().configure(bg=COLORS['surface'])
    canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Bind mousewheel and touchpad scrolling to canvas
    def _on_mousewheel_overview(event):
        # Handle different platforms and input methods
        if event.delta:
            # Windows mouse wheel
            canvas_overview.yview_scroll(int(-1*(event.delta/120)), "units")
        elif event.num == 4:
            # Linux mouse wheel up
            canvas_overview.yview_scroll(-1, "units")
        elif event.num == 5:
            # Linux mouse wheel down
            canvas_overview.yview_scroll(1, "units")
    
    def _on_mousewheel_overview_shift(event):
        # Horizontal scrolling with Shift+wheel
        if event.delta:
            canvas_overview.xview_scroll(int(-1*(event.delta/120)), "units")
        elif event.num == 4:
            canvas_overview.xview_scroll(-1, "units")
        elif event.num == 5:
            canvas_overview.xview_scroll(1, "units")
    
    # Bind scroll events to the canvas itself (not bind_all) so it works when cursor is over the canvas
    canvas_overview.bind("<MouseWheel>", _on_mousewheel_overview)  # Windows
    canvas_overview.bind("<Button-4>", _on_mousewheel_overview)    # Linux scroll up
    canvas_overview.bind("<Button-5>", _on_mousewheel_overview)    # Linux scroll down
    canvas_overview.bind("<Shift-MouseWheel>", _on_mousewheel_overview_shift)  # Horizontal scroll
    
    # Touchpad support (works on most systems)
    canvas_overview.bind("<Control-MouseWheel>", _on_mousewheel_overview)  # Touchpad alternative
    
    # Also bind to the scrollable frame for better coverage
    scrollable_frame_overview.bind("<MouseWheel>", _on_mousewheel_overview)
    scrollable_frame_overview.bind("<Button-4>", _on_mousewheel_overview)
    scrollable_frame_overview.bind("<Button-5>", _on_mousewheel_overview)
    scrollable_frame_overview.bind("<Shift-MouseWheel>", _on_mousewheel_overview_shift)
    scrollable_frame_overview.bind("<Control-MouseWheel>", _on_mousewheel_overview)
    
    # Bind to the plots frame as well
    plots_frame.bind("<MouseWheel>", _on_mousewheel_overview)
    plots_frame.bind("<Button-4>", _on_mousewheel_overview)
    plots_frame.bind("<Button-5>", _on_mousewheel_overview)
    plots_frame.bind("<Shift-MouseWheel>", _on_mousewheel_overview_shift)
    plots_frame.bind("<Control-MouseWheel>", _on_mousewheel_overview)
    
    # Bind scroll events to matplotlib canvas widgets (this is the key fix)
    def bind_matplotlib_canvas(canvas_widget):
        canvas_widget.bind("<MouseWheel>", _on_mousewheel_overview)
        canvas_widget.bind("<Button-4>", _on_mousewheel_overview)
        canvas_widget.bind("<Button-5>", _on_mousewheel_overview)
        canvas_widget.bind("<Shift-MouseWheel>", _on_mousewheel_overview_shift)
        canvas_widget.bind("<Control-MouseWheel>", _on_mousewheel_overview)
    
    # Bind to all matplotlib canvas widgets
    bind_matplotlib_canvas(canvas1.get_tk_widget())
    bind_matplotlib_canvas(canvas2.get_tk_widget())
    bind_matplotlib_canvas(canvas3.get_tk_widget())

    # Function to save plots as PNG
    def save_plot_png(figure, plot_name):
        """Save a matplotlib figure as PNG file"""
        from tkinter import filedialog
        import datetime

        # Generate default filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"{plot_name}_{timestamp}.png"

        # Ask user for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile=default_filename,
            title=f"Save {plot_name.replace('_', ' ').title()} Plot"
        )

        if file_path:
            try:
                # Save the figure with high DPI for quality
                figure.savefig(file_path, dpi=300, bbox_inches='tight',
                              facecolor='white', edgecolor='none')
                messagebox.showinfo("Success",
                                   f"Plot saved successfully!\n\nFile: {file_path}")
                print(f"Plot saved: {file_path}")
            except Exception as e:
                messagebox.showerror("Error",
                                   f"Failed to save plot:\n\n{str(e)}")
                print(f"Error saving plot: {e}")

    def update_plot1():
        fig1.clear()
        ax = fig1.add_subplot(111)
        
        # Get data based on selected mode
        mode = plot1_mode.get()
        if mode == "daily":
            data = daily_summary
            title_suffix = "Daily"
            xlabel_suffix = "Daily"
            interval = 30
        elif mode == "weekly":
            data = daily_summary_weekly
            title_suffix = "Weekly"
            xlabel_suffix = "Weekly"
            interval = 7
        else:  # monthly
            data = daily_summary_monthly
            title_suffix = "Monthly"
            xlabel_suffix = "Monthly"
            interval = 30
        
        ax.plot(data.index, data['Cumulative_Positive'], 
                label=f'Cumulative Positive Cases ({title_suffix})', marker='o', markersize=5, linewidth=2)
        ax.set_title(f'Cumulative COVID-19 Positive Cases Over Time ({title_suffix})')
        ax.set_xlabel(f'Date ({xlabel_suffix})')
        ax.set_ylabel('Cumulative Number of Positive Cases')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Set x-axis ticks based on mode
        import matplotlib.dates as mdates
        if mode == "daily":
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=interval))
        else:
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=interval))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        
        # Rotate x-axis labels for better readability
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        fig1.tight_layout()
        canvas1.draw()
    
    def update_plot2():
        fig2.clear()
        ax = fig2.add_subplot(111)
        
        # Get data based on selected mode
        mode = plot2_mode.get()
        if mode == "daily":
            data_all = daily_summary
            data_students = students_daily
            data_faculty = faculty_staff_daily
            title_suffix = "Daily"
            xlabel_suffix = "Daily"
            interval = 30
        elif mode == "weekly":
            data_all = daily_summary_weekly
            data_students = students_daily_weekly
            data_faculty = faculty_staff_daily_weekly
            title_suffix = "Weekly"
            xlabel_suffix = "Weekly"
            interval = 7
        else:  # monthly
            data_all = daily_summary_monthly
            data_students = students_daily_monthly
            data_faculty = faculty_staff_daily_monthly
            title_suffix = "Monthly"
            xlabel_suffix = "Monthly"
            interval = 30
        
        # Plot overall (faint) and split by Students vs Faculty/Staff
        ax.plot(data_all.index, data_all['Positive'], 
                label=f'All Positive ({title_suffix})', color='gray', alpha=0.4, linewidth=1)
        ax.plot(data_students.index, data_students['Positive'], 
                label=f'Students Positive ({title_suffix})', color='#1f77b4', alpha=0.9, marker='o', markersize=5)
        ax.plot(data_faculty.index, data_faculty['Positive'], 
                label=f'Faculty/Staff Positive ({title_suffix})', color='#d62728', alpha=0.9, marker='s', markersize=5)
        
        # Removed "All Negative" line to prevent scale issues and focus on positive cases
        # ax.plot(data_all.index, data_all['Negative'],
        #         label=f'All Negative ({title_suffix})', color='black', alpha=0.3, linestyle='--', linewidth=1)
        ax.set_title(f'COVID-19 Test Results ({title_suffix})')
        ax.set_xlabel(f'Date ({xlabel_suffix})')
        ax.set_ylabel(f'Number of Positive Cases ({title_suffix})')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Set x-axis ticks based on mode
        import matplotlib.dates as mdates
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=interval))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        
        # Rotate x-axis labels for better readability
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        fig2.tight_layout()
        canvas2.draw()
    
    def update_plot3():
        fig3.clear()
        ax = fig3.add_subplot(111)
        
        # Get data based on selected mode
        mode = plot3_mode.get()
        if mode == "daily":
            res_data = residential_daily
            non_res_data = non_residential_daily
            title_suffix = "Daily"
            xlabel_suffix = "Daily"
            interval = 30
        elif mode == "weekly":
            res_data = residential_daily_weekly
            non_res_data = non_residential_daily_weekly
            title_suffix = "Weekly"
            xlabel_suffix = "Weekly"
            interval = 7
        else:  # monthly
            res_data = residential_daily_monthly
            non_res_data = non_residential_daily_monthly
            title_suffix = "Monthly"
            xlabel_suffix = "Monthly"
            interval = 30
        
        # Plot both datasets
        ax.plot(res_data.index, res_data['Positive'], 
                label=f'Residential ({title_suffix})', color='blue', alpha=0.8, marker='o', markersize=6, linewidth=2)
        ax.plot(non_res_data.index, non_res_data['Positive'], 
                label=f'Non-Residential ({title_suffix})', color='red', alpha=0.8, marker='s', markersize=6, linewidth=2)
        
        # Set title and labels
        ax.set_title(f'Positive Cases: Residential vs Non-Residential ({title_suffix})')
        ax.set_xlabel(f'Date ({xlabel_suffix})')
        ax.set_ylabel(f'Number of Positive Cases ({title_suffix})')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Set x-axis ticks based on mode
        import matplotlib.dates as mdates
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=interval))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        
        # Rotate x-axis labels for better readability
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Add data statistics as text
        res_total = res_data['Positive'].sum()
        non_res_total = non_res_data['Positive'].sum()
        res_max = res_data['Positive'].max()
        non_res_max = non_res_data['Positive'].max()
        
        stats_text = f'Residential Total: {res_total:,} | Non-Residential Total: {non_res_total:,}\nResidential Max: {res_max:,} | Non-Residential Max: {non_res_max:,}'
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=9,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
        
        fig3.tight_layout()
        canvas3.draw()
    
    def refresh_plots():
        update_plot1()
        update_plot2()
        update_plot3()
        messagebox.showinfo("Refresh Complete", "All plots have been refreshed!")
    
    # Tab 2: Detailed Analysis with modern styling
    detail_tab = tk.Frame(notebook, bg=COLORS['background'])
    notebook.add(detail_tab, text="🔍 Detailed Analysis")
    
    # Control panel for detailed analysis with modern styling
    detail_control = tk.Frame(detail_tab, bg=COLORS['surface'], relief=tk.RAISED, bd=1)
    detail_control.pack(fill=tk.X, padx=10, pady=10)
    
    # Control panel content
    detail_control_content = tk.Frame(detail_control, bg=COLORS['surface'])
    detail_control_content.pack(fill=tk.X, padx=15, pady=10)
    
    def show_peak_details():
        peak_text = f"""
PEAK INFECTION ANALYSIS
{'='*40}

TOP 3 PEAK PERIODS:
"""
        for peak in peak_analysis['peak_periods']:
            peak_text += f"""
Peak {peak['rank']}: {peak['date']}
   Daily Cases: {peak['daily_cases']:,}
   7-day Average: {peak['rolling_avg']:.2f}
   Period: {peak['week_start']} to {peak['week_end']}
"""
        messagebox.showinfo("Peak Analysis Details", peak_text)
    
    def show_residential_details():
        res_text = f"""
RESIDENTIAL ANALYSIS
{'='*30}

RESIDENTIAL:
   Total Positive: {residential_daily['Positive'].sum():,}
   Max Daily: {residential_daily['Positive'].max():,}
   Average Daily: {residential_daily['Positive'].mean():.2f}

NON-RESIDENTIAL:
   Total Positive: {non_residential_daily['Positive'].sum():,}
   Max Daily: {non_residential_daily['Positive'].max():,}
   Average Daily: {non_residential_daily['Positive'].mean():.2f}

RATIO: {(residential_daily['Positive'].sum() / non_residential_daily['Positive'].sum()):.2f}
"""
        messagebox.showinfo("Residential Analysis Details", res_text)
    
    def show_seasonal_analysis():
        """Show seasonal analysis results in a message box"""
        # Analyze seasonal patterns for different data types
        residential_seasonal = analyze_seasonal_patterns(residential_daily)
        non_residential_seasonal = analyze_seasonal_patterns(non_residential_daily)
        overall_seasonal = analyze_seasonal_patterns(daily_summary)

        seasonal_text = "🌤️ COVID-19 Seasonal Pattern Analysis\n\n"

        # Overall seasonal insights
        if overall_seasonal['seasonal_insights']:
            insights = overall_seasonal['seasonal_insights']
            seasonal_text += f"📊 OVERALL SEASONAL INSIGHTS:\n"
            seasonal_text += f"Peak Season: {insights['peak_season']['season']} "
            seasonal_text += f"({insights['peak_season']['total_cases']:,} cases, "
            seasonal_text += f"{insights['peak_season']['avg_daily']:.1f} avg daily)\n"
            seasonal_text += f"Low Season: {insights['low_season']['season']} "
            seasonal_text += f"({insights['low_season']['total_cases']:,} cases, "
            seasonal_text += f"{insights['low_season']['avg_daily']:.1f} avg daily)\n"
            seasonal_text += f"Seasonal Variation: {insights['seasonal_variation']}%\n\n"

        # Seasonal breakdown
        seasonal_text += "📈 SEASONAL BREAKDOWN:\n"
        for season, stats in overall_seasonal['seasonal_analysis'].items():
            seasonal_text += f"{season}: {stats['total_cases']:,} total cases "
            seasonal_text += f"({stats['avg_daily_cases']:.1f} avg daily)\n"
        seasonal_text += "\n"

        # Monthly peaks
        if overall_seasonal['monthly_analysis']:
            monthly_sorted = sorted(overall_seasonal['monthly_analysis'],
                                  key=lambda x: x['total_cases'], reverse=True)
            seasonal_text += "📅 TOP MONTHS BY CASES:\n"
            for i, month in enumerate(monthly_sorted[:3], 1):
                seasonal_text += f"{i}. {month['month']}: {month['total_cases']:,} cases "
                seasonal_text += f"({month['avg_daily_cases']:.1f} avg daily)\n"

        messagebox.showinfo("Seasonal Analysis", seasonal_text)

    def show_seasonal_analysis_visual():
        """Show seasonal analysis with comprehensive visualizations in a new window"""
        import matplotlib.pyplot as plt
        import calendar
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import tkinter as tk
        from tkinter import ttk

        # Create new window for seasonal analysis
        seasonal_window = tk.Toplevel(root)
        seasonal_window.title("🌤️ Seasonal Analysis Dashboard")
        seasonal_window.geometry("1400x900")
        seasonal_window.configure(bg='#f0f0f0')

        # Analyze seasonal patterns
        overall_seasonal = analyze_seasonal_patterns(daily_summary)
        residential_seasonal = analyze_seasonal_patterns(residential_daily)
        non_residential_seasonal = analyze_seasonal_patterns(non_residential_daily)

        # Create main frame with scrollbar
        main_frame = ttk.Frame(seasonal_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(main_frame, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # Title
        title_label = ttk.Label(scrollable_frame, text="🌤️ COVID-19 Seasonal Pattern Analysis",
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Create figure 1: Monthly Distribution
        fig1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig1.suptitle('Monthly Case Distribution Analysis', fontsize=14, fontweight='bold')

        # Monthly totals
        monthly_data = daily_summary.groupby(daily_summary.index.month)['Positive'].sum()
        months_full = [calendar.month_name[i] for i in range(1, 13)]
        bars = ax1.bar(range(1, 13), monthly_data.values, color='skyblue', alpha=0.7)
        ax1.set_title('Total Cases by Month')
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Total Cases')
        ax1.set_xticks(range(1, 13))
        ax1.set_xticklabels([calendar.month_abbr[i] for i in range(1, 13)], rotation=45)

        # Add value labels on bars
        for bar, value in zip(bars, monthly_data.values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(monthly_data.values)*0.01,
                    f'{value:,}', ha='center', va='bottom', fontsize=8, fontweight='bold')

        # Seasonal breakdown
        seasons = {'Winter': [12, 1, 2], 'Spring': [3, 4, 5], 'Summer': [6, 7, 8], 'Fall': [9, 10, 11]}
        seasonal_totals = {}
        for season_name, season_months in seasons.items():
            season_data = daily_summary[daily_summary.index.month.isin(season_months)]
            seasonal_totals[season_name] = season_data['Positive'].sum()

        colors = ['lightblue', 'lightgreen', 'orange', 'lightcoral']
        season_bars = ax2.bar(seasonal_totals.keys(), seasonal_totals.values(), color=colors, alpha=0.8)
        ax2.set_title('Cases by Season')
        ax2.set_xlabel('Season')
        ax2.set_ylabel('Total Cases')

        # Add value labels
        for bar, (season, value) in zip(season_bars, seasonal_totals.items()):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(seasonal_totals.values())*0.02,
                    f'{value:,}', ha='center', va='bottom', fontsize=9, fontweight='bold')

        # Monthly averages
        monthly_avg = daily_summary.groupby(daily_summary.index.month)['Positive'].mean()
        ax3.plot(range(1, 13), monthly_avg.values, 'o-', color='darkblue', linewidth=2, markersize=6)
        ax3.fill_between(range(1, 13), monthly_avg.values, alpha=0.3, color='lightblue')
        ax3.set_title('Average Daily Cases by Month')
        ax3.set_xlabel('Month')
        ax3.set_ylabel('Average Daily Cases')
        ax3.set_xticks(range(1, 13))
        ax3.set_xticklabels([calendar.month_abbr[i] for i in range(1, 13)], rotation=45)
        ax3.grid(True, alpha=0.3)

        # Peak vs Low season comparison
        if overall_seasonal['seasonal_insights']:
            insights = overall_seasonal['seasonal_insights']
            peak_season = insights['peak_season']['season']
            low_season = insights['low_season']['season']
            peak_cases = insights['peak_season']['total_cases']
            low_cases = insights['low_season']['total_cases']

            ax4.bar(['Peak Season', 'Low Season'], [peak_cases, low_cases],
                   color=['red', 'green'], alpha=0.7)
            ax4.set_title(f'Peak vs Low Season\n({peak_season} vs {low_season})')
            ax4.set_ylabel('Total Cases')

            # Add percentage difference
            pct_diff = insights['seasonal_variation']
            ax4.text(0.5, max(peak_cases, low_cases) * 0.9,
                    f'Seasonal Variation: {pct_diff:.1f}%',
                    ha='center', va='center', fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

        plt.tight_layout()

        # Create canvas for figure 1
        canvas1 = FigureCanvasTkAgg(fig1, master=scrollable_frame)
        canvas1.get_tk_widget().pack(pady=10)
        canvas1.draw()

        # Create figure 2: Residential vs Non-Residential Seasonal Comparison
        fig2, ((ax5, ax6), (ax7, ax8)) = plt.subplots(2, 2, figsize=(12, 8))
        fig2.suptitle('Residential vs Non-Residential Seasonal Patterns', fontsize=14, fontweight='bold')

        # Residential monthly
        res_monthly = residential_daily.groupby(residential_daily.index.month)['Positive'].sum()
        ax5.bar(range(1, 13), res_monthly.values, color='blue', alpha=0.7, label='Residential')
        ax5.set_title('Residential Cases by Month')
        ax5.set_xlabel('Month')
        ax5.set_ylabel('Total Cases')
        ax5.set_xticks(range(1, 13))
        ax5.set_xticklabels([calendar.month_abbr[i] for i in range(1, 13)], rotation=45)

        # Non-residential monthly
        non_res_monthly = non_residential_daily.groupby(non_residential_daily.index.month)['Positive'].sum()
        ax6.bar(range(1, 13), non_res_monthly.values, color='red', alpha=0.7, label='Non-Residential')
        ax6.set_title('Non-Residential Cases by Month')
        ax6.set_xlabel('Month')
        ax6.set_ylabel('Total Cases')
        ax6.set_xticks(range(1, 13))
        ax6.set_xticklabels([calendar.month_abbr[i] for i in range(1, 13)], rotation=45)

        # Seasonal comparison
        res_seasonal = {}
        non_res_seasonal = {}

        for season_name, season_months in seasons.items():
            res_data = residential_daily[residential_daily.index.month.isin(season_months)]
            non_res_data = non_residential_daily[non_residential_daily.index.month.isin(season_months)]
            res_seasonal[season_name] = res_data['Positive'].sum()
            non_res_seasonal[season_name] = non_res_data['Positive'].sum()

        x = range(len(seasons))
        width = 0.35
        ax7.bar([i - width/2 for i in x], list(res_seasonal.values()), width, color='blue', alpha=0.7, label='Residential')
        ax7.bar([i + width/2 for i in x], list(non_res_seasonal.values()), width, color='red', alpha=0.7, label='Non-Residential')
        ax7.set_title('Seasonal Comparison: Residential vs Non-Residential')
        ax7.set_xlabel('Season')
        ax7.set_ylabel('Total Cases')
        ax7.set_xticks(x)
        ax7.set_xticklabels(list(seasons.keys()))
        ax7.legend()

        # Monthly ratio
        ratios = []
        for month in range(1, 13):
            res_cases = res_monthly.get(month, 0)
            non_res_cases = non_res_monthly.get(month, 0)
            ratio = res_cases / non_res_cases if non_res_cases > 0 else 0
            ratios.append(ratio)

        ax8.plot(range(1, 13), ratios, 'o-', color='purple', linewidth=2, markersize=6)
        ax8.fill_between(range(1, 13), ratios, alpha=0.3, color='violet')
        ax8.set_title('Monthly Residential/Non-Residential Ratio')
        ax8.set_xlabel('Month')
        ax8.set_ylabel('Ratio (Residential : Non-Residential)')
        ax8.set_xticks(range(1, 13))
        ax8.set_xticklabels([calendar.month_abbr[i] for i in range(1, 13)], rotation=45)
        ax8.grid(True, alpha=0.3)

        # Add horizontal line at ratio = 1
        ax8.axhline(y=1, color='black', linestyle='--', alpha=0.5, label='Equal Ratio')
        ax8.legend()

        plt.tight_layout()

        # Create canvas for figure 2
        canvas2 = FigureCanvasTkAgg(fig2, master=scrollable_frame)
        canvas2.get_tk_widget().pack(pady=10)
        canvas2.draw()

        # Summary statistics section
        stats_frame = ttk.LabelFrame(scrollable_frame, text="📊 Seasonal Analysis Summary", padding=10)
        stats_frame.pack(fill=tk.X, pady=10)

        # Create text widget for summary
        summary_text = tk.Text(stats_frame, height=12, wrap=tk.WORD, font=("Consolas", 10))
        summary_scrollbar = ttk.Scrollbar(stats_frame, orient="vertical", command=summary_text.yview)
        summary_text.configure(yscrollcommand=summary_scrollbar.set)

        # Generate summary
        summary_content = "🌤️ COVID-19 SEASONAL ANALYSIS SUMMARY\n"
        summary_content += "=" * 50 + "\n\n"

        if overall_seasonal['seasonal_insights']:
            insights = overall_seasonal['seasonal_insights']
            summary_content += "📈 OVERALL SEASONAL INSIGHTS:\n"
            summary_content += f"• Peak Season: {insights['peak_season']['season']}\n"
            summary_content += f"  - Total Cases: {insights['peak_season']['total_cases']:,}\n"
            summary_content += f"  - Avg Daily: {insights['peak_season']['avg_daily']:.1f}\n\n"
            summary_content += f"• Low Season: {insights['low_season']['season']}\n"
            summary_content += f"  - Total Cases: {insights['low_season']['total_cases']:,}\n"
            summary_content += f"  - Avg Daily: {insights['low_season']['avg_daily']:.1f}\n\n"
            summary_content += f"• Seasonal Variation: {insights['seasonal_variation']:.1f}%\n\n"

        # Monthly peaks
        if overall_seasonal['monthly_analysis']:
            monthly_sorted = sorted(overall_seasonal['monthly_analysis'],
                                  key=lambda x: x['total_cases'], reverse=True)
            summary_content += "📅 TOP 3 MONTHS BY TOTAL CASES:\n"
            for i, month in enumerate(monthly_sorted[:3], 1):
                summary_content += f"{i}. {month['month']}: {month['total_cases']:,} cases "
                summary_content += f"({month['avg_daily_cases']:.1f} avg daily)\n"
            summary_content += "\n"

        # Residential vs Non-Residential insights
        res_total = residential_daily['Positive'].sum()
        non_res_total = non_residential_daily['Positive'].sum()
        ratio = res_total / non_res_total if non_res_total > 0 else 0

        summary_content += "🏠 RESIDENTIAL VS NON-RESIDENTIAL:\n"
        summary_content += f"• Residential Total: {res_total:,} cases\n"
        summary_content += f"• Non-Residential Total: {non_res_total:,} cases\n"
        summary_content += f"• Ratio: {ratio:.2f} (Residential : Non-Residential)\n\n"

        # Seasonal patterns
        summary_content += "🌿 SEASONAL PATTERNS:\n"
        for season in ['Winter', 'Spring', 'Summer', 'Fall']:
            if season in res_seasonal and season in non_res_seasonal:
                res_cases = res_seasonal[season]
                non_res_cases = non_res_seasonal[season]
                season_ratio = res_cases / non_res_cases if non_res_cases > 0 else 0
                summary_content += f"• {season}: Res={res_cases:,} | Non-Res={non_res_cases:,} | Ratio={season_ratio:.2f}\n"

        summary_text.insert(tk.END, summary_content)
        summary_text.config(state=tk.DISABLED)

        summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Close button
        close_button = ttk.Button(scrollable_frame, text="Close Seasonal Analysis",
                                 command=seasonal_window.destroy)
        close_button.pack(pady=10)

        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)

        # Force window to front
        seasonal_window.update_idletasks()
        seasonal_window.lift()
        seasonal_window.focus_force()

    # Create scrollable frame for detailed plot
    canvas_detail = tk.Canvas(detail_tab)
    scrollbar_detail = ttk.Scrollbar(detail_tab, orient="vertical", command=canvas_detail.yview)
    scrollable_frame_detail = ttk.Frame(canvas_detail)

    scrollable_frame_detail.bind(
        "<Configure>",
        lambda e: canvas_detail.configure(scrollregion=canvas_detail.bbox("all"))
    )

    canvas_detail.create_window((0, 0), window=scrollable_frame_detail, anchor="nw")
    canvas_detail.configure(yscrollcommand=scrollbar_detail.set)

    # Pack scrollable area
    canvas_detail.pack(side="left", fill="both", expand=True)
    scrollbar_detail.pack(side="right", fill="y")

    # Detailed plot area
    detail_plot_frame = ttk.Frame(scrollable_frame_detail)
    detail_plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    fig_detail = Figure(figsize=(18, 12), dpi=100)
    canvas_detail_plot = FigureCanvasTkAgg(fig_detail, detail_plot_frame)
    canvas_detail_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Bind mousewheel and touchpad scrolling to canvas
    def _on_mousewheel_detail(event):
        # Handle different platforms and input methods
        if event.delta:
            # Windows mouse wheel
            canvas_detail.yview_scroll(int(-1*(event.delta/120)), "units")
        elif event.num == 4:
            # Linux mouse wheel up
            canvas_detail.yview_scroll(-1, "units")
        elif event.num == 5:
            # Linux mouse wheel down
            canvas_detail.yview_scroll(1, "units")

    def _on_mousewheel_detail_shift(event):
        # Horizontal scrolling with Shift+wheel
        if event.delta:
            canvas_detail.xview_scroll(int(-1*(event.delta/120)), "units")

    # Bind scroll events to the canvas itself (not bind_all) so it works when cursor is over the canvas
    canvas_detail.bind("<MouseWheel>", _on_mousewheel_detail)  # Windows
    canvas_detail.bind("<Button-4>", _on_mousewheel_detail)    # Linux scroll up
    canvas_detail.bind("<Button-5>", _on_mousewheel_detail)    # Linux scroll down
    canvas_detail.bind("<Shift-MouseWheel>", _on_mousewheel_detail_shift)  # Horizontal scroll

    # Touchpad support (works on most systems)
    canvas_detail.bind("<Control-MouseWheel>", _on_mousewheel_detail)  # Touchpad alternative

    # Also bind to the scrollable frame for better coverage
    scrollable_frame_detail.bind("<MouseWheel>", _on_mousewheel_detail)
    scrollable_frame_detail.bind("<Button-4>", _on_mousewheel_detail)
    scrollable_frame_detail.bind("<Button-5>", _on_mousewheel_detail)
    scrollable_frame_detail.bind("<Shift-MouseWheel>", _on_mousewheel_detail_shift)
    scrollable_frame_detail.bind("<Control-MouseWheel>", _on_mousewheel_detail)

    # Bind to the detail plot frame as well
    detail_plot_frame.bind("<MouseWheel>", _on_mousewheel_detail)
    detail_plot_frame.bind("<Button-4>", _on_mousewheel_detail)
    detail_plot_frame.bind("<Button-5>", _on_mousewheel_detail)
    detail_plot_frame.bind("<Shift-MouseWheel>", _on_mousewheel_detail_shift)
    detail_plot_frame.bind("<Control-MouseWheel>", _on_mousewheel_detail)

    # Bind scroll events to matplotlib canvas widget for detailed plot
    def bind_matplotlib_canvas_detail(canvas_widget):
        canvas_widget.bind("<MouseWheel>", _on_mousewheel_detail)
        canvas_widget.bind("<Button-4>", _on_mousewheel_detail)
        canvas_widget.bind("<Button-5>", _on_mousewheel_detail)
        canvas_widget.bind("<Shift-MouseWheel>", _on_mousewheel_detail_shift)
        canvas_widget.bind("<Control-MouseWheel>", _on_mousewheel_detail)

    # Bind to the detailed matplotlib canvas widget
    bind_matplotlib_canvas_detail(canvas_detail_plot.get_tk_widget())

    def update_detail_plot():
        fig_detail.clear()
        ax1, ax2 = fig_detail.subplots(1, 2, sharey=False)  # Changed to False to allow independent scaling

        # Residential plot
        ax1.plot(residential_daily_30d.index, residential_daily_30d['Positive'],
                label='Positive (30-day totals)', color='blue', alpha=0.7, marker='o', markersize=5)
        ax1.plot(residential_daily_30d.index, residential_daily_30d['Cumulative_Positive'],
                label='Cumulative Positive', color='darkblue', linewidth=2)
        ax1.set_title('Residential Cases (30-Day Periods)')
        ax1.set_xlabel('Date (30-Day Periods)')
        ax1.set_ylabel('Number of Cases')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Non-residential plot
        ax2.plot(non_residential_daily_30d.index, non_residential_daily_30d['Positive'],
                label='Positive (30-day totals)', color='red', alpha=0.7, marker='o', markersize=5)
        ax2.plot(non_residential_daily_30d.index, non_residential_daily_30d['Cumulative_Positive'],
                label='Cumulative Positive', color='darkred', linewidth=2)
        ax2.set_title('Non-Residential Cases (30-Day Periods)')
        ax2.set_xlabel('Date (30-Day Periods)')
        ax2.set_ylabel('Number of Cases')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Add statistics for both plots
        res_max = residential_daily_30d['Positive'].max()
        non_res_max = non_residential_daily_30d['Positive'].max()
        res_total = residential_daily_30d['Positive'].sum()
        non_res_total = non_residential_daily_30d['Positive'].sum()

        # Add stats to residential plot
        stats_text1 = f'Residential:\nTotal: {res_total:,}\nMax: {res_max:,}'
        ax1.text(0.02, 0.98, stats_text1, transform=ax1.transAxes, fontsize=9,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

        # Add stats to non-residential plot
        stats_text2 = f'Non-Residential:\nTotal: {non_res_total:,}\nMax: {non_res_max:,}'
        ax2.text(0.02, 0.98, stats_text2, transform=ax2.transAxes, fontsize=9,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))

        # Set x-axis ticks for 30-day periods
        import matplotlib.dates as mdates
        for ax in [ax1, ax2]:
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=30))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        fig_detail.suptitle('Detailed Residential vs Non-Residential Analysis (30-Day Periods)', fontsize=14, fontweight='bold')
        fig_detail.tight_layout()
        canvas_detail_plot.draw()

    # Initialize all plots
    update_plot1()
    update_plot2()
    update_plot3()
    update_detail_plot()

    # Cleanup function to unbind scroll events when window closes
    def on_closing():
        try:
            # Unbind from canvas
            canvas_overview.unbind("<MouseWheel>")
            canvas_overview.unbind("<Button-4>")
            canvas_overview.unbind("<Button-5>")
            canvas_overview.unbind("<Shift-MouseWheel>")
            canvas_overview.unbind("<Control-MouseWheel>")
            canvas_detail.unbind("<MouseWheel>")
            canvas_detail.unbind("<Button-4>")
            canvas_detail.unbind("<Button-5>")
            canvas_detail.unbind("<Shift-MouseWheel>")
            canvas_detail.unbind("<Control-MouseWheel>")

            # Unbind from frames
            scrollable_frame_overview.unbind("<MouseWheel>")
            scrollable_frame_overview.unbind("<Button-4>")
            scrollable_frame_overview.unbind("<Button-5>")
            scrollable_frame_overview.unbind("<Shift-MouseWheel>")
            scrollable_frame_overview.unbind("<Control-MouseWheel>")
            plots_frame.unbind("<MouseWheel>")
            plots_frame.unbind("<Button-4>")
            plots_frame.unbind("<Button-5>")
            plots_frame.unbind("<Shift-MouseWheel>")
            plots_frame.unbind("<Control-MouseWheel>")
            scrollable_frame_detail.unbind("<MouseWheel>")
            scrollable_frame_detail.unbind("<Button-4>")
            scrollable_frame_detail.unbind("<Button-5>")
            scrollable_frame_detail.unbind("<Shift-MouseWheel>")
            scrollable_frame_detail.unbind("<Control-MouseWheel>")
            detail_plot_frame.unbind("<MouseWheel>")
            detail_plot_frame.unbind("<Button-4>")
            detail_plot_frame.unbind("<Button-5>")
            detail_plot_frame.unbind("<Shift-MouseWheel>")
            detail_plot_frame.unbind("<Control-MouseWheel>")

            # Unbind from matplotlib canvas widgets
            canvas1.get_tk_widget().unbind("<MouseWheel>")
            canvas1.get_tk_widget().unbind("<Button-4>")
            canvas1.get_tk_widget().unbind("<Button-5>")
            canvas1.get_tk_widget().unbind("<Shift-MouseWheel>")
            canvas1.get_tk_widget().unbind("<Control-MouseWheel>")
            canvas2.get_tk_widget().unbind("<MouseWheel>")
            canvas2.get_tk_widget().unbind("<Button-4>")
            canvas2.get_tk_widget().unbind("<Button-5>")
            canvas2.get_tk_widget().unbind("<Shift-MouseWheel>")
            canvas2.get_tk_widget().unbind("<Control-MouseWheel>")
            canvas3.get_tk_widget().unbind("<MouseWheel>")
            canvas3.get_tk_widget().unbind("<Button-4>")
            canvas3.get_tk_widget().unbind("<Button-5>")
            canvas3.get_tk_widget().unbind("<Shift-MouseWheel>")
            canvas3.get_tk_widget().unbind("<Control-MouseWheel>")
            canvas_detail_plot.get_tk_widget().unbind("<MouseWheel>")
            canvas_detail_plot.get_tk_widget().unbind("<Button-4>")
            canvas_detail_plot.get_tk_widget().unbind("<Button-5>")
            canvas_detail_plot.get_tk_widget().unbind("<Shift-MouseWheel>")
            canvas_detail_plot.get_tk_widget().unbind("<Control-MouseWheel>")
        except:
            pass
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Bind resize event now that functions are defined
    root.bind('<Configure>', on_window_resize)

    # Add keyboard shortcuts
    def toggle_fullscreen(event):
        """Toggle fullscreen mode with F11 key"""
        if root.attributes('-fullscreen'):
            root.attributes('-fullscreen', False)
        else:
            root.attributes('-fullscreen', True)

    root.bind('<F11>', toggle_fullscreen)

    # Add modern buttons to detail control frame
    ttk.Button(detail_control_content, text="🔥 Peak Analysis", style='Modern.TButton',
              command=show_peak_details).pack(side=tk.LEFT, padx=5)
    ttk.Button(detail_control_content, text="🏠 Residential Details", style='Modern.TButton',
              command=show_residential_details).pack(side=tk.LEFT, padx=5)
    ttk.Button(detail_control_content, text="🌤️ Seasonal Analysis", style='Modern.TButton',
              command=show_seasonal_analysis).pack(side=tk.LEFT, padx=5)
    ttk.Button(detail_control_content, text="📊 Visual Analysis", style='Modern.TButton',
              command=show_seasonal_analysis_visual).pack(side=tk.LEFT, padx=5)
    ttk.Button(detail_control_content, text="💾 Save PNG", style='Secondary.TButton',
              command=lambda: save_plot_png(fig_detail, "detailed_analysis")).pack(side=tk.RIGHT, padx=5)

    # Add modern footer
    footer_frame = tk.Frame(root, bg=COLORS['primary'], height=40)
    footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
    footer_frame.pack_propagate(False)
    
    footer_content = tk.Frame(footer_frame, bg=COLORS['primary'])
    footer_content.pack(expand=True, fill=tk.BOTH, padx=30, pady=8)
    
    footer_text = "🦠 COVID-19 Analysis Dashboard | Advanced Data Visualization | Built with Python & Matplotlib"
    footer_label = tk.Label(footer_content, text=footer_text, 
                           font=('Segoe UI', 9), 
                           fg=COLORS['text_secondary'], bg=COLORS['primary'])
    footer_label.pack(side=tk.LEFT)
    
    # Version info
    version_label = tk.Label(footer_content, text="v2.0 | Modern UI", 
                            font=('Segoe UI', 9), 
                            fg=COLORS['text_secondary'], bg=COLORS['primary'])
    version_label.pack(side=tk.RIGHT)
    
    # Configure matplotlib for modern dark theme
    plt.rcParams.update({
        'figure.facecolor': COLORS['surface'],
        'axes.facecolor': COLORS['surface'],
        'axes.edgecolor': COLORS['border'],
        'axes.labelcolor': COLORS['text'],
        'text.color': COLORS['text'],
        'xtick.color': COLORS['text_secondary'],
        'ytick.color': COLORS['text_secondary'],
        'grid.color': COLORS['border'],
        'figure.edgecolor': COLORS['surface'],
        'savefig.facecolor': COLORS['surface'],
        'savefig.edgecolor': COLORS['surface']
    })
    
    root.mainloop()

# Run the dashboard
if __name__ == "__main__":
    create_dashboard()
