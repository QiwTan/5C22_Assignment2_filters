'''
The function does
1. Read in a degraded sound file and a detection file
2. Easer all the clicks where detection.wav indicades
    using median filter
3. Generate a median output file

PS: 
1. Please change the file path in main function
    to your own sound file path
2. You can change filter length but it has to be an ODD
'''

import wave
import numpy as np
import unittest
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

def median_filter_restore(degraded, detectionfile, filterlength, is_wav=True):
    if filterlength % 2 == 0:
        raise ValueError("Filter length must be an odd number")
    
    if is_wav:
        # Read the degraded audio and detection file
        degraded_audio, rate = read_wav_file(degraded)
        detection_values, _ = read_wav_file(detectionfile)
    else:
        # For testing with list input (non-wav)
        degraded_audio = degraded
        detection_values = [1] * len(degraded)  # Simulate all values as errors
        rate = 1  # Dummy value for rate
    
    # Initialize the restored audio
    restored_audio = np.copy(degraded_audio)
    total_frames = len(degraded_audio)

    outsider = filterlength // 2
    filtered_list = []
    input_padding_same = np.pad(restored_audio, (outsider, outsider), 'constant', constant_values=(0, 0))
    
    # Apply the median filter
    for i in range(len(degraded_audio)):
        if detection_values[i] != 0:
            # Only apply the median filter where there's an error
            window = input_padding_same[i:i + filterlength]
            window_sorted = sorted(window)
            median_value = window_sorted[filterlength // 2]
            filtered_list.append(median_value)
        else:
            # Where there's no error, append the original audio data
            filtered_list.append(degraded_audio[i])
        
        progress = (i + 1) / total_frames * 100
        sys.stdout.write(f"\rFiltering: {progress:.2f}% complete")
        sys.stdout.flush()
    filtered_array = np.array(filtered_list, dtype=np.int16)
    return filtered_array, rate

def calculate_mse(clean, restored):
    # Compute the MSE
    clean_audio, rate = read_wav_file(clean)
    output_audio, _ = read_wav_file(restored)
    mse = np.mean((clean_audio/2 - output_audio) ** 2) / rate
    print(f"MSE: {mse}")
    return mse

# Unit tests
class TestMedianFilterWithNumpy(unittest.TestCase):
    def test_median_filter(self):
        input_list = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=np.int16)
        filter_length = 3
        restored_audio, _ = median_filter_restore(input_list, None, filter_length, is_wav=False)

        numpy_result = []
        for i in range(len(input_list)):
            start = max(0, i - filter_length // 2)
            end = min(len(input_list), i + filter_length // 2 + 1)
            window = input_list[start:end]
            numpy_result.append(int(np.median(window)))

        numpy_result = np.array(numpy_result, dtype=np.int16)
        self.assertTrue(np.array_equal(restored_audio, numpy_result))

    def test_filter_length_even(self):
        input_list = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=np.int16)
        with self.assertRaises(ValueError):
            median_filter_restore(input_list, None, 4, is_wav=False)


def main():
    # Define the file names and paths, please switch to your path
    file_path = '/Users/tanqiwen/Documents/5C22-python/Assignment2/'

    degraded_file = file_path + 'degraded.wav'
    detection_file = file_path + 'detectionfile.wav'
    clean_file = file_path + 'clean.wav'
    median_output_file = file_path + 'median_output.wav'

    # You can change the filter length
    # But filter length must be an ODD
    filter_length = 3

    # Call the median filter function
    restored_audio, rate = median_filter_restore(degraded_file, detection_file, filter_length)
    write_wav_file(median_output_file, restored_audio, rate)
    print("Done")
    mse = calculate_mse(clean_file, median_output_file)

if __name__ == "__main__":
    # run unittest
    unittest.main(exit=False)
    main()
    