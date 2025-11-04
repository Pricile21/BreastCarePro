#!/usr/bin/env python3
"""
STEP 1: Train VIEW detection only
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

def main():
    """Step 1: Train view detection only"""
    print("MEDSIGLIP STEP 1: VIEW DETECTION TRAINING")
    print("=" * 60)
    print("Training only VIEW detection (CC/MLO, LEFT/RIGHT)")
    print("This should be much faster and fit in free tier limits!")
    print("=" * 60)
    
    from ml.train_medsiglip import MedSigLIPTrainer
    
    # Create trainer for step 1 (views only)
    trainer = MedSigLIPTrainer(fine_tune=True, training_step="views")
    
    # Train model
    results = trainer.train_model()
    
    print("\n" + "=" * 60)
    print("STEP 1 COMPLETED!")
    print("Your model now has VIEW detection capabilities!")
    print("Next: Run step 2 for finding detection")
    print("=" * 60)

if __name__ == "__main__":
    main()
