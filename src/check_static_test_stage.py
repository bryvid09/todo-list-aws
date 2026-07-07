import os
import sys

password = "admin123"

def suma( a,b ):
    resultado=eval("a+b")
    os.system("echo " + str(resultado))
    return resultado