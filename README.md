# Vintage-Tech

> Build an application for a retro technology collector. This collector likes to
collect old technology, like computers, cameras, phones etc. You will be building a small
database program so the collector can record all the items in the collection.
The collector must be able to:
> 1. Add items to the collection.
> 2. Show the items in the collection (by type).
> 3. Delete items from the collection.

>  When the program runs, it should display a menu with the options above, as well as an exit option.

## Technology Stack
- Python 3.8
- QT Creator
- IDE - Intellij

## Edit, Package and Run
### To edit the exisiting project:
- Download python [here](https://www.python.org/downloads/ "here").
- Download QT creator [here](https://www.qt.io/download "here").
- Download intellij IDE [here](https://www.jetbrains.com/idea/download/ "here")

### Package and run the application:
- Run **pip install pyinstaller**
- Package the application by running command:
**pyinstaller --onedir -w --add-data mainwindow.ui;. --add-data collectibles.json;. app.py --name VintageTech**
- Run vintageTech.exe from path *\dist\VintageTech*

# Screenshot
![image](https://user-images.githubusercontent.com/37985253/113522714-3701ba00-95a3-11eb-8c24-7a34abc93e4c.png)
