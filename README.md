# Median and Cubic Spline audio filters

This project includes two audio filters, namely the median filter and the cubic spline filter. Both filters are designed to eliminate clicks in audio files and insert new values using different algorithms. Specifically:

1. The Median Filter replaces the value at the click with the median value from a set of 'n' values, which includes the click, where 'n' equals the filter_length.
2. The Cubic Spline Filter fits a smooth curve using a cubic equation for the segments between every two values, thereby inferring the value at the click.

## installation

Use the packet manager [pip](http://pip.pypa.io/en/stable/) to install
1. numpy: To run unit test for median filter and to build deteciton list for cubic spline 
2. wave: To read and write wav files
3. scipy: To apply cubic spline algorithm
4. playsound: To play restored audio
5. unittest: To test if the median filter code runs well
6. sys: To display a grogress update

```bash
pip install numpy wave scipy playsound unittest sys
```

## Usage
To use these filters, firstly you need to
1. Prepare a degraded wav file, a detection wav file and a clean wav file
2. Select one filter you prefer to use
3. If you selected median filter, you can try different values for filter length which is defined in main function but make sure you entered an odd number

```python
def main():
    # You can change the filter length
    # But filter length must be an ODD
    filter_length = 3
```

4. Go to main funciton and change the "file_path" to your own file path

```python
def main():
    # Define the file names and paths, please change to your path
    file_path = '/Users/tanqiwen/Documents/5C22-python/Assignment2/'
```

5. Run the script. For median filter you will get a median_output.wav file and for cubic spline filter you will get a spline_output.wav file
