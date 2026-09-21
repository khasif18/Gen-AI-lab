"""Generator model for the MNIST GAN demonstration."""

from __future__ import annotations

import tensorflow as tf
from tensorflow.keras import layers, Sequential


def create_generator(latent_dim: int = 100) -> tf.keras.Model:
    """Create a generator that maps a latent vector to a 28x28 grayscale image."""
    model = Sequential(name="generator")
    model.add(layers.Input(shape=(latent_dim,), name="latent_vector"))
    model.add(layers.Dense(7 * 7 * 256, use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())
    model.add(layers.Reshape((7, 7, 256)))

    model.add(layers.Conv2DTranspose(128, 5, strides=1, padding="same", use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())
    model.add(layers.Conv2DTranspose(64, 5, strides=2, padding="same", use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())
    model.add(layers.Conv2DTranspose(1, 5, strides=2, padding="same", activation="tanh"))
    return model
