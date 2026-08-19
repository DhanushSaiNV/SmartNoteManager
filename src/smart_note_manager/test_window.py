from .window import Window

l = [1,2,3,4,5]

w = Window(1, 0,1,l, size=3)

print(w)
print()
print(w.size)
print()

w.forward()
print(w)

print()

w.forward()
print(w)

print() 

w.forward()
print(w)

print()

w.forward()
print(w)

print()

w.forward()
print(w)

print()

w.forward()
print(w)

print("\nbackwards\n")

w.backward()
print(w)

print()

w.backward()
print(w)

print()

w.backward()
print(w)

print()

w.backward()
print(w)

print()

w.backward()
print(w)
