# Medical Data Augmentation using GAN for Synthetic Medical Images

## Important dataset note

This project uses the **MNIST handwritten-digit dataset only as a safe demonstration dataset**. MNIST images are not medical images, and the outputs from this project must not be described as medical images or used for clinical decisions.

The GAN architecture is a beginner-friendly example of a pipeline that can later be adapted to properly governed medical datasets such as chest X-rays, MRI scans, CT scans, or histopathology images. Medical use requires expert review, privacy controls, validation, and approval from the relevant institution or ethics process.

## What the project demonstrates

- Loading and normalizing MNIST images from `[0, 255]` to `[-1, 1]`.
- A convolutional Generator that maps a random latent vector to a `28 x 28 x 1` image.
- A convolutional Discriminator that returns a real/fake probability.
- Binary cross-entropy loss, Adam optimization, and a custom TensorFlow training loop.
- Training progress, generated-image snapshots, original/generated comparisons, and loss curves.
- Creation of at least 100 final synthetic images in a NumPy array, with optional PNG export.

## Project structure

```text
medical_gan/
|-- main.py                 # End-to-end entry point
|-- generator.py            # Generator model
|-- discriminator.py        # Discriminator model
|-- train.py                # Custom training loop and loss CSV export
|-- visualize.py            # Image grids, comparisons, plots, and PNG export
|-- requirements.txt
|-- README.md
`-- generated_images/       # Snapshots and final PNG files are written here
```

## Local setup

Python 3.10 or newer is recommended.

```bash
cd medical_gan
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py --epochs 15 --num-synthetic 100 --save-images
```

The default 15 epochs is suitable for a practical demonstration. Reduce it to `--epochs 2` or `--epochs 5` for a quick smoke run. A GPU is used automatically by TensorFlow when one is available; the same code runs on CPU.

The program prints both model summaries and epoch losses. It displays:

1. Original MNIST examples.
2. Generated grids at every fifth epoch and at the final epoch.
3. Generator and discriminator loss curves.
4. An original-versus-generated comparison.
5. The number of generated images.

With `--save-images`, the final PNG files, snapshots, and `loss_history.csv` are written to `generated_images/`.

## Google Colab

1. Upload the `medical_gan` folder to Colab or clone/copy the files into the notebook working directory.
2. Run:

```python
%cd /content/medical_gan
!pip install -r requirements.txt
!python main.py --epochs 15 --num-synthetic 100 --save-images
```

Colab's runtime menu can be used to enable a GPU. The first run downloads MNIST automatically through `tensorflow.keras.datasets`.

## Architecture

### Generator

`latent vector (100)` -> `Dense` -> `BatchNormalization` -> `LeakyReLU` -> `Reshape (7 x 7)` -> `Conv2DTranspose` upsampling layers -> `tanh` output `(28, 28, 1)`.

The `tanh` output matches the input normalization range `[-1, 1]`.

### Discriminator

`(28, 28, 1)` -> `Conv2D` -> `LeakyReLU` -> `Dropout` -> `Conv2D` -> `LeakyReLU` -> `Dropout` -> `Flatten` -> `sigmoid probability`.

During each training step, the Discriminator learns to classify real MNIST images as 1 and generated images as 0. The Generator learns from the Discriminator's feedback and tries to make generated images classify as 1.

## Medical data augmentation adaptation

A responsible medical imaging adaptation would follow this sequence:

1. Obtain real patient images under appropriate consent, governance, de-identification, and access controls.
2. Preprocess them consistently: resize or crop, normalize intensity, remove unsuitable records, and preserve clinically important metadata.
3. Train a GAN using the target image dimensions and domain-specific validation splits.
4. Generate candidate synthetic images.
5. Quality-check the candidates with imaging experts and automated measures. Check realism, diversity, labels, and downstream diagnostic performance.
6. Combine synthetic and real images only after validation, and evaluate the diagnostic model on a separate real patient test set.

Synthetic images should **not automatically be treated as clinically valid data**. Important risks include:

- **Mode collapse:** the Generator produces a small set of similar images and loses diversity.
- **Artifacts:** generated structures may look plausible but be anatomically incorrect.
- **Privacy leakage:** a model can memorize or reproduce identifiable training examples.
- **Distribution mismatch:** synthetic images may not represent scanners, populations, diseases, or acquisition settings found in deployment.
- **Synthetic bias:** existing under-representation or labeling errors can be amplified.

## Viva Explanation

### What is a GAN?

A Generative Adversarial Network is a pair of neural networks trained together: a Generator creates examples and a Discriminator judges whether examples are real or generated.

### What is a Generator?

The Generator takes a random latent vector, which is a compact vector of random numbers, and transforms it into a new image.

### What is a Discriminator?

The Discriminator is a binary classifier. It outputs a probability describing whether an input image appears to come from the real training dataset.

### How does GAN training work?

The Discriminator learns from real images labeled real and generated images labeled fake. The Generator is then updated so that its images are more likely to be classified as real. These two objectives compete and improve each other over many steps.

### What is synthetic data?

Synthetic data is artificially generated data that imitates patterns in real data without being a direct new observation from a patient or other real-world subject.

### Why is synthetic medical data useful?

It may help explore data augmentation, increase representation of rare classes, support software testing, and reduce the need to share some real patient images. It still needs validation before it is used for a medical purpose.

### What is mode collapse?

Mode collapse happens when the Generator learns to produce only a few repeated patterns instead of diverse examples from the full data distribution.

### What are the limitations of GAN-generated medical images?

They can contain subtle artifacts, incorrect anatomy, label errors, privacy leakage, bias, and distribution mismatch. Visual realism alone does not prove clinical validity.

### How can this system help when real patient data is limited?

After governance and quality checks, validated synthetic examples can supplement real training data. The diagnostic model must still be evaluated on independent, real patient data, and clinical experts should review the process.

## Practical interpretation of the loss curves

The curves are diagnostic signals, not a scorecard where one loss must reach zero. If the Discriminator becomes too strong, the Generator may receive weak learning feedback. Unstable oscillations can indicate training imbalance. Losses should be interpreted together with image quality, diversity, and downstream evaluation.
