import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
import numpy as np
from pathlib import Path
import os

class OptimizedMammographyModel:
    """
    Modèle CNN optimisé pour la mammographie
    Architecture simple et efficace
    """
    
    def __init__(self, num_bi_rads_classes=5, num_density_classes=4, input_shape=(512, 512, 3)):
        self.num_bi_rads_classes = num_bi_rads_classes
        self.num_density_classes = num_density_classes
        self.input_shape = input_shape
        self.model = None
        
    def create_model(self):
        """Créer l'architecture CNN optimisée"""
        
        # Input layer
        input_layer = layers.Input(shape=self.input_shape, name='mammography_input')
        
        # Convolutional layers avec batch normalization
        x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(input_layer)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        
        x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        
        x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        
        x = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        
        # Global Average Pooling pour éviter l'overfitting
        x = layers.GlobalAveragePooling2D()(x)
        
        # Dense layers avec dropout
        x = layers.Dense(512, activation='relu')(x)
        x = layers.Dropout(0.5)(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dropout(0.3)(x)
        
        # Output layers
        bi_rads_output = layers.Dense(
            self.num_bi_rads_classes, 
            activation='softmax', 
            name='bi_rads_classification'
        )(x)
        
        density_output = layers.Dense(
            self.num_density_classes, 
            activation='softmax', 
            name='density_classification'
        )(x)
        
        # Create model
        model = Model(
            inputs=input_layer,
            outputs=[bi_rads_output, density_output],
            name='optimized_mammography_model'
        )
        
        return model
    
    def compile_model(self, learning_rate=0.001):
        """Compiler le modèle avec les optimisations"""
        if self.model is None:
            self.model = self.create_model()
        
        # Optimizer avec learning rate scheduling
        optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
        
        # Loss functions
        bi_rads_loss = 'categorical_crossentropy'
        density_loss = 'categorical_crossentropy'
        
        # Metrics
        bi_rads_metrics = ['accuracy']
        density_metrics = ['accuracy']
        
        # Compile model
        self.model.compile(
            optimizer=optimizer,
            loss={
                'bi_rads_classification': bi_rads_loss,
                'density_classification': density_loss
            },
            loss_weights={
                'bi_rads_classification': 1.0,
                'density_classification': 0.5
            },
            metrics={
                'bi_rads_classification': bi_rads_metrics,
                'density_classification': density_metrics
            }
        )
        
        return self.model
    
    def get_callbacks(self, checkpoint_path):
        """Callbacks pour l'entraînement"""
        callbacks = [
            keras.callbacks.ModelCheckpoint(
                filepath=checkpoint_path,
                monitor='val_loss',
                save_best_only=True,
                save_weights_only=False,
                verbose=1
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            ),
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            )
        ]
        return callbacks
    
    def train(self, train_data, val_data, epochs=100, batch_size=32, checkpoint_path=None):
        """Entraîner le modèle"""
        if self.model is None:
            self.model = self.compile_model()
        
        # Callbacks
        callbacks = self.get_callbacks(checkpoint_path)
        
        # Train model
        history = self.model.fit(
            train_data,
            validation_data=val_data,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        return history
    
    def save_model(self, filepath):
        """Sauvegarder le modèle"""
        if self.model is not None:
            self.model.save(filepath)
            print(f"Modèle sauvegardé: {filepath}")
    
    def load_model(self, filepath):
        """Charger le modèle"""
        self.model = keras.models.load_model(filepath)
        print(f"Modèle chargé: {filepath}")
        return self.model
