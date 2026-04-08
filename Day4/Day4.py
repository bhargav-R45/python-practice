# 1. Palindrome Check
num = int(input("Enter a number: "))
temp = num
rev = 0

while num > 0:
    digit = num % 10
    rev = rev * 10 + digit
    num //= 10

if temp == rev:
    print("Palindrome")
else:
    print("Not Palindrome")

# 2. Sum of Digits
num = int(input("Enter a number: "))
sum = 0

while num > 0:
    digit = num % 10
    sum += digit
    num //= 10

print("Sum of digits:", sum)

# 3. Even or Odd
num = int(input("Enter a number: "))

if num % 2 == 0:
    print("Even")
else:
    print("Odd")
