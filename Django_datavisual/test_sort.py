def partition(arr,low,high): 
    i = ( low-1 )         # 最小元素索引
    pivot = arr[high]     
  
    for j in range(low , high): 
  
        # 当前元素小于或等于 pivot 
        if   arr[j] <= pivot: 
          
            i = i+1 
            
            arr[i],arr[j] = arr[j],arr[i]
            arr_str[i],arr_str[j] = arr_str[j],arr_str[i] 
  
    arr[i+1],arr[high] = arr[high],arr[i+1] 
    arr_str[i+1],arr_str[high] = arr_str[high],arr_str[i+1] 
    
    return ( i+1 ) 
  
 

def quickSort(arr,low,high): 
    if low < high: 
        print(arr,low,high)

        pi = partition(arr,low,high) 
  
        quickSort(arr, low, pi-1) 
        quickSort(arr, pi+1, high) 
    
  
  
ar = [3, 7, 8, 9, 5, 1] 
arr_str = ["c","g","h","i","e","a"]
arr_url = ["c","g","h","i","e","a"]
n = len(ar) 
#quickSort(ar,0,n-1)
#print ("after:") 

 
#print (ar)


# 返回 x 在 arr 中的索引，如果不存在返回 -1
def binarySearch (arr, l, r, x): 
  
    # 基本判断
    if r >= l: 
  
        mid = int(l + (r - l)/2)
  
        # 元素整好的中间位置
        if arr[mid] == x: 
            return mid 
          
        # 元素小于中间位置的元素，只需要再比较左边的元素
        elif arr[mid] > x: 
            return binarySearch(arr, l, mid-1, x) 
  
        # 元素大于中间位置的元素，只需要再比较右边的元素
        else: 
            return binarySearch(arr, mid+1, r, x) 
  
    else: 
        # 不存在
        return -1
  
# 测试数组
arr = [ 18,21,26,29,34,41,59,60,72,81,89] 
x = 35
  
# 函数调用
result = binarySearch(arr, 0, len(arr)-1, x) 
  
if result != -1: 
    print ("元素在数组中的索引为 %d" % result )
else: 
    print ("元素不在数组中")