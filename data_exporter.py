
import pandas as pd
import os

def export_logs_to_csv(log_type, data, filename):
    """
    Exports data to a CSV file.
    Args:
        log_type (str): Type of log (e.g., "chat", "mood", "journal").
        data (pd.DataFrame): DataFrame containing the data to export.
        filename (str): Name of the CSV file to export to.
    """
    try:
        file_exists = os.path.isfile(filename)
        data.to_csv(filename, mode="a", index=False, header=not file_exists)
        return f"Successfully exported {log_type} logs to {filename}"
    except Exception as e:
        return f"Error exporting {log_type} logs: {e}"

def get_all_logs(log_file_path):
    """
    Reads all logs from a given CSV file.
    Args:
        log_file_path (str): Path to the log CSV file.
    Returns:
        pd.DataFrame: DataFrame containing the logs, or an empty DataFrame if file not found.
    """
    if os.path.isfile(log_file_path):
        return pd.read_csv(log_file_path)
    return pd.DataFrame()

if __name__ == "__main__":
    # Example Usage:
    # Create dummy data
    dummy_chat_data = pd.DataFrame({
        "timestamp": ["2025-07-26T10:00:00", "2025-07-26T10:05:00"],
        "user_input": ["Hello", "How are you?"],
        "ai_reply": ["Hi there!", "I am doing well."]
    })
    print(export_logs_to_csv("chat", dummy_chat_data, "test_chat_logs.csv"))

    dummy_mood_data = pd.DataFrame({
        "timestamp": ["2025-07-26T10:00:00"],
        "mood": ["happy"]
    })
    print(export_logs_to_csv("mood", dummy_mood_data, "test_mood_logs.csv"))

    # Read logs
    print("\nReading test_chat_logs.csv:")
    print(get_all_logs("test_chat_logs.csv"))

    print("\nReading test_mood_logs.csv:")
    print(get_all_logs("test_mood_logs.csv"))



