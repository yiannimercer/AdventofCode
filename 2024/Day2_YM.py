from dotenv import load_dotenv
load_dotenv()
from aocd import get_data, submit
import pandas as pd

# ------------------------------------------------
# PUZZLE 1 
# ------------------------------------------------

data = [report.split(' ') for report in get_data(day=2, year=2024).splitlines()]
data = [[int(level) for level in report] for report in data]

# Check for all increasing or all decreasing
safe_reports_count = []
for report in data:
    report_series = pd.Series(report)
    safe_report = report_series.is_unique and (report_series.is_monotonic_increasing or report_series.is_monotonic_decreasing)
    if safe_report:
        # Calculate differences between consecutive values
        differences = report_series.diff().dropna().abs()
        
        # Check if all differences are between 1 and 3 (inclusive)
        if differences.between(1, 3).all():
            safe_report = True
        else:
            safe_report = False
    else:
        safe_report = False
        
    safe_reports_count.append(safe_report)
    
# Sum safe report counts
answer_1 = sum(safe_reports_count)

# Submit
submit(answer=answer_1, day=2, year=2024, part='a')

# ------------------------------------------------
# PUZZLE 2 
# ------------------------------------------------

# Convert above logic to a function to make it easier to iterate over
def safe_report_logic(report_series_input):
    safe_report = report_series_input.is_unique and (report_series_input.is_monotonic_increasing or report_series_input.is_monotonic_decreasing)
    if safe_report:
        # Calculate differences between consecutive values
        differences = report_series_input.diff().dropna().abs()
        
        # Check if all differences are between 1 and 3 (inclusive)
        if differences.between(1, 3).all():
            safe_report = True
        else:
            safe_report = False
    else:
        safe_report = False
    
    return safe_report


safe_reports_count = []

for report in data:
    report_series = pd.Series(report)  # Convert the list to a pandas Series
    is_safe = safe_report_logic(report_series)  # Check the full series first

    # If the full series is not safe, try dropping elements one by one
    if not is_safe:
        for i in range(len(report_series)):
            # Create a new series without the current element
            temp_series = report_series.drop(report_series.index[i]).reset_index(drop=True)
            
            # Check if the modified series is safe
            if safe_report_logic(temp_series):
                is_safe = True
                break  # Exit the loop as soon as a safe subset is found

    # Append the result to the safe_reports_count list
    safe_reports_count.append(is_safe)

# Sum safe_reports_count
answer_2 = sum(safe_reports_count)

# Submit
submit(answer_2, day=2, year=2024, part='b')