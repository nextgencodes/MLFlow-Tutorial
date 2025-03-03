import pandas as pd
import yaml
import mlflow
import os
import datetime
import re

def load_config(config_path):
    """Loads configuration from a YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def ingest_data(config):
    """Ingests data from the specified source."""
    ingestion_config = config['data_ingestion']
    main_config = config

    if ingestion_config['source_type'] == 'local_csv':
        try:
            if not os.path.exists(main_config['raw_data_path']):
                raise FileNotFoundError(f"The file {main_config['raw_data_path']} was not found.")
            df = pd.read_csv(main_config['raw_data_path'], sep=ingestion_config.get('separator', ','), encoding=ingestion_config.get('encoding', 'utf-8'))
            print(f"Data ingested successfully from {main_config['raw_data_path']}")
            return df

        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None
        except pd.errors.ParserError as e:
            print(f"Error: Could not parse the CSV file.  Check separator and encoding. {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    elif ingestion_config['source_type'] == 'database':
        pass

    elif ingestion_config['source_type'] == 'api':
        pass

    else:
        raise ValueError(f"Unsupported source type: {ingestion_config['source_type']}")

def sanitize_metric_name(name):
    """Creates a valid MLflow metric name by replacing invalid characters.

    Args:
        name: The original string (e.g., a column name).

    Returns:
        A valid MLflow metric name.
    """
    # Replace spaces and parentheses with underscores
    name = re.sub(r'[ ()]', '_', name)
    # Remove any remaining characters that are not alphanumeric, underscore, dash, period, or slash.
    name = re.sub(r'[^a-zA-Z0-9_\-\./]', '', name)
    return name

def run_data_ingestion(config_path='configs/main_config.yaml'):
    """Runs data ingestion, logging parameters and metrics to MLflow."""

    config = load_config(config_path)
    if config is None:
        print("Failed to load configuration.  Exiting.")
        return

    mlflow.set_tracking_uri(config['mlflow_server_uri'])
    mlflow.set_experiment(config['experiment_name'])

    with mlflow.start_run(run_name="Data Ingestion Run") as run:
        # --- Log Parameters ---
        mlflow.log_params(config['data_ingestion'])
        mlflow.log_param("raw_data_path", config['raw_data_path'])
        mlflow.log_param("processed_data_path", config['processed_data_path'])
        mlflow.log_param("mlflow_server_uri", config['mlflow_server_uri'])
        mlflow.log_param("run_id", run.info.run_id)
        mlflow.log_param("experiment_id", run.info.experiment_id)
        mlflow.log_param("timestamp", datetime.datetime.now().isoformat())

        # --- Ingest Data ---
        data = ingest_data(config)

        if data is not None:
            # --- Log Metrics ---
            mlflow.log_metric("num_rows", data.shape[0])
            mlflow.log_metric("num_columns", data.shape[1])

            for dtype in data.dtypes.unique():
                count = data.select_dtypes(include=[dtype]).shape[1]
                mlflow.log_metric(f"num_cols_{dtype}", count)

            total_missing = 0
            for col in data.columns:
                missing_count = data[col].isnull().sum()
                sanitized_col = sanitize_metric_name(col)  # Sanitize the column name
                mlflow.log_metric(f"missing_values_{sanitized_col}", missing_count)
                total_missing += missing_count
            mlflow.log_metric("total_missing_values", total_missing)

            for col in data.columns:
                unique_count = data[col].nunique()
                sanitized_col = sanitize_metric_name(col) # Sanitize
                mlflow.log_metric(f"unique_values_{sanitized_col}", unique_count)

            # --- Log Artifacts ---
            os.makedirs(config['processed_data_path'], exist_ok=True)
            processed_file_path = os.path.join(config['processed_data_path'], 'ingested_data.csv')
            data.to_csv(processed_file_path, index=False)
            mlflow.log_artifact(processed_file_path)
            # mlflow.log_artifact(config_path)

            print(f"Ingested data saved to {processed_file_path}")
        else:
            print("Data ingestion failed.")

if __name__ == '__main__':
    run_data_ingestion()