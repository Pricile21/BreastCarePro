#!/usr/bin/env python3
"""
ULTRA-MINIMAL training for free tier server
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

def main():
    """Ultra-minimal training for free tier"""
    print("MEDSIGLIP ULTRA-MINIMAL TRAINING")
    print("=" * 60)
    print("Ultra-minimal settings for free tier server!")
    print("Only 500 samples, batch size 3, 2 epochs")
    print("=" * 60)
    
    from ml.train_medsiglip import MedSigLIPTrainer
    
    # Create trainer with ultra-minimal settings
    trainer = MedSigLIPTrainer(fine_tune=True, training_step="views", max_samples=500)
    
    # Override settings for ultra-minimal
    trainer.batch_size = 1  # Minimal batch size
    trainer.epochs = 2  # Minimal epochs
    trainer.learning_rate = 1e-4
    
    print(f"Ultra-minimal configuration:")
    print(f"  - Max samples: 500")
    print(f"  - Batch size: {trainer.batch_size}")
    print(f"  - Epochs: {trainer.epochs}")
    print(f"  - Learning rate: {trainer.learning_rate}")
    
    # Train model
    results = trainer.train_model()
    
    print("\n" + "=" * 60)
    print("ULTRA-MINIMAL TRAINING COMPLETED!")
    print("✅ View detection trained with minimal data!")
    print("=" * 60)

if __name__ == "__main__":
    main()

