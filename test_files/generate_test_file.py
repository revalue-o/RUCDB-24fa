import os
os.chdir(os.path.dirname(__file__))
for i in range(10):
    with open(str(i)+".txt", "w") as f:
        f.write("test file"+str(i))