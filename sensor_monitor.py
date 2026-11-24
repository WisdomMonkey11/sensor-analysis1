import random
import csv
import numpy as np
import matplotlib.pyplot as plt


def get_user_input():
    # ask for sensor name
    sensor_type = input("Enter sensor type (e.g. temperature, light): ")
    while sensor_type.strip() == "":
        print("Sensor type cannot be empty.")
        sensor_type = input("Enter sensor type (e.g. temperature, light): ")

    # ask for number of readings
    while True:
        try:
            num_readings = int(input("Enter number of readings: "))
            if num_readings <= 0:
                print("Error: number of readings must be greater than 0.")
            else:
                break
        except ValueError:
            print("Error: please enter a whole number.")

    # ask for min and max values
    while True:
        try:
            min_val = float(input("Enter minimum sensor value: "))
            max_val = float(input("Enter maximum sensor value: "))
            if min_val >= max_val:
                print("Error: minimum value must be less than maximum value.")
            else:
                break
        except ValueError:
            print("Error: please enter valid numbers.")

    # ask for alert threshold
    while True:
        try:
            threshold = float(input("Enter alert threshold: "))
            break
        except ValueError:
            print("Error: please enter a valid number.")

    return sensor_type, num_readings, min_val, max_val, threshold


def generate_readings(num_readings, min_val, max_val):
    random.seed(42)  # makes results reproducible
    readings = []
    for i in range(num_readings):
        val = random.uniform(min_val, max_val)
        readings.append(round(val, 2))
    return np.array(readings)


def calculate_statistics(readings, threshold):
    count = len(readings)
    mean_val = np.mean(readings)
    min_val = np.min(readings)
    max_val = np.max(readings)
    std_val = np.std(readings)

    above_count = 0
    for value in readings:
        if value > threshold:
            above_count = above_count + 1

    print("\n--- Analysis Results ---")
    print("Number of readings:", count)
    print("Mean:", round(mean_val, 2))
    print("Minimum:", round(min_val, 2))
    print("Maximum:", round(max_val, 2))
    print("Standard deviation:", round(std_val, 2))
    print("Readings above threshold:", above_count)


def find_outliers(readings, threshold):
    outliers = []
    for i in range(len(readings)):
        if readings[i] > threshold:
            outliers.append((i + 1, readings[i]))

    print("\n--- Readings Above Threshold ---")
    if len(outliers) == 0:
        print("No readings exceeded the threshold.")
    else:
        for item in outliers:
            print("Sample", item[0], ":", round(item[1], 2))

    return outliers


def save_readings(readings, filename):
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Sample Number", "Sensor Reading"])
            for i in range(len(readings)):
                writer.writerow([i + 1, readings[i]])
        print("Saved readings to", filename)
    except Exception as e:
        print("Error saving CSV file:", e)


def load_readings(filename):
    readings = []
    try:
        with open(filename, "r") as file:
            reader = csv.reader(file)
            next(reader)  # skip header row
            for row in reader:
                if len(row) >= 2:
                    readings.append(float(row[1]))

        if len(readings) == 0:
            print("Error: CSV file has no readings.")
            return None

        return np.array(readings)
    except FileNotFoundError:
        print("Error: file not found.")
        return None
    except Exception as e:
        print("Error loading CSV file:", e)
        return None


def plot_readings(readings, sensor_type, threshold):
    samples = range(1, len(readings) + 1)

    plt.figure()
    plt.plot(samples, readings, marker="o", label=sensor_type + " Readings")
    plt.axhline(y=threshold, color="red", linestyle="--", label="Alert Threshold")
    plt.title(sensor_type + " Sensor Readings")
    plt.xlabel("Sample Number")
    plt.ylabel("Sensor Value")
    plt.grid(True)
    plt.legend()
    plt.savefig("line_plot.png")
    plt.show()


def plot_histogram(readings, sensor_type):
    plt.figure()
    plt.hist(readings, bins=10, edgecolor="black", label=sensor_type)
    plt.title(sensor_type + " Readings Distribution")
    plt.xlabel("Sensor Value")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.legend()
    plt.savefig("histogram.png")
    plt.show()


def main():
    print("1. Generate new sensor readings")
    print("2. Load readings from an existing CSV file")

    choice = input("Choose 1 or 2: ")
    while choice != "1" and choice != "2":
        print("Invalid choice. Enter 1 or 2.")
        choice = input("Choose 1 or 2: ")

    if choice == "1":
        sensor_type, num_readings, min_val, max_val, threshold = get_user_input()
        readings = generate_readings(num_readings, min_val, max_val)

        filename = input("Enter CSV filename to save (press Enter for sensor_data.csv): ")
        if filename.strip() == "":
            filename = "sensor_data.csv"
        save_readings(readings, filename)
    else:
        filename = input("Enter CSV filename to load (e.g. sensor_data.csv): ")
        readings = load_readings(filename)
        if readings is None:
            return

        sensor_type = input("Enter sensor type for the graphs: ")
        if sensor_type.strip() == "":
            sensor_type = "Sensor"

        while True:
            try:
                threshold = float(input("Enter alert threshold: "))
                break
            except ValueError:
                print("Error: please enter a valid number.")

    calculate_statistics(readings, threshold)
    find_outliers(readings, threshold)
    plot_readings(readings, sensor_type, threshold)
    plot_histogram(readings, sensor_type)


if __name__ == "__main__":
    main()