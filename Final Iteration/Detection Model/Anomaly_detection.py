import numpy as np
import Database 
from anomaly_alert import send_email_alert


def fetch_gas_data():
    return Database.get_gas_usage_data()

def fetch_historical_gas_data():
    return Database.get_historical_gas_usage()

def compute_std_dev_threshold(historical_gas_data):
    gas_values = [x[0] for x in historical_gas_data]  # Assuming x[0] is the gas_used value
    mean_gas = np.mean(gas_values)
    std_dev_gas = np.std(gas_values)
    return mean_gas, std_dev_gas

def is_anomaly(current_gas, mean_gas, std_dev_gas):
    return abs(current_gas - mean_gas) > std_dev_gas

def compute_anomalies(current_gas_data, mean_gas, std_dev_gas):
    return [data for data in current_gas_data if is_anomaly(data['gas_used'], mean_gas, std_dev_gas)]

def main():
    historical_gas_data = fetch_historical_gas_data()
    mean_gas, std_dev_gas = compute_std_dev_threshold(historical_gas_data)
    
    current_gas_data = fetch_gas_data()
    anomalies = compute_anomalies(current_gas_data, mean_gas, std_dev_gas)
    
    for anomaly in anomalies:
        print(f"Anomaly detected for transaction {anomaly['tx_hash']} with {anomaly['gas_used']} gas used.")
        alert_message = f"Anomaly detected for transaction {anomaly['tx_hash']} with {anomaly['gas_used']} gas used."
        send_email_alert("Anomaly Detected", alert_message, "mittalaman026@gmail.com")
        Database.insert_anomaly(anomaly['tx_hash'], anomaly['gas_used'])

if __name__ == "__main__":
    main()



# TODO: 3. Machine learning to identify Anomalies
# 6. Security 