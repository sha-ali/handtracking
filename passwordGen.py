import random
import string

length = int(input("enter the length of password"))

lower = string.ascii_lowercase
upper = string.ascii_uppercase
digit = string.digits
symbol = string.punctuation

all = lower + upper + digit

temp = random.sample(all, length - 1)
temps = random.sample(symbol, 1)
temp = temp + temps

password = "".join(temp)

print(password)