# COVID-19 Analyzer
## Usage:
### Download the app  

### Open it in Terminal (or command line)  

### Create virtual environment:
``` bash
python3 -m venv venv
```
### Activate virtual environment
Windows:
``` bash
venv\Scripts\activate
```
Mac:
``` bash
source venv/bin/activate
```
### Install modules:
Windows:
``` bash
pip3 install -r win_requirements.txt
```
``` bash
python -m pip3 install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio===0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
```
Mac:
``` bash
pip3 install -r mac_requirements.txt
```
### Run the app
``` bash
python3 main.py 
```
