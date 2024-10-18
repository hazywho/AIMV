import math
add = 0
for i in range(180,360):
    v = math.sin(math.radians(i))
    print(v)
    add+=v
    
print(add)
