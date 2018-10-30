import math
import sys
a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])

discriminant = b * b - 4 * a * c
root_a = (-b + math.sqrt(discriminant)) / 2 * a
root_b = (-b - math.sqrt(discriminant)) / 2 * a

print(int(root_a))
print(int(root_b))
