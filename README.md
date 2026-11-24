# Sensor Data Analysis Tool

A python program to generate simulated sensor readings or loads reading from a CSV file, uses NumPy to calculate statistics and creates 2 graphs using Matplotlib

## Requirements
- Python 3
- numpy
- matplotlib

Install dependencies:
pip install -r requirements.txt

## How to Run
python sensor_monitor.py

1. Choose 1 to generate new sensor readings or 2 to load an existing CSV file.
2. Enter the sensor type, number of readings, min/max values, and alert threshold.
3. Check the terminal for statistics and threshold alerts, and view the two graphs.

## Files
- sensor_monitor.py: Main program
- requirements.txt: Required Python libraries
- sensor_data.csv: Sample generated readings
- line_plot.png & histogram.png: Saved graphs
