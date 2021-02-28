# dsp-ip-homework1
# For computers that support with CUDA
## Installation
```bash
pip install -r requirements.txt 
```

## Usage

1) data acquisition using Bing API
   ```python
   python3 search-bing-api.py --query "dog" --output dataset/dog
   python3 search-bing-api.py --query "cat" --output dataset/cat
   ```

2) Automated data cleaning using Rekognition:
   ```python
   # change the flag in line 127 to True
   upload_file_switch = True
   python3 dataHandler.py
   ```
3) download the data after rekognition
   ```python
   # change the flag in line 153 to True
   download_data_switch =True
   python3 alexTrainer.py
   ```
   
3) Create a model 
   ```python
   python3 alexTrainer.py
   ```

4) Create and Inference server using Flask
   ```python
   download_data_switch = False
   python3 predictor.py
   ```
## License
[MIT](https://choosealicense.com/licenses/mit/)
