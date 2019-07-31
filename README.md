# whistle_to_run
Trigger running of commands by whistling or playing back sounds within a frequency range

### Requirements
This system was developed and run on a Windows 7, Python 3 with only the following dependencies
sounddevice, numpy

### Installation 
1. Setup your virtual environment through conda or pipenv
```
conda create --name myvirtual_env python=3.6.9
activate myvirtual_env
```

2. Install the required packages 
```
pip install numpy sounddevice 
```
If you already have a python 3 installation and the packages above - proceed to Step 3.

3. Clone the repo and got into the directory
```
git clone https://github.com/thejasvibr/whistle_to_run.git
cd whistle_to_run
```

### Whistling your commands

1. Open a command prompt/ terminal and run the script with these settings. Start whistling and when the peak frequency of 
your whistle hits 2000 +/- 200 Hz the command will be executed. 
```
python run_cmd_on_whistle.py -fs 22050 -target 2000 -tolerance 200 -command "start echo HELLO THERE!!!"
```
This example should give you a new command prompt window with 'HELLO THERE' printed out. 

By default the target frequency is set to 1000 Hz and tolerance to 500 Hz. For the most basic version you can also just set the command and it should be enough.

2. Get creative while whistling with the commands you run - and have fun. Here is another example. This example opens a Youtube video - you must enable your browser's autoplay for it work smoothly! 
```
python run_cmd_on_whistle.py -command "cd <path to folder where your firefox.exe is> & firefox.exe -new-window <A Youtube video you'd like to watch>"
```
eg. on my system  this would
```
python run_cmd_on_whistle.py -command "cd C:\Program Files (86)\Mozilla Firefox & firefox.exe-new-window https://www.youtube.com/embed/qdtLCfEcPL4?autoplay=1"
```



