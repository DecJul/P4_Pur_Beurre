categories = ["ciyciy", "ouiokj", "oijoijo"]
answer = input(">>>")

try:
    answer = int(answer) - 1
    category = categories[int(answer)]
    print(category)
except (ValueError, IndexError):
    print(answer)
