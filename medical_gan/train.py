"""Custom TensorFlow training loop for the GAN."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

import tensorflow as tf


BinaryCrossEntropy = tf.keras.losses.BinaryCrossentropy(from_logits=False)


def train_gan(
    generator: tf.keras.Model,
    discriminator: tf.keras.Model,
    dataset: tf.data.Dataset,
    latent_dim: int = 100,
    epochs: int = 15,
    learning_rate: float = 1e-4,
    snapshot_interval: int = 5,
    snapshot_callback: Optional[Callable[[tf.keras.Model, int], None]] = None,
) -> dict[str, list[float]]:
    """Train both networks and return average losses for every epoch."""
    generator_optimizer = tf.keras.optimizers.Adam(learning_rate, beta_1=0.5)
    discriminator_optimizer = tf.keras.optimizers.Adam(learning_rate, beta_1=0.5)

    @tf.function
    def train_step(real_images: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        noise = tf.random.normal([tf.shape(real_images)[0], latent_dim])
        with tf.GradientTape() as generator_tape, tf.GradientTape() as discriminator_tape:
            generated_images = generator(noise, training=True)
            real_predictions = discriminator(real_images, training=True)
            generated_predictions = discriminator(generated_images, training=True)

            discriminator_loss = BinaryCrossEntropy(tf.ones_like(real_predictions), real_predictions)
            discriminator_loss += BinaryCrossEntropy(tf.zeros_like(generated_predictions), generated_predictions)
            generator_loss = BinaryCrossEntropy(tf.ones_like(generated_predictions), generated_predictions)

        generator_gradients = generator_tape.gradient(generator_loss, generator.trainable_variables)
        discriminator_gradients = discriminator_tape.gradient(discriminator_loss, discriminator.trainable_variables)
        generator_optimizer.apply_gradients(zip(generator_gradients, generator.trainable_variables))
        discriminator_optimizer.apply_gradients(zip(discriminator_gradients, discriminator.trainable_variables))
        return generator_loss, discriminator_loss

    history = {"generator": [], "discriminator": []}
    for epoch in range(1, epochs + 1):
        generator_metric = tf.keras.metrics.Mean()
        discriminator_metric = tf.keras.metrics.Mean()
        for real_images in dataset:
            generator_loss, discriminator_loss = train_step(real_images)
            generator_metric.update_state(generator_loss)
            discriminator_metric.update_state(discriminator_loss)

        generator_value = float(generator_metric.result())
        discriminator_value = float(discriminator_metric.result())
        history["generator"].append(generator_value)
        history["discriminator"].append(discriminator_value)
        print(
            f"Epoch {epoch:02d}/{epochs} | "
            f"Generator loss: {generator_value:.4f} | "
            f"Discriminator loss: {discriminator_value:.4f}"
        )
        if snapshot_callback and (epoch % snapshot_interval == 0 or epoch == epochs):
            snapshot_callback(generator, epoch)

    return history


def save_loss_history(history: dict[str, list[float]], output_path: str | Path) -> None:
    """Save numeric loss history as a CSV file without requiring pandas."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        file.write("epoch,generator_loss,discriminator_loss\n")
        for epoch, (generator_loss, discriminator_loss) in enumerate(
            zip(history["generator"], history["discriminator"]), start=1
        ):
            file.write(f"{epoch},{generator_loss:.6f},{discriminator_loss:.6f}\n")
