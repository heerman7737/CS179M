def partition(arr):

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
