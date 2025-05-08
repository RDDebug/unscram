import random


try:
    from PIL import Image
    print("Pillow library is installed.")
except ImportError:
    print("Pillow library is NOT installed.")

try:
    from PIL import Image
    print("Pillow library is installed.")
except ImportError:
    print("Pillow library is NOT installed.")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    array_size = 40
    max_wait = 10
    waits = [0] * array_size
    wait_sum = 0
    for i, v in enumerate(waits):
        waits[i] = random.choice([100, 300, 500, 1000])
    ratio = (max_wait * 1000) / sum(waits)
    adj_waits = [int(num * ratio) for num in waits]
    x=1

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
