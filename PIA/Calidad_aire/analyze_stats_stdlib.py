
import csv
import statistics

filename = 'AirQuality.csv'
target_values = []

try:
    with open(filename, 'r', encoding='utf-8') as f:
        # Handle potential BOM or encoding issues if any, but utf-8 usually fine
        lines = f.readlines()
        
    # Header is line 0
    # Data starts line 1
    
    for i, line in enumerate(lines):
        if i == 0: continue
        line = line.strip()
        if not line: continue
        
        parts = line.split(';')
        if len(parts) < 10: continue
        
        # NO2(GT) is at index 9
        val_str = parts[9]
        
        # Replace decimal comma
        val_str = val_str.replace(',', '.')
        
        try:
            val = float(val_str)
            if val != -200:
                target_values.append(val)
        except ValueError:
            continue

    if target_values:
        mean_val = statistics.mean(target_values)
        stdev_val = statistics.stdev(target_values)
        min_val = min(target_values)
        max_val = max(target_values)
        
        print(f"Count: {len(target_values)}")
        print(f"Mean: {mean_val:.2f}")
        print(f"StdDev: {stdev_val:.2f}")
        print(f"Min: {min_val:.2f}")
        print(f"Max: {max_val:.2f}")
    else:
        print("No valid data found for NO2(GT)")

except Exception as e:
    print(f"Error: {e}")
