import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Patch
from scipy import stats
import warnings
import os
from matplotlib.backends.backend_pdf import PdfPages

# Suppress matplotlib display
import matplotlib

matplotlib.use('Agg')  # Use non-interactive backend

warnings.filterwarnings('ignore')

# Load the shot data from Excel file
df = pd.read_excel('shot_data.xlsx')

# CONFIGURATION - Minimum shots required for analysis
MIN_SHOTS = 350  # Change this value to adjust the minimum shots threshold

# Create Results Figures folder if it doesn't exist
output_folder = 'Result Figures'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Created folder: {output_folder}")

# Map the actual column names to what the code expects
column_mapping = {
    'id': 'shot_id',
    'minute': 'minute',
    'result': 'result',
    'X': 'X',
    'Y': 'Y',
    'xG': 'xG',
    'player': 'player',
    'player_id': 'player_id',
    'situation': 'situation',
    'season': 'season',
    'shotType': 'shot_type',
    'match_id': 'match_id',
    'h_team': 'home_team',
    'a_team': 'away_team',
    'h_goals': 'home_goals',
    'a_goals': 'away_goals',
    'date': 'date',
    'player_assisted': 'assist_player',
    'lastAction': 'last_action'
}

# Rename columns if they exist
for old_name, new_name in column_mapping.items():
    if old_name in df.columns:
        df = df.rename(columns={old_name: new_name})

# Check if we have the required columns
required_cols = ['X', 'Y', 'result', 'xG', 'player']
missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    print(f"ERROR: Missing required columns: {missing_cols}")
    print(f"Available columns: {df.columns.tolist()}")
    exit()

# Ensure player_id exists
if 'player_id' not in df.columns:
    if 'player' in df.columns:
        unique_players = df['player'].unique()
        player_to_id = {p: i for i, p in enumerate(unique_players)}
        df['player_id'] = df['player'].map(player_to_id)
    else:
        print("ERROR: Neither 'player_id' nor 'player' columns found!")
        exit()


# Clean result column - standardize values
def clean_result(result):
    if isinstance(result, str):
        result_lower = result.lower()
        if 'goal' in result_lower:
            return 'Goal'
        elif 'saved' in result_lower:
            return 'SavedShot'
        elif 'block' in result_lower:
            return 'BlockedShot'
        elif 'post' in result_lower or 'woodwork' in result_lower:
            return 'ShotOnPost'
        elif 'miss' in result_lower or 'off target' in result_lower:
            return 'MissedShots'
    return result


df['result'] = df['result'].apply(clean_result)


# Define functions for dimensionless metrics
def calculate_distance(row):
    return np.sqrt((1 - row['X']) ** 2 + (row['Y'] - 0.5) ** 2)


def get_result_coefficient(result):
    result_map = {
        'Goal': 1.0,
        'SavedShot': 0.6,
        'ShotOnPost': 0.5,
        'BlockedShot': 0.2,
        'MissedShots': 0.0,
        'missed': 0.0
    }
    result_str = str(result).strip()
    return result_map.get(result_str, 0.1)


# Function to draw pitch
def draw_pitch(ax):
    """Draw a soccer pitch"""
    # Pitch outline
    ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, edgecolor='black', linewidth=2))

    # Goal
    ax.add_patch(Rectangle((0.94, 0.35), 0.06, 0.30, fill=False, edgecolor='black', linewidth=3))
    ax.add_patch(Rectangle((0.94, 0.40), 0.06, 0.20, fill=True, facecolor='white', alpha=0.3))

    # Center line
    ax.axvline(x=0.5, color='black', linestyle='-', alpha=0.3)

    # Center circle
    ax.add_patch(Circle((0.5, 0.5), 0.08, fill=False, edgecolor='black', linestyle='--', alpha=0.3))

    # Penalty areas
    ax.add_patch(Rectangle((0.78, 0.15), 0.22, 0.70, fill=False, edgecolor='black', linestyle='--', alpha=0.3))
    ax.add_patch(Rectangle((0, 0.15), 0.22, 0.70, fill=False, edgecolor='black', linestyle='--', alpha=0.3))

    # Goal areas
    ax.add_patch(Rectangle((0.88, 0.30), 0.12, 0.40, fill=False, edgecolor='black', linestyle='--', alpha=0.3))
    ax.add_patch(Rectangle((0, 0.30), 0.12, 0.40, fill=False, edgecolor='black', linestyle='--', alpha=0.3))

    # Penalty spots
    ax.plot(0.85, 0.5, 'ko', markersize=4, alpha=0.3)
    ax.plot(0.15, 0.5, 'ko', markersize=4, alpha=0.3)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])


# Function to save a dataframe as a PDF table
def save_table_as_pdf(df, title, filename, folder, highlight_cols=None):
    """Save a pandas DataFrame as a formatted PDF table"""

    fig, ax = plt.subplots(figsize=(12, len(df) * 0.5 + 1))
    ax.axis('off')

    # Add title
    ax.text(0.5, 0.98, title,
            transform=ax.transAxes,
            fontsize=14, fontweight='bold',
            horizontalalignment='center',
            verticalalignment='top')

    # Create the table
    table_data = df.values.tolist()
    columns = df.columns.tolist()

    # Create table
    table = ax.table(cellText=table_data,
                     colLabels=columns,
                     cellLoc='center',
                     loc='center',
                     bbox=[0, 0, 1, 0.85])

    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    # Color the header
    for j, col in enumerate(columns):
        table[(0, j)].set_facecolor('#40466e')
        table[(0, j)].set_text_props(weight='bold', color='white')

    # Color alternating rows
    for i in range(len(table_data)):
        for j in range(len(columns)):
            if i % 2 == 0:
                table[(i + 1, j)].set_facecolor('#f5f5f5')
            else:
                table[(i + 1, j)].set_facecolor('#e0e0e0')

    # Highlight specific columns if requested
    if highlight_cols:
        for col_name in highlight_cols:
            if col_name in columns:
                col_idx = columns.index(col_name)
                for i in range(len(table_data)):
                    table[(i + 1, col_idx)].set_facecolor('#ffeb3b')
                    table[(i + 1, col_idx)].set_text_props(weight='bold')

    # Save the figure as PDF
    save_path = os.path.join(folder, filename)
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white', format='pdf')
    plt.close(fig)
    print(f"✓ Table saved to: {save_path}")


# Function to create combined SEN and CPG figure (no display)
def create_combined_figure(data, player_name, save_path):
    """Create a combined figure with SEN and CPG side by side and save it as PDF"""

    fig = plt.figure(figsize=(20, 10))

    # Metrics to plot
    metrics = [
        ('SEN', 'Shot Efficiency Number (SEN)', 'coolwarm', 'Larger/redder dot = more efficient'),
        ('CPG', 'Conversion Pressure Gradient (CPG)', 'coolwarm', 'Red = above avg, Blue = below avg')
    ]

    # Store regression results for display
    regression_results = {}

    # Create subplots for each metric
    for idx, (metric_name, title, cmap, legend_text) in enumerate(metrics):
        # Position: left (idx=0) or right (idx=1)
        left_pos = 0.02 if idx == 0 else 0.52
        width = 0.45

        # Create pitch axes
        ax_pitch = plt.axes([left_pos, 0.35, width, 0.55])
        draw_pitch(ax_pitch)

        # Create scatterplot axes below the pitch
        ax_scatter = plt.axes([left_pos, 0.08, width, 0.22])

        # Get metric values
        metric_values = data[metric_name].values
        vmin = metric_values.min()
        vmax = metric_values.max()

        if vmin == vmax:
            vmin = vmin - 0.1
            vmax = vmax + 0.1

        # Normalize values for size mapping
        norm_values = (metric_values - vmin) / (vmax - vmin) if vmax > vmin else np.ones_like(metric_values)
        sizes = 50 + (norm_values * 250)

        # Choose colormap
        if cmap == 'coolwarm':
            cmap_obj = plt.cm.coolwarm
        else:
            cmap_obj = plt.cm.viridis

        # Plot shots on pitch
        scatter = ax_pitch.scatter(data['X'], data['Y'],
                                   c=data[metric_name],
                                   s=sizes,
                                   cmap=cmap_obj,
                                   edgecolors='black', linewidth=1.5,
                                   vmin=vmin, vmax=vmax, zorder=5, alpha=0.85)

        # Plot goals as stars
        goals = data[data['result'] == 'Goal']
        if len(goals) > 0:
            ax_pitch.scatter(goals['X'], goals['Y'],
                             marker='*', s=400,
                             facecolors='gold', edgecolors='black', linewidth=2,
                             zorder=6)

        # Colorbar
        cbar = plt.colorbar(scatter, ax=ax_pitch, shrink=0.6, pad=0.02)
        cbar.set_label(metric_name, fontsize=11)

        # Pitch title
        n_shots = len(data)
        n_goals = len(goals)
        ax_pitch.set_title(f'{title}\n{player_name} | {n_shots} shots, {n_goals} goals',
                           fontsize=13, fontweight='bold')

        # Pitch legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w',
                       markerfacecolor='gray', markersize=8,
                       markeredgecolor='black', label='Shot location'),
            plt.Line2D([0], [0], marker='*', color='w',
                       markerfacecolor='gold', markersize=12,
                       markeredgecolor='black', label='Goal scored ⭐'),
            Patch(facecolor='none', edgecolor='none', label=legend_text)
        ]

        if metric_name == 'SEN':
            legend_elements.append(Patch(facecolor='none', edgecolor='none',
                                         label='SEN = (xG / avg_xG) × result_coefficient'))
        elif metric_name == 'CPG':
            legend_elements.append(Patch(facecolor='none', edgecolor='none',
                                         label='CPG = (SEN - avg_SEN) / distance'))

        ax_pitch.legend(handles=legend_elements, loc='lower left',
                        bbox_to_anchor=(0.02, 0.02), fontsize=7,
                        framealpha=0.9, edgecolor='black', title='LEGEND')

        # Create scatterplot
        x = data['xG'].values
        y = data[metric_name].values
        goal_mask = data['result'] == 'Goal'

        # Scatter plot
        ax_scatter.scatter(x[~goal_mask], y[~goal_mask],
                           alpha=0.6, s=30, c='blue', label='Non-Goals',
                           edgecolors='black', linewidth=0.5)
        ax_scatter.scatter(x[goal_mask], y[goal_mask],
                           alpha=0.8, s=60, c='gold', label='Goals ⭐',
                           edgecolors='black', linewidth=1.5, marker='*')

        # Linear regression
        try:
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            line_x = np.linspace(x.min(), x.max(), 100)
            line_y = slope * line_x + intercept
            ax_scatter.plot(line_x, line_y, 'r-', linewidth=2,
                            label=f'Fit: y = {slope:.3f}x + {intercept:.3f}')

            r_squared = r_value ** 2
            stats_text = f'R² = {r_squared:.3f} | p = {p_value:.4f}'
            ax_scatter.text(0.05, 0.95, stats_text,
                            transform=ax_scatter.transAxes, fontsize=8,
                            verticalalignment='top',
                            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

            # Store results
            regression_results[metric_name] = {
                'R2': r_squared,
                'p': p_value,
                'slope': slope,
                'intercept': intercept,
                'n': len(x)
            }
        except:
            pass

        ax_scatter.set_xlabel('xG', fontsize=9, fontweight='bold')
        ax_scatter.set_ylabel(metric_name, fontsize=9, fontweight='bold')
        ax_scatter.grid(True, alpha=0.3, linestyle='--')
        ax_scatter.legend(loc='lower right', fontsize=7, framealpha=0.9)

    # Add main title
    plt.suptitle(f'{player_name} - Spatial Dimensionless Metrics Analysis',
                 fontsize=16, fontweight='bold', y=0.98)

    plt.tight_layout()
    plt.subplots_adjust(top=0.93)

    # Save the figure as PDF
    plt.savefig(save_path, dpi=300, bbox_inches='tight', format='pdf')
    plt.close(fig)  # Close the figure to free memory

    return regression_results


# Function to create a multi-page PDF with all summaries
def create_summary_pdf(all_summaries, output_path):
    """Create a multi-page PDF with all summary tables and figures"""

    with PdfPages(output_path) as pdf:
        # Page 1: Overall comparison summary
        fig, ax = plt.subplots(figsize=(14, len(all_summaries) * 0.5 + 1))
        ax.axis('off')

        ax.text(0.5, 0.98, 'Overall Player Comparison Summary',
                transform=ax.transAxes, fontsize=16, fontweight='bold',
                horizontalalignment='center', verticalalignment='top')

        # Create table
        table_data = all_summaries.values.tolist()
        columns = all_summaries.columns.tolist()

        table = ax.table(cellText=table_data,
                         colLabels=columns,
                         cellLoc='center',
                         loc='center',
                         bbox=[0, 0, 1, 0.85])

        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.5)

        for j, col in enumerate(columns):
            table[(0, j)].set_facecolor('#40466e')
            table[(0, j)].set_text_props(weight='bold', color='white')

        for i in range(len(table_data)):
            for j in range(len(columns)):
                if i % 2 == 0:
                    table[(i + 1, j)].set_facecolor('#f5f5f5')
                else:
                    table[(i + 1, j)].set_facecolor('#e0e0e0')

        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)


# Function to calculate metrics for a player
def calculate_player_metrics(player_data):
    """Calculate all dimensionless metrics for a player's data"""

    # Calculate distance
    player_data['distance'] = player_data.apply(calculate_distance, axis=1)
    player_data['result_coef'] = player_data['result'].apply(get_result_coefficient)

    total_xG = player_data['xG'].sum()
    n_shots = len(player_data)
    avg_xG_per_shot = total_xG / n_shots if n_shots > 0 else 0.01

    # SEN - Shot Efficiency Number
    player_data['SEN'] = (player_data['xG'] / (avg_xG_per_shot + 0.001)) * player_data['result_coef']

    # CPG - Conversion Pressure Gradient
    player_avg_sen = player_data['SEN'].mean()
    player_data['CPG'] = (player_data['SEN'] - player_avg_sen) / (player_data['distance'] + 0.01)

    return player_data


# Identify all players and their shot counts
player_shot_counts = df.groupby('player_id').size().reset_index(name='shot_count')
player_names = df.groupby('player_id')['player'].first().reset_index()

# Merge to get player names with shot counts
player_stats = player_shot_counts.merge(player_names, on='player_id')

# Filter players with at least MIN_SHOTS
qualified_players = player_stats[player_stats['shot_count'] >= MIN_SHOTS].copy()
qualified_players = qualified_players.sort_values('shot_count', ascending=False)

print("=" * 80)
print(f"ANALYZING PLAYERS WITH AT LEAST {MIN_SHOTS} SHOTS")
print("=" * 80)
print(f"\nTotal players in dataset: {len(player_stats)}")
print(f"Players with >= {MIN_SHOTS} shots: {len(qualified_players)}")
print("\nQualified Players:")
print(qualified_players[['player', 'shot_count']].to_string(index=False))
print("=" * 80)

print("\n" + "=" * 80)
print("METRICS BEING ANALYZED")
print("=" * 80)
print("1. SEN (Shot Efficiency Number)")
print("   - SEN = (xG / avg_xG) × result_coefficient")
print("   - Measures shot efficiency relative to average")
print("\n2. CPG (Conversion Pressure Gradient)")
print("   - CPG = (SEN - avg_SEN) / distance")
print("   - Measures efficiency gradient based on shot distance")
print("=" * 80)

print(f"\nOutput folder: {os.path.abspath(output_folder)}")
print("Figures and tables are being saved as PDFs (no display).")
print("Please check the 'Result Figures' folder after analysis completes.\n")

# Dictionary to store all player metrics and regression results
all_players_metrics = {}
all_regression_results = {}

# Analyze each qualified player
for idx, row in qualified_players.iterrows():
    player_id = row['player_id']
    player_name = row['player']
    shot_count = row['shot_count']

    print(f"\n{'=' * 60}")
    print(f"ANALYZING: {player_name} (ID: {player_id})")
    print(f"Shots: {shot_count}")
    print(f"{'=' * 60}")

    # Filter data for this player
    player_df = df[df['player_id'] == player_id].copy()
    player_df = player_df.reset_index(drop=True)

    # Calculate metrics
    player_df = calculate_player_metrics(player_df)

    # Store in dictionary
    all_players_metrics[player_name] = player_df

    print(f"\n--- Dimensionless Metrics ---")
    print(f"SEN range: {player_df['SEN'].min():.3f} to {player_df['SEN'].max():.3f}")
    print(f"CPG range: {player_df['CPG'].min():.3f} to {player_df['CPG'].max():.3f}")

    # Generate combined figure and save as PDF (no display)
    print(f"\nGenerating and saving combined SEN and CPG figure for {player_name}...")

    # Create filename with player name (replace spaces with underscores)
    filename = f"{player_name.replace(' ', '_')}_SEN_CPG_Analysis.pdf"
    save_path = os.path.join(output_folder, filename)

    # Create the figure and save it as PDF (no display)
    regression_results = create_combined_figure(player_df, player_name, save_path)
    all_regression_results[player_name] = regression_results

    print(f"✓ Figure saved to: {save_path}")

    # Summary statistics for this player
    print(f"\n--- Summary Statistics for {player_name} ---")

    # Group by result
    result_summary = player_df.groupby('result').agg({
        'xG': ['count', 'sum', 'mean'],
        'SEN': 'mean'
    }).round(3)

    print("\nShot Results Summary:")
    print(result_summary)

    # Print regression results
    if player_name in all_regression_results:
        print(f"\nRegression Results:")
        for metric, results in all_regression_results[player_name].items():
            print(f"  {metric}: R² = {results['R2']:.3f}, p = {results['p']:.4f}")

    # Top shots by SEN
    print(f"\nTop 5 Most Efficient Shots (Highest SEN):")
    if 'minute' in player_df.columns:
        top_sen = player_df.nlargest(5, 'SEN')[['minute', 'result', 'X', 'Y', 'xG', 'SEN']]
        print(top_sen.to_string(index=False))

        print(f"\nBottom 5 Least Efficient Shots (Lowest SEN):")
        bottom_sen = player_df.nsmallest(5, 'SEN')[['minute', 'result', 'X', 'Y', 'xG', 'SEN']]
        print(bottom_sen.to_string(index=False))
    else:
        top_sen = player_df.nlargest(5, 'SEN')[['result', 'X', 'Y', 'xG', 'SEN']]
        print(top_sen.to_string(index=False))

        print(f"\nBottom 5 Least Efficient Shots (Lowest SEN):")
        bottom_sen = player_df.nsmallest(5, 'SEN')[['result', 'X', 'Y', 'xG', 'SEN']]
        print(bottom_sen.to_string(index=False))

# Generate overall comparison summary
print("\n" + "=" * 80)
print("OVERALL COMPARISON SUMMARY - ALL PLAYERS")
print("=" * 80)

# Create summary dataframe for all players
summary_data = []
for player_name, player_df in all_players_metrics.items():
    goals = player_df[player_df['result'] == 'Goal']
    summary_data.append({
        'Player': player_name,
        'Shots': len(player_df),
        'Goals': len(goals),
        'Goal_Conversion': len(goals) / len(player_df) * 100,
        'Avg_SEN': player_df['SEN'].mean(),
        'Avg_CPG': player_df['CPG'].mean(),
        'Max_SEN': player_df['SEN'].max(),
        'Min_SEN': player_df['SEN'].min(),
        'Total_xG': player_df['xG'].sum()
    })

summary_df = pd.DataFrame(summary_data)
summary_df = summary_df.sort_values('Shots', ascending=False)

print("\nPlayer Comparison Table:")
print(summary_df.round(3).to_string(index=False))

# Save the summary table as PDF
print("\nSaving summary tables as PDF files...")
save_table_as_pdf(
    summary_df.round(3),
    'Player Comparison Summary',
    'Player_Comparison_Summary.pdf',
    output_folder,
    highlight_cols=['Shots', 'Goals', 'Avg_SEN', 'Avg_CPG']
)

# Find top performers by different metrics
print("\n" + "=" * 80)
print("TOP PERFORMERS")
print("=" * 80)

top_performers_tables = {}

# Only show if we have data
if len(summary_df) > 0:
    print(f"\nHighest Goal Conversion Rate:")
    top_conversion = summary_df.nlargest(3, 'Goal_Conversion')[['Player', 'Shots', 'Goals', 'Goal_Conversion']]
    print(top_conversion.round(2).to_string(index=False))
    top_performers_tables['Goal_Conversion'] = top_conversion

    print(f"\nHighest Average SEN (Efficiency):")
    top_sen_avg = summary_df.nlargest(3, 'Avg_SEN')[['Player', 'Shots', 'Avg_SEN', 'Total_xG']]
    print(top_sen_avg.round(3).to_string(index=False))
    top_performers_tables['Avg_SEN'] = top_sen_avg

    print(f"\nHighest Average CPG (Efficiency Gradient):")
    top_cpg_avg = summary_df.nlargest(3, 'Avg_CPG')[['Player', 'Shots', 'Avg_CPG']]
    print(top_cpg_avg.round(3).to_string(index=False))
    top_performers_tables['Avg_CPG'] = top_cpg_avg

# Save top performers tables as PDF
print("\nSaving top performers tables...")
table_configs = [
    ('Goal_Conversion', 'Highest Goal Conversion Rate', ['Player', 'Shots', 'Goals', 'Goal_Conversion']),
    ('Avg_SEN', 'Highest Average SEN (Efficiency)', ['Player', 'Shots', 'Avg_SEN', 'Total_xG']),
    ('Avg_CPG', 'Highest Average CPG (Efficiency Gradient)', ['Player', 'Shots', 'Avg_CPG'])
]

for key, title, columns in table_configs:
    if key in top_performers_tables:
        df_to_save = top_performers_tables[key][columns].round(3)
        filename = f"Top_Performers_{key}.pdf"
        save_table_as_pdf(
            df_to_save,
            title,
            filename,
            output_folder,
            highlight_cols=[columns[-1]]  # Highlight the metric column
        )

# Create a combined summary PDF
print("\nCreating combined summary PDF...")
summary_pdf_path = os.path.join(output_folder, 'Complete_Analysis_Summary.pdf')
create_summary_pdf(summary_df.round(3), summary_pdf_path)
print(f"✓ Combined summary PDF saved to: {summary_pdf_path}")

print("\n" + "=" * 80)
print("EXPORT SUMMARY")
print("=" * 80)
print(f"All figures and tables have been saved to: {os.path.abspath(output_folder)}")

# Count total exported files
fig_files = len(all_players_metrics)
summary_files = 1  # Player Comparison Summary
top_performer_files = len(table_configs)
total_files = fig_files + summary_files + top_performer_files + 1  # +1 for combined summary

print(f"\nTotal files exported: {total_files}")
print("\nExported files:")
print(f"  Player Analysis Figures (PDF): {fig_files}")
print(f"  Player Comparison Summary (PDF): 1")
print(f"  Top Performers Tables (PDF): {top_performer_files}")
print(f"  Combined Analysis Summary (PDF): 1")

print("\nFile list:")
print(f"  ✓ Player Analysis Figures:")
for player_name in all_players_metrics.keys():
    filename = f"{player_name.replace(' ', '_')}_SEN_CPG_Analysis.pdf"
    print(f"    - {filename}")

print(f"\n  ✓ Summary Tables:")
print(f"    - Player_Comparison_Summary.pdf")
for key in table_configs:
    print(f"    - Top_Performers_{key[0]}.pdf")
print(f"    - Complete_Analysis_Summary.pdf")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print(f"Analyzed {len(all_players_metrics)} players with {MIN_SHOTS}+ shots")
print("All results exported as PDF files")
print("=" * 80)