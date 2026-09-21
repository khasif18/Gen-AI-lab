"""Run the complete Medical Data Augmentation GAN demonstration.

MNIST is used only as a safe, non-medical demonstration dataset. The same
architecture can be adapted to appropriately prepared medical image data.
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import mnist

from discriminator import create_discriminator
from generator import create_generator
from train import save_loss_history, train_gan
from visualize import (
    compare_original_and_generated,
    generate_image_grid,
    plot_losses,
    save_synthetic_images,
    show_original_images,
)


SEED = 42


def set_reproducible_seeds(seed: int = SEED) -> None:
    """Set seeds for Python, NumPy, and TensorFlow where supported."""
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)


def load_mnist_dataset(batch_size: int = 128) -> tuple[np.ndarray, tf.data.Dataset]:
    """Load MNIST and normalize grayscale pixels from [0, 255] to [-1, 1]."""
    (images, _), _ = mnist.load_data()
    images = images.astype("float32")
    images = (images - 127.5) / 127.5
    images = np.expand_dims(images, axis=-1)
    dataset = (
        tf.data.Dataset.from_tensor_slices(images)
        .shuffle(len(images), seed=SEED, reshuffle_each_iteration=True)
        .batch(batch_size, drop_remainder=True)
        .prefetch(tf.data.AUTOTUNE)
    )
    return images, dataset


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a GAN on MNIST as a safe image-generation demo.")
    parser.add_argument("--epochs", type=int, default=15, help="Training epochs; 15 is practical for Colab/laptops.")
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--latent-dim", type=int, default=100)
    parser.add_argument("--num-synthetic", type=int, default=100)
    parser.add_argument("--output-dir", type=Path, default=Path("generated_images"))
    parser.add_argument("--save-images", action="store_true", help="Save the final synthetic images as PNG files.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    set_reproducible_seeds()
    print(f"TensorFlow version: {tf.__version__}")
    print(f"Available GPUs: {len(tf.config.list_physical_devices('GPU'))}")

    original_images, dataset = load_mnist_dataset(args.batch_size)
    show_original_images(original_images)

    generator = create_generator(args.latent_dim)
    discriminator = create_discriminator()
    print("\nGenerator architecture:")
    generator.summary()
    print("\nDiscriminator architecture:")
    discriminator.summary()

    snapshot_dir = args.output_dir / "training_snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    def snapshot_callback(current_generator: tf.keras.Model, epoch: int) -> None:
        generate_image_grid(
            current_generator,
            args.latent_dim,
            epoch,
            output_path=snapshot_dir / f"epoch_{epoch:03d}.png",
        )

    history = train_gan(
        generator,
        discriminator,
        dataset,
        latent_dim=args.latent_dim,
        epochs=args.epochs,
        snapshot_callback=snapshot_callback,
    )
    save_loss_history(history, args.output_dir / "loss_history.csv")
    plot_losses(history)

    final_noise = tf.random.normal([args.num_synthetic, args.latent_dim], seed=SEED)
    synthetic_images = generator(final_noise, training=False).numpy()
    print(f"\nNumber of synthetic images generated: {len(synthetic_images)}")
    compare_original_and_generated(original_images, synthetic_images)
    generate_image_grid(generator, args.latent_dim, args.epochs, output_path=args.output_dir / "final_grid.png")
    if args.save_images:
        save_synthetic_images(synthetic_images, args.output_dir)
        print(f"PNG files saved to: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
