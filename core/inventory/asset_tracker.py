# core/inventory/asset_tracker.py
import json
from glob import glob

class AIAssetTracker:
    def __init__(self):
        self.assets = {
            'models': [],
            'datasets': [],
            'dependencies': []
        }

    def scan_directory(self, path):
        # Find all model files
        self.assets['models'] = glob(f"{path}/**/*.h5", recursive=True)
        self.assets['models'] += glob(f"{path}/**/*.pkl", recursive=True)
        
        # Find datasets
        self.assets['datasets'] = glob(f"{path}/**/*.csv", recursive=True)
        self.assets['datasets'] += glob(f"{path}/**/*.parquet", recursive=True)
        
        # Find dependency files
        self.assets['dependencies'] = glob(f"{path}/**/requirements.txt", recursive=True)
        
        return self.assets

    def generate_report(self):
        with open('inventory_report.json', 'w') as f:
            json.dump(self.assets, f, indent=2)

# Usage
tracker = AIAssetTracker()
tracker.scan_directory('./models')
tracker.generate_report()
