"""Visualization and image-export helpers for the GAN project."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf


def show_original_images(images: np.ndarray, count: int = 16) -> None:
    """Display a grid of real MNIST examples."""
    _plot_grid(images[:count], title="Original MNIST images", value_range=(-1, 1))


def generate_image_grid(
    generator: tf.keras.Model,
    latent_dim: int,
    epoch: int,
    output_path: Optional[Union[str, Path]] = None,
    count: int = 16,
    seed: int = 42,
) -> np.ndarray:
    """Generate and display/save a deterministic grid of images."""
    rng = tf.random.Generator.from_seed(seed + epoch)
    noise = rng.normal([count, latent_dim])
    images = generator(noise, training=False).numpy()
    _plot_grid(
        images,
        title=f"Generated images after epoch {epoch}",
        value_range=(-1, 1),
        output_path=output_path,
    )
    return images


def compare_original_and_generated(
    original_images: np.ndarray,
    generated_images: np.ndarray,
    count: int = 8,
) -> None:
    """Display real and synthetic examples in two aligned rows."""
    figure, axes = plt.subplots(2, count, figsize=(1.6 * count, 3.5))
    figure.suptitle("Original MNIST vs generated demonstration images")
    for index in range(count):
        axes[0, index].imshow(_to_display(original_images[index]), cmap="gray")
        axes[0, index].axis("off")
        axes[1, index].imshow(_to_display(generated_images[index]), cmap="gray")
        axes[1, index].axis("off")
    axes[0, 0].set_ylabel("Original", rotation=0, labelpad=35, va="center")
    axes[1, 0].set_ylabel("Generated", rotation=0, labelpad=35, va="center")
    figure.tight_layout()
    plt.show()


def plot_losses(history: dict[str, list[float]]) -> None:
    """Plot generator and discriminator losses over epochs."""
    figure, axis = plt.subplots(figsize=(9, 4.5))
    axis.plot(history["generator"], label="Generator loss", linewidth=2)
    axis.plot(history["discriminator"], label="Discriminator loss", linewidth=2)
    axis.set_title("GAN training losses")
    axis.set_xlabel("Epoch")
    axis.set_ylabel("Binary cross-entropy loss")
    axis.grid(alpha=0.25)
    axis.legend()
    figure.tight_layout()
    plt.show()


def save_synthetic_images(images: np.ndarray, output_dir: str | Path) -> None:
    """Save images in a uint8 PNG format for easy inspection."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    for index, image in enumerate(images):
        plt.imsave(output_path / f"synthetic_{index + 1:04d}.png", _to_display(image), cmap="gray", vmin=0, vmax=1)


def _plot_grid(
    images: np.ndarray,
    title: str,
    value_range: tuple[float, float],
    output_path: Optional[Union[str, Path]] = None,
) -> None:
    columns = 4
    rows = int(np.ceil(len(images) / columns))
    figure, axes = plt.subplots(rows, columns, figsize=(8, 2 * rows))
    axes = np.atleast_1d(axes).ravel()
    for axis, image in zip(axes, images):
        axis.imshow(_to_display(image, value_range), cmap="gray")
        axis.axis("off")
    for axis in axes[len(images):]:
        axis.axis("off")
    figure.suptitle(title)
    figure.tight_layout()
    if output_path is not None:
        figure.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.show()
    plt.close(figure)


def _to_display(image: np.ndarray, value_range: tuple[float, float] = (-1, 1)) -> np.ndarray:
    """Convert either normalized GAN output or uint8 data to [0, 1]."""
    image = np.asarray(image).squeeze()
    low, high = value_range
    if low < 0:
        image = (image - low) / (high - low)
    return np.clip(image, 0, 1)
