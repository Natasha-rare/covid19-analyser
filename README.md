# COVID-19 Analyzer
Identify COVID-19 in photos of lungs. Built with PyQt, YOLOv5, Python3. This project was made for the Moscow Programming Olympiad final.
# Video (watch it!): https://youtu.be/Vdvi8eIfBSk
# Screenshots:
### Windows  
![Windows](https://i.imgur.com/eZYfdvW.png)  
### Mac  
![Mac](https://i.imgur.com/1CJGxiq.png)  
### Linux  
![Linux](https://i.imgur.com/s7nm2bS.png)  
# Usage:
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
Mac/Linux:
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
Linux:
``` bash
pip3 install -r linux_requirements.txt
```
### Run the app
``` bash
python3 main.py 
```
