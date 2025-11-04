#!/usr/bin/env python3
"""
STEP 2: Train FINDING detection only
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

def main():
    """Step 2: Train finding detection only"""
    print("MEDSIGLIP STEP 2: FINDING DETECTION TRAINING")
    print("=" * 60)
    print("Training only FINDING detection (Mass, Calcification, etc.)")
    print("This should be much faster and fit in free tier limits!")
    print("=" * 60)
    
    from ml.train_medsiglip import MedSigLIPTrainer
    
    # Create trainer for step 2 (findings only)
    trainer = MedSigLIPTrainer(fine_tune=True, training_step="findings")
    
    # Train model
    results = trainer.train_model()
    
    print("\n" + "=" * 60)
    print("STEP 2 COMPLETED!")
    print("Your model now has both VIEW and FINDING detection capabilities!")
    print("🎉 Training completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
