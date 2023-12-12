import pandas as pd
import os
import re

# Function to process a single file
def process_file(file_path):
    with open(file_path, 'r') as file:
        # Initialize variables
        temperature, humidity, light_intensity, soil_moisture = None, None, None, None
        door_state, light_state, fan_state, pump_state = None, None, None, None
        data = []

        for line in file:
            # Parse the sensor readings
            if "DHT_Temperature" in line:
                temperature = float(line.split('=')[-1].strip())
                if(temperature <= 23) : fan_state = 0
                
            elif "Humidity" in line:
                humidity = float(line.split('=')[-1].strip())
                if(humidity < 70) : fan_state = 0
            
            elif "Light intensity" in line:
                light_intensity = float(line.split('=')[-1].strip())
                if(light_intensity <= 390) : light_state = 0
            
            elif "Soil Moisture" in line:
                soil_moisture = float(line.split('=')[-1].strip())
                if(soil_moisture > 626) : pump_state = 0           
            # Update device states
            elif "Door State" in line:
                door_state = 0 if "Closed" in line else 1
            elif "LIGHTS" in line:
                light_state = 1 if "ON" in line else 0
            elif "FANS" in line:
                fan_state = 1 if "ON" in line else 0
            elif "PUMP" in line:
                pump_state = 1 if "ON" in line else 0

            # Add a new entry to the data list  
            entry = {
                'Temperature': temperature,
                'Humidity': humidity,
                'Light Intensity': light_intensity,
                'Soil Moisture': soil_moisture,
                'Door State': door_state,
                'Light State': light_state,
                'Fan State': fan_state,
                'Pump State': pump_state
            }
            data.append(entry)

    # Convert the list of data to a DataFrame
    df = pd.DataFrame(data)
    return df

# Directory where the files are stored
directory = 'C:\\Users\\avhis\\Documents\\UNL Courses\\Internet of Things\\Course_Project'

# List to hold all DataFrames
all_dfs = []

# Loop through each file and process it
for i in range(1, 11):  # Assuming 10 files named sensor_data1.txt to sensor_data10.txt
    file_path = os.path.join(directory, f'sensor_data{i}.txt')
    df = process_file(file_path)
    all_dfs.append(df)

# Concatenate all DataFrames into one
combined_df = pd.concat(all_dfs)

# Handle missing values by forward filling and dropping remaining NaNs
combined_df_filled = combined_df.ffill().dropna()

# Save the processed DataFrame as a CSV file
output_file_path = os.path.join(directory, 'combined_sensor_data.csv')
combined_df_filled.to_csv(output_file_path, index=False)

print(f"Saved combined data to {output_file_path}")
