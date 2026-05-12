import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf

# Add project root to sys.path
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from src.data_processor import VectorSequenceProcessor
from src.engine import VectorLSTM

def run_fast_track_training():
    print("--- VECTOR VXP2: FAST-TRACK MODEL INITIALIZATION ---")
    
    # 1. Initialize Processor
    processor = VectorSequenceProcessor()
    
    # 2. Load and Preprocess Data (FD001)
    train_path = os.path.join(_PROJECT_ROOT, "data", "train_FD001.txt")
    if not os.path.exists(train_path):
        print(f"ERROR: Training data not found at {train_path}")
        return

    print(f"Step 1/4: Ingesting NASA CMAPSS dataset from {os.path.basename(train_path)}...")
    df = processor.load_data(train_path)
    df = processor.calculate_rul(df)
    df = processor.normalize_sensors(df, fit=True)
    
    # 3. Generate Sequences (Window=50, Sensors=21)
    print("Step 2/4: Generating 3D telemetry sequences (50x21 window)...")
    X_train, y_train = processor.gen_sequences(df, window_size=50)
    print(f"Data ready. Input Shape: {X_train.shape}, Labels: {y_train.shape}")
    
    # 4. Initialize and Train Model
    print("Step 3/4: Initializing VectorLSTM Core Architecture...")
    vector_engine = VectorLSTM()
    
    # Fast-track 7-epoch fit
    print("Step 4/4: Executing 7-epoch fit cycle. High-intensity compute engaged...")
    vector_engine.model.fit(
        X_train, 
        y_train, 
        epochs=7, 
        batch_size=64, 
        verbose=1,
        validation_split=0.1
    )
    
    # 5. Export Gold Master
    model_dir = os.path.join(_PROJECT_ROOT, "models")
    os.makedirs(model_dir, exist_ok=True)
    model_save_path = os.path.join(model_dir, "vxp2_lstm_v1.h5")
    
    # Saving in standard Keras H5 format for deployment
    vector_engine.model.save(model_save_path)
    print(f"\n✅ TRAINING SUCCESSFUL: Model exported to {model_save_path}")
    print(f"Model File Size: {os.path.getsize(model_save_path) / 1024:.2f} KB")

if __name__ == "__main__":
    run_fast_track_training()
