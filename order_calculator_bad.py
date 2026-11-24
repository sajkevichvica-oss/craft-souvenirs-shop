def calc(a, b, c, d, e):
    x = 0

    for i in a:
        x = x + i["price"] * i["quantity"]

    if b == True:
        x = x - x * 0.1

    if c == "Lviv":
        y = 50
    elif c == "Ukraine":
        y = 80
    else:
        y = 150

    if x > 1500:
        y = 0

    if d == "card":
        z = x + y
    elif d == "cash":
        z = x + y
    else:
        z = x + y

    if e != "":
        if e == "CRAFT10":
            z = z - z * 0.1
        elif e == "SAVE50":
            z = z - 50

    print("sum:", x)
    print("delivery:", y)
    print("total:", z)

    return z


items = [
    {
        "name": "Керамічна чашка",
        "price": 350,
        "quantity": 2
    },
    {
        "name": "Ароматична свічка",
        "price": 280,
        "quantity": 1
    }
]

result = calc(
    items,
    True,
    "Lviv",
    "card",
    "CRAFT10"
)

print(result)