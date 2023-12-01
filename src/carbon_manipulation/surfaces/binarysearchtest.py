[1,2,3,4,5,6]
[0,1,2,3,4,5]

target = 3.3

low = 0
high = 5
mid = (low + high) // 2


def radmatch(target, list):
    low = 0
    high = len(list) - 1
    mid = (low + high) //2
    
    target 