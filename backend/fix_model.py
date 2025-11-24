"""
Script to fix and convert the old CNN model to be compatible with TensorFlow 2.13.0
"""
import h5py
import json
import os

model_path = 'cnn_model.h5'

try:
    # Read the model file
    with h5py.File(model_path, 'r+') as f:
        # Check if model_config exists
        if 'model_config' in f.attrs:
            config_str = f.attrs['model_config']
            if isinstance(config_str, bytes):
                config_str = config_str.decode('utf-8')
            
            config = json.loads(config_str)
            
            # Fix batch_shape -> batch_input_shape
            def fix_config(obj):
                if isinstance(obj, dict):
                    if 'batch_shape' in obj:
                        obj['batch_input_shape'] = obj.pop('batch_shape')
                    for v in obj.values():
                        fix_config(v)
                elif isinstance(obj, list):
                    for item in obj:
                        fix_config(item)
            
            fix_config(config)
            f.attrs['model_config'] = json.dumps(config).encode('utf-8')
            print("Model config fixed!")
    
    # Try loading with Keras
    from tensorflow import keras
    model = keras.models.load_model(model_path, compile=False)
    
    # Re-save the model in the new format
    model.save('cnn_model_fixed.h5')
    print("Model successfully converted and saved as cnn_model_fixed.h5")
    
    # Replace the old model
    os.replace('cnn_model_fixed.h5', 'cnn_model.h5')
    print("Original model replaced!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
