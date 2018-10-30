import sys

num_steps = int(sys.argv[1])

#for step in range(num_steps):
#    print(" " * (num_steps - step - 1), "#" * (step + 1), sep="")


for step in range(1, num_steps + 1):
    print(('#' * i).rjust(num_steps, ' '))
