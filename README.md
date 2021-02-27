# dsp-ip-homework1

## Installation
```bash
pip install -r requirements.txt 
```

## Usage

1) data acquisition using Bing API.
   ```python
   python3 search-bing-api.py --query "dog" --output dataset/dog
   python3 search-bing-api.py --query "cat" --output dataset/cat
   ```

2) Automated data cleaning using Rekognition
   ```python
   python3 upload_file.py
   python3 checkAndDownload.py
   ```
   
3) Create a model 
   ```python
   python3 createModel.py
   ```

4) Create and Inference server using Flask
   ```python
   python3 deploymentUsingFlask.py
   ```
## License
[MIT](https://choosealicense.com/licenses/mit/)
