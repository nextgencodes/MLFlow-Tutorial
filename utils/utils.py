# src/utils/utils.py
import yaml
import pandas as pd

def load_config(config_path):
    """Loads configuration from a YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def handle_zero_division(numerator, denominator):
    """Safely handles division, returning 0 if the denominator is 0."""
    return numerator / denominator if denominator != 0 else 0