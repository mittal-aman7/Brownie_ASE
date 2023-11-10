import numpy as np
import Database 

# Standard Deviation 
STD_DEV_THRESHOLD = 3

def fetch_gas_data():
    return Database.get_gas_usage_data()

def compute_anomalies(gas_data):
    # Calculate mean and standard deviation of gas used
    gas_values = [x['gas_used'] for x in gas_data]
    mean_gas = np.mean(gas_values)
    std_dev_gas = np.std(gas_values)

    # Detect anomalies
    anomalies = [data for data in gas_data if abs(data['gas_used'] - mean_gas) > STD_DEV_THRESHOLD * std_dev_gas]
    return anomalies

def main():
    gas_data = fetch_gas_data()
    anomalies = compute_anomalies(gas_data)
    for anomaly in anomalies:
        # TODO: Implement alerting mechanism. Possible methods include email, SMS, or webhook notifications.
        print(f"Anomaly detected for transaction {anomaly['tx_hash']} with {anomaly['gas_used']} gas used.")
        # send_alert(anomaly['tx_hash'], anomaly['gas_used']) kind of like this

if __name__ == "__main__":
    main()


# TODO: 1. Alerting mechanism 2. Dynamic Anomaly detection 3. Machine learning to identify Anomalies
# 4. User Interface 5. Anomaly History 6. Security 