from build123d import *
from ocp_vscode import show

with BuildPart() as b:
    Box(10, 10, 10)
    
try:
    b.part.color = Color("red")
    print("Color set successfully")
except Exception as e:
    print("Error:", e)
