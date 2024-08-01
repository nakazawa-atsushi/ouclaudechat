import datetime
import os

s1 = 'New line 1\nNew line 2\nNew line 3\n'
s2 = 'line 4\nline 5\nline 6\n'
dt_now = datetime.datetime.now()
dt = dt_now.strftime("%Y-%m-%dT%H-%M-%S.%f")
# path = f"{dt}.txt"

with open(f"context/{dt}.txt", mode='w') as f:
    f.write(s1)
with open(f"context/{dt}.txt", mode='a') as f:
    f.write(f"{s2}こんにちは")
    f.write(s1)

with open(f"context/{dt}.txt") as f:
    # print(f.read())
    # conv_sofar = f.readlines()[-2].rstrip("\n")
    # print(conv_sofar)
    lines = f.read().splitlines()
    total = ""
    total2 = ""
    print(type(lines))
    for i in lines[:-2]:
        # print(i)
        # print(type(i))
        total += i
        
    print(total)
    print(type(total))
    
    for i in lines[-2:]:
        total2 += i
    
    print(total2)
    print(type(total2))