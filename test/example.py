import time

def f():
    print("Trust me, you really want to step into me!!!")
    with open("/tmp/secret", 'wb') as f:
        f.write('muhahaha, you have discovered my secret lair!')
    return

TIME = 20
for i in reversed(range(TIME)):
    time.sleep(i)
    print(f"Have to wait {i:2d} seconds longer, hope you don't mess up debugging me after :P")

f()
print("I hope you saw the secrets inside f()! No going back now.")

