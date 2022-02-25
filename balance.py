def partition(arr):

    arr.sort(reverse=True)
    sum1 = 0
    sum2 = 0 
    l1 =[]
    l2 =[]
    for i in range(len(arr)):
        if sum1 <=sum2:
            sum1+=arr[i]
            l1.append(arr[i])
        else:
            sum2+=arr[i]
            l2.append(arr[i])
    return l1,l2

def select(ar, i, target):

    if i >= len(ar): return []

    
    l1 = select(ar,i+1,target  -ar[i])
    l1.append(ar[i])

    l2 = select(ar,i+1,target)

    t1 = sum(l1) 	
    t2 = sum(l2)

    if abs(t1 - target) < abs(t2 -target):
        return l1

    else:
        return l2
    
    
a =[9041,10001,500,600,100,10]
print(f'here: {partition(a)}')