import sys
from array import array

lst = [3,5,6]
llst = array("i", lst)
total_size = 0
print("list: ", sys.getsizeof(llst))

for item in llst:
    size = sys.getsizeof(item)
    print(item, ":", size)
    total_size += size

print("total: ", sys.getsizeof(lst) - sys.getsizeof([]))