import sys
import subprocess


MODULES_PATH = "pymodules"
def install_if_missing(*modules):
    sys.path.append(MODULES_PATH)
    installed = installed_modules()
    missing = list(set(modules) - set(installed))
    if missing:
        print("Installing modules: " +  ", ".join(missing))
        subprocess.check_call(['pip', 'install', '--target=' + MODULES_PATH, *missing])
        print("Installed modules: " +  ", ".join(missing))
    else:
        print("All modules are up to date!")

def installed_modules():
    output = subprocess.check_output(["pip", "freeze", "--path=" + MODULES_PATH])
    lines = output.decode().rsplit()
    modules = [line.split("==")[0] for line in lines]
    return modules