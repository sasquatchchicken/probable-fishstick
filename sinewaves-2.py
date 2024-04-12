# Author: hector33
# Github: https://github.com/sasquatchchicken

import numpy as np
import sounddevice as sd

def generate_sine_wave(frequency, duration, sample_rate):
    """Generate sine wave samples."""
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    samples = np.sin(2 * np.pi * frequency * t)
    return samples

def normalize_samples(samples):
    """Normalize samples to fit within the range of a signed 16-bit integer."""
    max_sample = np.max(np.abs(samples))
    if max_sample == 0:
        return samples
    normalized_samples = samples / max_sample * 32767
    return normalized_samples.astype(np.int16)

def encode_samples(samples):
    """Encode samples into bytes for transmission over BLE."""
    encoded_bytes = ' '.join(['0x{:02X}'.format(sample) for sample in samples])
    return encoded_bytes

if __name__ == "__main__":
    try:
        frequency = float(input("Enter the frequency of the sine wave (Hz): "))
        duration = float(input("Enter the duration of the sine wave (seconds): "))
        sample_rate = 44100  # Use a standard sample rate (e.g., 44100 Hz)

        # Generate sine wave samples
        samples = generate_sine_wave(frequency, duration, sample_rate)

        # Normalize samples
        normalized_samples = normalize_samples(samples)

        # Play the audio at the specified sample rate
        sd.play(normalized_samples, sample_rate)
        sd.wait()

        # Encode samples
        encoded_output = encode_samples(normalized_samples)

        print("Sine wave samples generated, normalized, and encoded successfully.")
        print("Encoded samples:", encoded_output)

    except ValueError:
        print("Invalid input. Please enter numeric values.")

