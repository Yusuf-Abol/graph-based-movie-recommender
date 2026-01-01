"""Training pipeline script"""
import sys
import yaml

if __name__ == '__main__':
    # Load config
    with open('configs/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Your training pipeline here
    print('Starting training...')
