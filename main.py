# Author by TinhNT

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def check_input(number):
    if isinstance(number, (int, float)) is True:
        print("is number")
        if number%2==0:
            return 2*number
        elif number%3==0:
            return 3*number
        else:
            return 5*number
    else:
        return "is string"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(check_input(2.2))
