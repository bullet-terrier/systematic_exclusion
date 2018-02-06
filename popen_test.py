import sys;
input("Here...");
for a in sys.argv:
    print("arg: %s type: %s"%(a,type(a)));
input("Looks like I'm %s"%(__name__))