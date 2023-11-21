'''
The function does
1. Read in a degraded sound file and a detection file
2. Easer all the clicks where detection.wav indicades
    using cubic spline filter
3. Generate a spline output file
4. Play degraded.wav and restored.wav

PS: Please change the file path in main function
    to your own sound file path
'''

import wave
import numpy as np
from scipy.interpolate import CubicSpline
from playsound import playsound
import time
import sys

def read_wav_file(filename):
    # Open the WAV file
    with wave.open(filename, 'rb') as wav_file:
        sample_rate = wav_file.getframerate()
        n_frames = wav_file.getnframes()
        audio_data = np.frombuffer(wav_file.readframes(n_frames), dtype=np.int16)
    return audio_data, sample_rate

def write_wav_file(filename, data, sample_rate):
    # Save the data to a WAV file
    with wave.open(filename, 'wb') as wav_file:
        n_channels = 1
        sample_width = 2
        wav_file.setparams((n_channels, sample_width, sample_rate, len(data), 'NONE', 'not compressed'))
        wav_file.writeframes(data.tobytes())

def cubic_spline_restore(degraded, detection_file):
    # Read the degraded audio and detection file
    degraded_audio, rate = read_wav_file(degraded)
    detection_values, _ = read_wav_file(detection_file)

    # Identify errors
    error_indices = np.where(detection_values != 0)[0]
    valid_indices = np.where(detection_values == 0)[0]
    
    # Interpolate using cubic splines
    cs = CubicSpline(valid_indices, degraded_audio[valid_indices])
    restored_audio = np.copy(degraded_audio)
    restored_audio[error_indices] = cs(error_indices)

    total_errors = len(error_indices)
    print("Starting restoration process...")
    for i, index in enumerate(error_indices):
        # Update the restored audio at the error index
        restored_audio[index] = cs(index)
        
        # Calculate and print progress
        progress = (i + 1) / total_errors * 100
        sys.stdout.write(f"\rFiltering: {progress:.2f}% complete")
        sys.stdout.flush()    
    print("\nRestoration process completed.")
    
    return restored_audio.astype(np.int16), rate

def calculate_mse(clean, restored):
    # Compute the MSE
    clean_audio, rate = read_wav_file(clean)
    output_audio, _ = read_wav_file(restored)
    mse = np.mean((clean_audio/2 - output_audio) ** 2) / rate
    print(f"MSE: {mse}")
    return mse

def main():
    # Define the file names and paths, please change to your path
    file_path = '/Users/tanqiwen/Documents/5C22-python/Assignment2/'
    degraded_file = file_path + 'degraded.wav'
    detection_file = file_path + 'detectionfile.wav'
    clean_file = file_path + 'clean.wav'
    spline_output_file = file_path + 'spline_output.wav'

    # Call the cubic_spline_restore function
    restored_audio, rate = cubic_spline_restore(degraded_file, detection_file)
    write_wav_file(spline_output_file, restored_audio, rate)

    mse = calculate_mse(clean_file, spline_output_file)

    # Play the original and restored audio files
    playsound(file_path + 'degraded.wav')
    playsound(file_path + 'spline_output.wav')

    print('Done')

if __name__ == "__main__":
    main()
