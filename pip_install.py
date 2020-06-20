import os
libs = {"pyecharts"}
try:
  for lib in libs:
   os.system("pip install -i  https://pypi.mirrors.ustc.edu.cn/simple/ " + lib)
  print("Successful")
except:
  print("Failed Somehow")
