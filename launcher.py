import subprocess
import sys
import os
import data_controller
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def launch(screen):
    python_exe = sys.executable
    creationflags = 0
    if os.name == "nt": #If windows machine create a console and run from there.
        creationflags = subprocess.CREATE_NEW_CONSOLE
    
    subprocess.Popen([python_exe, screen], creationflags=creationflags)



if __name__ == "__main__":
    screens = ["ordering.py", "fulfilment.py", "progress.py"]
    data_controller.create_db()
    for screen in screens:
        if os.path.isfile(screen):
            launch(screen)
        else:
            raise Exception(f"Unable to launch {screen}. Ensure you have the whole project open in your explorer")
        


#The launch function and line 5 have been inspired from multiple online sources and was NOT desined by myself.