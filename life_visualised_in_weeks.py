
"""
life_in_weeks_productivity.py

Requirements:
    pip install matplotlib numpy
"""

import datetime as dt
import math
import os
import webbrowser
from io import BytesIO
import base64

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def calculate_productivity_score(age_years, week_of_year):
    """
    Calculate productivity score based on life phase and time of year.
    Returns a value between 0.1 (very chill) and 1.0 (highly productive)
    """
    # Base productivity by age/life phase
    if age_years < 6:  # Early childhood
        base_productivity = 0.2
    elif age_years < 12:  # Elementary school
        base_productivity = 0.4
    elif age_years < 18:  # High school
        base_productivity = 0.7
    elif age_years < 23:  # College years
        base_productivity = 0.85
    elif age_years < 65:  # Working years
        base_productivity = 0.8
    else:  # Retirement
        base_productivity = 0.3
    
    # Seasonal adjustments
    seasonal_modifier = 1.0
    
    # Summer break (weeks 24-35, roughly June-August)
    if 24 <= week_of_year <= 35:
        if age_years < 18:  # School age - summer break is chill
            seasonal_modifier = 0.3
        elif 18 <= age_years < 23:  # College - internships/summer courses
            seasonal_modifier = 0.9
        else:  # Working age - normal productivity
            seasonal_modifier = 1.0
    
    # Exam periods (weeks 18-22 for spring, 46-50 for fall)
    elif (18 <= week_of_year <= 22) or (46 <= week_of_year <= 50):
        if 12 <= age_years < 23:  # School and college exam periods
            seasonal_modifier = 1.2
    
    # Holiday periods (weeks 51-2)
    elif week_of_year >= 51 or week_of_year <= 2:
        seasonal_modifier = 0.4
    
    # Spring productivity boost (weeks 10-15)
    elif 10 <= week_of_year <= 15:
        seasonal_modifier = 1.1
    
    final_score = base_productivity * seasonal_modifier
    return max(0.1, min(1.0, final_score))


def create_productivity_heatmap(dob, weeks_lived, weeks_total):
    """Create a productivity heatmap visualization"""
    rows = 75  # Reduced from 90 for smaller visualization
    cols = 52
    
    # Create custom colormap matching the page theme (purple-blue gradient)
    colors = [
        '#f8f9fa',    # Very light (chill periods)
        '#e9ecef',    # Light gray
        '#a8b5d1',    # Light purple-blue
        '#8499d1',    # Medium purple-blue  
        '#667eea',    # Main theme blue
        '#6b73d9',    # Deeper blue
        '#764ba2',    # Deep purple (high productivity)
        '#5a4482'     # Darkest purple
    ]
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('productivity', colors, N=n_bins)
    
    fig, ax = plt.subplots(figsize=(10, 8))     
    productivity_data = np.full((rows, cols), np.nan)
    
    for week in range(min(weeks_lived, weeks_total)):
        age_weeks = week
        age_years = age_weeks / 52.0
        
        if age_years >= rows:  # Don't go beyond our visualization
            break
            
        row = int(age_years)
        col = week % cols
        week_of_year = col + 1
        
        productivity = calculate_productivity_score(age_years, week_of_year)
        productivity_data[row, col] = productivity
    
    # Create the heatmap
    im = ax.imshow(productivity_data, cmap=cmap, aspect='auto', 
                   interpolation='nearest', alpha=0.9)
    
    # Styling
    ax.set_xlim(-0.5, cols-0.5)
    ax.set_ylim(rows-0.5, -0.5)  # Flip y-axis so age 0 is at top
    
    # Add subtle grid
    ax.set_xticks(np.arange(0, cols, 13))  # Quarterly marks
    ax.set_xticklabels(['Jan', 'Apr', 'Jul', 'Oct'])
    ax.set_yticks(np.arange(0, rows, 5))
    ax.set_yticklabels([f'{i}' for i in range(0, rows, 5)])
    
    ax.tick_params(colors='#8499d1', labelsize=9)
    ax.grid(True, alpha=0.08, color='#a8b5d1')
    
    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    plt.tight_layout()
    
    # Save to base64
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches='tight', 
                transparent=True, facecolor='none')
    plt.close(fig)
    img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    
    return img_b64


def main():
    # ----------------------------
    # 1) Input
    # ----------------------------
    dob_str = input("Enter your date of birth (YYYY-MM-DD): ").strip()
    try:
        dob = dt.datetime.strptime(dob_str, "%Y-%m-%d").date()
    except ValueError:
        raise SystemExit("Invalid date format. Please use YYYY-MM-DD.")

    LIFE_EXPECTANCY_YEARS = 75  # Will live this much maybe?
    
    # ----------------------------
    # 2) Derived stats
    # ----------------------------
    today = dt.date.today()
    days_lived = (today - dob).days
    if days_lived < 0:
        raise SystemExit("You entered a future birth date. Please try again.")

    weeks_lived = days_lived // 7
    weeks_total = LIFE_EXPECTANCY_YEARS * 52
    pct_life = int((weeks_lived / weeks_total) * 100) if weeks_total else 0

    age_years = int(days_lived / 365.2425)
    seasons = days_lived // 92
    heartbeats = int(days_lived * 80_000)
    breaths = int(days_lived * 16_000)
    sleep_hours = int(days_lived * 8)
    lunar_cycles = int(days_lived / 29.53)
    books_could_read = int(age_years * 8)  # ~8 books per year (not a bookworm!)
    movies_watched = int(age_years * 20)   # ~20 movies per year
    
    # Calculate average productivity
    total_productivity = 0
    for week in range(min(weeks_lived, weeks_total)):
        age_at_week = week / 52.0
        week_of_year = (week % 52) + 1
        total_productivity += calculate_productivity_score(age_at_week, week_of_year)
    
    avg_productivity = (total_productivity / weeks_lived * 100) if weeks_lived > 0 else 0

    # ----------------------------
    # 3) Generate the productivity heatmap
    # ----------------------------
    img_b64 = create_productivity_heatmap(dob, weeks_lived, weeks_total)

    # ----------------------------
    # 4) Beautiful HTML
    # ----------------------------
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Your Life Journey</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    body {{
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        color: #2c3e50;
        line-height: 1.6;
    }}
    
    .container {{
        max-width: 1000px;
        margin: 0 auto;
        padding: 2rem;
    }}
    
    .header {{
        text-align: center;
        margin-bottom: 3rem;
        color: white;
    }}
    
    .title {{
        font-size: 2.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }}
    
    .subtitle {{
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 300;
    }}
    
    .main-content {{
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }}
    
    .heatmap-container {{
        margin: 2rem 0;
        text-align: center;
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }}
    
    .heatmap-title {{
        font-size: 1.3rem;
        font-weight: 500;
        margin-bottom: 1rem;
        color: #34495e;
    }}
    
    .heatmap-subtitle {{
        font-size: 0.9rem;
        color: #8499d1;
        margin-bottom: 1.5rem;
    }}
    
    .heatmap-img {{
        width: 100%;
        max-width: 700px;
        height: auto;
        border-radius: 10px;
    }}
    
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }}
    
    .stat-card {{
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 4px solid #667eea;
        transition: transform 0.2s ease;
    }}
    
    .stat-card:hover {{
        transform: translateY(-2px);
    }}
    
    .stat-number {{
        font-size: 1.8rem;
        font-weight: 600;
        color: #495057;
        margin-bottom: 0.3rem;
    }}
    
    .stat-label {{
        font-size: 0.95rem;
        color: #6c757d;
        font-weight: 400;
    }}
    
    .productivity-badge {{
        display: inline-block;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        margin: 1rem 0;
    }}
    
    .legend {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 1rem;
        font-size: 0.85rem;
        color: #7f8c8d;
    }}
    
    .legend-item {{
        display: flex;
        align-items: center;
        margin: 0 1rem;
    }}
    
    .legend-color {{
        width: 12px;
        height: 12px;
        border-radius: 2px;
        margin-right: 0.5rem;
    }}
    
    .footer {{
        text-align: center;
        margin-top: 3rem;
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
        font-weight: 300;
    }}
    
    @media (max-width: 768px) {{
        .container {{
            padding: 1rem;
        }}
        
        .title {{
            font-size: 2.2rem;
        }}
        
        .main-content {{
            padding: 1.5rem;
        }}
        
        .stats-grid {{
            grid-template-columns: 1fr;
        }}
    }}
</style>
</head>
<body>

<div class="container">
    <div class="header">
        <div class="title">Your Life Journey</div>
        <div class="subtitle">Born {dob.strftime("%B %d, %Y")} • {weeks_lived:,} weeks of experiences</div>
    </div>
    
    <div class="main-content">
        <div class="heatmap-container">
            <div class="heatmap-title">Productivity Heatmap</div>
            <div class="heatmap-subtitle">Each square represents a week. Darker colors indicate periods of higher productivity and focus.</div>
            <img src="data:image/png;base64,{img_b64}" alt="Life productivity heatmap" class="heatmap-img">
            
            <div class="legend">
                <div class="legend-item">
                    <div class="legend-color" style="background: #764ba2;"></div>
                    <span>High Focus</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #667eea;"></div>
                    <span>Moderate</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #a8b5d1;"></div>
                    <span>Chill Time</span>
                </div>
            </div>
            
            <div class="productivity-badge">
                Average Life Productivity: {avg_productivity:.1f}%
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{pct_life}%</div>
                <div class="stat-label">of your projected life journey completed</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-number">{days_lived:,}</div>
                <div class="stat-label">days of unique experiences</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-number">{seasons:,}</div>
                <div class="stat-label">seasons witnessed and felt</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-number">{heartbeats:,}</div>
                <div class="stat-label">heartbeats keeping you alive</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-number">{sleep_hours:,}</div>
                <div class="stat-label">hours spent in dreams</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-number">{lunar_cycles:,}</div>
                <div class="stat-label">lunar cycles observed</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-number">~{books_could_read:,}</div>
                <div class="stat-label">books you could have read by now</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-number">~{movies_watched:,}</div>
                <div class="stat-label">movies worth of stories experienced</div>
            </div>
        </div>
    </div>
</div>

<div class="footer">
    Life is not measured by the number of breaths we take, but by the moments that take our breath away
</div>

</body>
</html>
"""

    # ----------------------------
    # 5) Write & auto-open
    # ----------------------------
    out_name = "life_journey_productivity.html"
    with open(out_name, "w", encoding="utf-8") as f:
        f.write(html)

    abs_path = os.path.abspath(out_name)
    webbrowser.open(f"file://{abs_path}")
    print(f"\nGenerated: {abs_path}")


if __name__ == "__main__":
    main()
