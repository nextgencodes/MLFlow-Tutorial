# src/main.py
from data.ingest_data import run_data_ingestion
#from src.data.validate_data import run_data_validation # Import when you have this
# ... other imports ...

def main():
    """Main entry point for the project."""

    # 1. Data Ingestion
    print("Running data ingestion...")
    run_data_ingestion()  # No arguments needed now


    # # 2. Data Validation (Add later)
    # print("Running data validation...")
    # run_data_validation()
    #
    # # 3. Data Preprocessing (Add later)
    # print("Running data preprocessing...")
    # run_data_preprocessing()
    #
    #
    # # 4. Feature Engineering (Add later)
    # print("Running Feature Engineering...")
    # run_feature_engineering()
    #
    #
    # # 5. Model Training (Add later)
    # print("Running model training...")
    # run_model_training()
    #
    # # 6. Model Evaluation (Add later)
    # print("Running model evaluation...")
    # run_model_evaluation()

    # # 7. Model Deployment - (Add Later)
    # print("Running model deployment...")
    # run_model_deployment()

if __name__ == "__main__":
    main()