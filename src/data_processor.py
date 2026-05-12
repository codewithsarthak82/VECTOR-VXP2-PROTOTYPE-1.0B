import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class VectorSequenceProcessor:
    """
    Data Processor for Vector VXP2 Predictive Maintenance System.
    Handles data loading, RUL calculation, normalization, and sequence generation
    for NASA CMAPSS dataset.
    """
    
    def __init__(self):
        self.scaler = MinMaxScaler()
        # NASA CMAPSS files typically have 26 columns: 
        # Engine ID, Cycle, 3 operational settings, and 21 sensors
        self.columns = ['Engine_ID', 'Cycle', 'OpSet1', 'OpSet2', 'OpSet3'] + [f'S{i}' for i in range(1, 22)]
        self.sensor_cols = [f'S{i}' for i in range(1, 22)]
        
    def load_data(self, file_path):
        """
        Universal Data Loader: Autonomously detects space-separated or comma-separated formats.
        Maps commercial headers (unit_id, cycle) to internal Engine_ID/Cycle schema.
        Implements Window Padding: Pre-pads short telemetry streams to 50 cycles.
        """
        try:
            # 1. Load with autonomous delimiter detection
            if hasattr(file_path, "seek"):
                file_path.seek(0)
            df = pd.read_csv(file_path, sep=None, engine='python')
            
            # 2. Header Detection & Standardization
            header_map = {
                'unit_id': 'Engine_ID', 'cycle': 'Cycle',
                'setting1': 'OpSet1', 'setting2': 'OpSet2', 'setting3': 'OpSet3'
            }
            # Add sensor mappings (s1-s21 -> S1-S21)
            for i in range(1, 22):
                header_map[f's{i}'] = f'S{i}'
            
            # Detect if we need to apply mapping or legacy positional mapping
            has_headers = any(h in df.columns for h in ['unit_id', 'cycle', 'Engine_ID', 'Cycle'])
            
            if has_headers:
                df.rename(columns=header_map, inplace=True)
                # Ensure all required columns exist, fill missing with nominals
                for col in self.columns:
                    if col not in df.columns:
                        df[col] = 0.0 if col.startswith('Op') else 500.0 # Nominal fallback
            else:
                # Legacy CMAPSS Fallback (space-separated, no headers)
                if hasattr(file_path, "seek"):
                    file_path.seek(0)
                df = pd.read_csv(file_path, sep=None, engine='python', header=None, names=self.columns, usecols=range(len(self.columns)))

            # 3. Window Padding: Ensure every unit has at least 50 cycles
            window_size = 50
            padded_chunks = []
            for _, group in df.groupby('Engine_ID'):
                if len(group) < window_size:
                    padding_needed = window_size - len(group)
                    # Replicate the first row as padding
                    padding = pd.concat([group.iloc[[0]]] * padding_needed, ignore_index=True)
                    group = pd.concat([padding, group], ignore_index=True)
                padded_chunks.append(group)
            
            final_df = pd.concat(padded_chunks, ignore_index=True)
            return final_df
            
        except Exception as e:
            print(f"CRITICAL: Universal Loader failure: {str(e)}")
            return pd.DataFrame(columns=self.columns)

    def calculate_rul(self, df):
        """
        Creates a ground-truth Remaining Useful Life (RUL) column for training.
        """
        # Group by Engine_ID to find the maximum cycle (end of life) for each engine
        max_cycles = df.groupby('Engine_ID')['Cycle'].max().reset_index()
        max_cycles.rename(columns={'Cycle': 'Max_Cycle'}, inplace=True)
        
        # Merge back and calculate RUL
        df = df.merge(max_cycles, on='Engine_ID', how='left')
        df['RUL'] = df['Max_Cycle'] - df['Cycle']
        df.drop(columns=['Max_Cycle'], inplace=True)
        
        return df

    def normalize_sensors(self, df, fit=True):
        """
        Applies MinMaxScaler to sensors S1 through S21.
        """
        if fit:
            df[self.sensor_cols] = self.scaler.fit_transform(df[self.sensor_cols])
        else:
            df[self.sensor_cols] = self.scaler.transform(df[self.sensor_cols])
        return df

    def gen_sequences(self, df, window_size=50):
        """
        Creates sequences of length window_size for each Engine_ID 
        to ensure sequences don't overlap between different engines.
        
        Returns:
            X (np.ndarray): 3D Numpy array of shape (Samples, window_size, 21)
            y (np.ndarray): 1D Numpy array of corresponding RUL labels if RUL exists
        """
        sequence_data = []
        labels = []
        
        # Generate sequences per engine to prevent overlap memory efficiently
        for _, group in df.groupby('Engine_ID'):
            sensor_data = group[self.sensor_cols].values
            
            has_rul = 'RUL' in group.columns
            if has_rul:
                rul_data = group['RUL'].values
            
            # Create sliding window sequences
            num_sequences = len(group) - window_size + 1
            for i in range(num_sequences):
                sequence_data.append(sensor_data[i : i + window_size])
                
                # The label is typically the RUL at the last time step of the window
                if has_rul:
                    labels.append(rul_data[i + window_size - 1])
                    
        X = np.array(sequence_data)
        
        if labels:
            y = np.array(labels)
            return X, y
            
        return X
