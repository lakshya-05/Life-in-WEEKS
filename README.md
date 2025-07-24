# Life in Weeks Productivity Visualization

## Overview
A Python application that generates a beautiful visualization of your life journey as a productivity heatmap. Based on your date of birth, it shows your weekly productivity patterns across different life phases (childhood, school, college, work) with insightful statistics.

## Features
- Interactive date input (YYYY-MM-DD format)
- Productivity heatmap with 52 weeks/year visualization
- Life phase detection (childhood, school, college, work, retirement)
- Seasonal productivity adjustments
- Elegant HTML output with responsive design
- Calculates days lived, heartbeats, sleep hours, and other interesting stats

## Requirements
- Python 3.6+
- matplotlib
- numpy

Install requirements:
```bash
pip install matplotlib numpy
```

## Usage
- Clone the repository
```bash
git clone https://github.com/lakshya-05/life-in-weeks.git
cd life-in-weeks-productivity
```

- Run the visualization
```bash
python life_in_weeks_productivity.py
```

The program will:

- Prompt for your birth date
- Generate an interactive HTML visualization
- Automatically open it in your default browser
- Output the file path for future reference
- Output file: `life_journey_productivity.html`
