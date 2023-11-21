# Median and Cubic Spline audio filters

这个项目中包含两个audio filters，分别为median filter和cubic spline filter，这两个filters都会过滤音频文件中的clicks并分别利用不同的算法插入新的值，其中
1. Median Filter会将原本click处的值替换为包含click在内的n个值中的中值，且n = filter_length
2. Cubic Spline Filter会为每两个值的中间部分用三次方程拟合一段平滑曲线，以此推断click处的值

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