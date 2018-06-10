
def solve(a, b, c):
    delta = b**2 - 4*a*c
    if delta < 0:
        print("Brak rozwiązań!")
    if delta == 0:
        x = - b / 2 * a
        print("x równa się: ", x)
    if delta > 0:
        x1 = (- b - delta ** 0.5) / 2 * a
        x2 = (- b + delta ** 0.5) / 2 * a
        print("oto rozwiązania: x1=", round(x1, 2), " i ", " x2=", round(x2,2))

def run_program():
    a = int(input('podaj a: '))
    b = int(input('podaj b: '))
    c = int(input('podaj c: '))
    solve(a, b, c)

run_program()
#1 2 1
#1 4 3