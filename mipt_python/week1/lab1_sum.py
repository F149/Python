import sys

digit_string = sys.argv[1]

#sum = 0
#if digit_string.isdigit:
#    for digit in digit_string:
#        sum += int(digit)
#print (sum)

print (sum([int(num) for num in digit_string if num.isdigit()]))
