from turtle import Turtle

t = Turtle()

t.screen.title("Object-oriented turtle demo")
t.screen.bgcolor("orange")
print(f"{t.screen.getshapes()=}")

print(f"{t.pos()=}")
t.screen.mainloop()
