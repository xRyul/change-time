
![Alt text](./images/Example1.gif)

---

Incrimentally change date/time of all files in all subfolders. 

Changes File Modification Date, Date/Time Digitized, XMP: Metadata Date/time, XMP: Modification Date/time, EXIF: MOdification date/time.

It doesn't change **Date Taken**. 

# How to
Incrementation is calcualted based on subfolders. Thus, for it to wrok, following subfolders must be created: `12, 13, 15, 20, 22, 24, 36`. 

## Install Python
1. Create new folder on the Desktop: "/change-time"
2. Download Python3.11.4 from www.python.org and put it into `/change-time`
3. Run the Python installer > Custom > install into `/change-time/python3.11`. Uncheck anything that sets PATH variables.
4. Create Virtual Environment. Open Terminal: `cd ~/Desktop/change-time/` and run ` C:\Users\[USERNAME]\Desktop\change-time\py3.11\python -m venv my_env`. my_env can be changed to any other name. 
5. Activate the environment. `my_env\scripts\activate`

## Install packages
```
pip install PyExifTool pyqt5
```

### Optional
Create an .exe executable with all packages inside. 
```
pip install pyinstaller
pyinstaller --onefile --noconsole .\Change_time.py
```

This will create a dist subfolder with compiled executable file which can be easily copy/pasted and shared. 
