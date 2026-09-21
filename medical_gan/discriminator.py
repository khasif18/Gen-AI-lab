"""Discriminator model for the MNIST GAN demonstration."""

from __future__ import annotations

import tensorflow as tf
from tensorflow.keras import layers, Sequential


def create_discriminator() -> tf.keras.Model:
    """Create a discriminator that returns the probability that an image is real."""
    model = Sequential(
        [
            layers.Input(shape=(28, 28, 1), name="image"),
            layers.Conv2D(64, 5, strides=2, padding="same"),
            layers.LeakyReLU(),
            layers.Dropout(0.3),
            layers.Conv2D(128, 5, strides=2, padding="same"),
            layers.LeakyReLU(),
            layers.Dropout(0.3),
            layers.Flatten(),
            layers.Dense(1, activation="sigmoid", name="real_probability"),
        ],
        name="discriminator",
    )
    return model
