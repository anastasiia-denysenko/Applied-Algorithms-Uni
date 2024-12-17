import random
import time
import math
import matplotlib.pyplot as plt
import sys
sys.setrecursionlimit(30000)

#-----------------------------
#           HOARE
#-----------------------------

def parts_for_hoare(lst:list, left, right):
    # pivot is the first element
    pivot = lst[left]
    i = left - 1
    j = right + 1
    while True:
        i += 1
        while lst[i] < pivot:
            i += 1
        j -= 1
        while lst[j] > pivot:
            j -= 1
        if i >= j:
            return j
        lst[i], lst[j] = lst[j], lst[i]
def quick_sort_hoare(lst:list, left, right):
    if left < right:
        part = parts_for_hoare(lst, left, right)
        quick_sort_hoare(lst, left, part)
        quick_sort_hoare(lst, part+1, right)
"""
l = [1, 5, 2, 8, 4, 0, 4]
quick_sort_hoare(l, 0, len(l)-1)
print(l)
"""
#-----------------------------
#          LOMUTO
#-----------------------------


def parts_for_lomuto(lst:list, left, right):
    # pivot is the last element
    pivot = lst[right]
    i = left - 1
    for j in range(left, right):
        if lst[j] <= pivot:
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
    lst[i+1], lst[right] = lst[right], lst[i+1]
    return i+1
def quick_sort_lomuto(lst:list, left, right):
    if left < right:
        part = parts_for_lomuto(lst, left, right)
        quick_sort_lomuto(lst, left, part - 1)
        quick_sort_lomuto(lst, part + 1, right)
"""
l = [1, 5, 2, 8, 4, 0, 4]
quick_sort_lomuto(l, 0, len(l)-1)
print(l)
"""
#-----------------------------
#        MIDDLE PIVOT
#-----------------------------

def parts_for_middle(lst:list, left, right):
    pivot = left
    i = left + 1
    for j in range(left+1, right+1):
        if lst[j] <= lst[pivot]:
            lst[i] , lst[j] = lst[j] , lst[i]
            i = i + 1
    lst[pivot], lst[i - 1] = lst[i - 1], lst[pivot]
    pivot = i - 1
    return pivot

def middle_partition(lst:list, left, right):
    middle_pivot = (left + right)//2
    lst[left], lst[middle_pivot] = lst[middle_pivot], lst[left]
    return parts_for_middle(lst, left, right)

def quicksort_middle_pivot(lst:list, left , right):
    if left < right:
        index_pivot = middle_partition(lst, left, right)
        quicksort_middle_pivot(lst, left, index_pivot - 1)
        quicksort_middle_pivot(lst, index_pivot + 1, right)

'''
l = [1, 5, 2, 8, 4, 0, 4]
quicksort_middle_pivot(l, 0, len(l)-1)
print(l)
'''

#-----------------------------
#        RANDOM PIVOT
#-----------------------------

def parts_for_random(lst:list, left, right):
    pivot = left
    i = left + 1
    for j in range(left+1, right+1):
        if lst[j] <= lst[pivot]:
            lst[i] , lst[j] = lst[j] , lst[i]
            i = i + 1
    lst[pivot], lst[i - 1] = lst[i - 1], lst[pivot]
    pivot = i - 1
    return pivot

def random_partition(lst:list, left, right):
    random_pivot = random.randrange(left, right)
    lst[left], lst[random_pivot] = lst[random_pivot], lst[left]
    return parts_for_random(lst, left, right)

def quicksort_random_pivot(lst:list, left , right):
    if left < right:
        index_pivot = random_partition(lst, left, right)
        quicksort_random_pivot(lst, left, index_pivot - 1)
        quicksort_random_pivot(lst, index_pivot + 1, right)
'''
l = [1, 5, 2, 8, 4, 0, 4]
quicksort_random_pivot(l, 0, len(l)-1)
print(l)
'''
#------------------------------
#     MEDIAN OF THREE PIVOT
#------------------------------

def get_median(a, b, c):
    lst = [a, b, c]
    mn = min(lst)
    mx = max(lst)
    lst.remove(mn)
    lst.remove(mx)
    return lst[0]

def patrs_for_three(lst:list, left, right):
    a = lst[left]
    b = lst[right]
    c = lst[(left+right)//2]
    median = get_median(a, b, c)
    index_pivot = lst.index(median)
    lst[left], lst[index_pivot] = lst[index_pivot], lst[left]
    pivot = lst[left]
    i = left
    for j in range(left + 1, right + 1):
        if (lst[j] < pivot):
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
    lst[i], lst[left] = lst[left], lst[i]
    return i

def quick_sort_three(lst, left, right):
    if left < right:
        m = patrs_for_three(lst, left, right)
        quick_sort_three(lst, left, m - 1)
        quick_sort_three(lst, m + 1, right)
    return lst

'''
l = [2, 6, 3, 8, 1, 0]
quick_sort_three(l, 0, len(l)-1)
print(l)
'''

#------------------------------
# MEDIAN OF THREE RANDOM PIVOT
#------------------------------

def get_median_random(a, b, c):
    lst = [a, b, c]
    mn = min(lst)
    mx = max(lst)
    lst.remove(mn)
    lst.remove(mx)
    return lst[0]

def patrs_for_three_random(lst:list, left, right):
    a = lst[random.randint(left, right)]
    b = lst[random.randint(left, right)]
    c = lst[random.randint(left, right)]
    median = get_median_random(a, b, c)
    index_pivot = lst.index(median)
    lst[left], lst[index_pivot] = lst[index_pivot], lst[left]
    pivot = lst[left]
    i = left
    for j in range(left + 1, right + 1):
        if (lst[j] < pivot):
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
    lst[i], lst[left] = lst[left], lst[i]
    return i

def quick_sort_three_random(lst, left, right):
    if left < right:
        m = patrs_for_three_random(lst, left, right)
        quick_sort_three_random(lst, left, m - 1)
        quick_sort_three_random(lst, m + 1, right)
    return lst

'''
l = [1, 5, 2, 8, 4, 0, 4]
quick_sort_three_random(l, 0, len(l)-1)
print(l)
'''

#------------------------------
#         TWO PIVOTS
#------------------------------

def parts_for_quick_sort_two(lst:list, left, right):
    if lst[left] > lst[right]:
        lst[left], lst[right] = lst[right], lst[left]
    i = j = left + 1
    k, l, m = right - 1, lst[left], lst[right]
    while j <= k:
        if lst[j] < l:
            lst[j], lst[i] = lst[i], lst[j]
            i += 1
        elif lst[j] >= m:
            while lst[k] > m and j < k:
                k -= 1   
            lst[j], lst[k] = lst[k], lst[j]
            k -= 1
            if lst[j] < l:
                lst[j], lst[i] = lst[i], lst[j]
                i += 1     
        j += 1       
    i -= 1
    k += 1
    lst[left], lst[i] = lst[i], lst[left]
    lst[right], lst[k] = lst[k], lst[right]
    return i, k

def quick_sort_two(lst:list, left, right):
    if left < right:
        lp, rp = parts_for_quick_sort_two(lst, left, right)
        quick_sort_two(lst, left, lp - 1)
        quick_sort_two(lst, lp + 1, rp - 1)
        quick_sort_two(lst, rp + 1, right)
        
'''
l = [1, 5, 2, 8, 4, 0, 4]
quick_sort_two(l, 0, len(l)-1)
print(l)
'''

def generate_different_lists(min_size, max_size, step, max_low_variety) -> list:
    if min_size <= 2:
        raise ValueError("Minimum size must be greater than 2.")
        return -1
    elif min_size >= max_size:
        raise ValueError("Invalid sizes.")
        return -1
    elif max_low_variety > (max_size - min_size)//step:
        raise ValueError("For low variety the amount of elements has to be greater then maximum in a list.")
        return -1
    answear = {'fully sorted':[], 
                'partialy sorted':[], 
                'reverse sorted':[], 
                'fully random':[], 
                'low variety':[],
                'triangle':[]}
    max_value = max_size*1000
    # FULLY SORTED
    fully_sorted = []
    for i in range(min_size, max_size, step):
        fully_sorted.append(list(range(i)))
    answear['fully sorted'] = fully_sorted
    # PARTIALY SORTED
    '''
    Because of this function, it is impossible to generate a list with size less than 3.
    To be partially sorted, a list needs to contain a sequence of sorted elements. A sequence
    can not have a length no less than 2. If length is 0 or 1, the list is fully sorted, 
    if it is 2, it is either fully sorted or not sorted at all.
    '''
    partialy_sorted = []
    for i in range(min_size, max_size, step):
        part = random.randrange(2, i-1)
        part_elem = list(range(part))
        partialy_sorted_temp = []
        for j in range(i-part):
            partialy_sorted_temp.append(random.randint(0, max_value))
        for k in range(part):
            place = random.randrange(0, i-part)
            partialy_sorted_temp.insert(place, part_elem[k])
        partialy_sorted.append(partialy_sorted_temp)
    answear['partialy sorted'] = partialy_sorted
    # REVERSE SORTED
    reverse_sorted = []
    for i in range(min_size, max_size, step):
        reverse_sorted.append(list(reversed(range(i))))
    answear['reverse sorted'] = reverse_sorted
    # FULLY RANDOM
    fully_random = []
    for i in range(min_size, max_size, step):
        fully_random_temp = []
        for j in range(i):
            fully_random_temp.append(random.randint(0, max_value))
        fully_random.append(fully_random_temp)
    answear['fully random'] = fully_random
    # LOW VARIETY
    low_variety = []
    for i in range(min_size, max_size, step):
        low_variety_temp = []
        for j in range(i):
            low_variety_temp.append(random.randint(0, max_low_variety))
        low_variety.append(low_variety_temp)
    answear['low variety'] = low_variety
    # TRIANGLE
    triangle = []
    for i in range(min_size, max_size, step):
        triangle_temp = []
        for j in range(i//2):
            triangle_temp.append(random.randint(0, max_value))
        triangle_temp += list(reversed(triangle_temp))
        triangle.append(triangle_temp)
    answear['triangle'] = triangle
    return answear

def return_times(min_size, max_size, step, max_low_variety):
    lists = generate_different_lists(min_size, max_size, step, max_low_variety)
    times_hoare = {'fully sorted':[], 
                'partialy sorted':[], 
                'reverse sorted':[], 
                'fully random':[], 
                'low variety':[],
                'triangle':[]}
    times_lomuto = {'fully sorted':[], 
                'partialy sorted':[], 
                'reverse sorted':[], 
                'fully random':[], 
                'low variety':[],
                'triangle':[]}
    times_middle_pivot = {'fully sorted':[], 
                'partialy sorted':[], 
                'reverse sorted':[], 
                'fully random':[], 
                'low variety':[],
                'triangle':[]}
    times_random_pivot = {'fully sorted':[], 
                'partialy sorted':[], 
                'reverse sorted':[], 
                'fully random':[], 
                'low variety':[],
                'triangle':[]}
    times_three = {'fully sorted':[], 
                'partialy sorted':[], 
                'reverse sorted':[], 
                'fully random':[], 
                'low variety':[],
                'triangle':[]}
    times_three_random = {'fully sorted':[], 
                'partialy sorted':[], 
                'reverse sorted':[], 
                'fully random':[], 
                'low variety':[],
                'triangle':[]}
    times_two = {'fully sorted':[], 
                'partialy sorted':[], 
                'reverse sorted':[], 
                'fully random':[], 
                'low variety':[],
                'triangle':[]}
    for k, v in lists.items():
        for j in v:
            start = time.time()
            quick_sort_hoare(j, 0, len(j)-1)
            end = time.time()
            times_hoare[k].append(end - start)

            start = time.time()
            quick_sort_lomuto(j, 0, len(j)-1)
            end = time.time()
            times_lomuto[k].append(end - start)

            start = time.time()
            quicksort_middle_pivot(j, 0, len(j)-1)
            end = time.time()
            times_middle_pivot[k].append(end - start)

            start = time.time()
            quicksort_random_pivot(j, 0, len(j)-1)
            end = time.time()
            times_random_pivot[k].append(end - start)

            start = time.time()
            quick_sort_three(j, 0, len(j)-1)
            end = time.time()
            times_three[k].append(end - start)

            start = time.time()
            quick_sort_three_random(j, 0, len(j)-1)
            end = time.time()
            times_three_random[k].append(end - start)

            start = time.time()
            quick_sort_two(j, 0, len(j)-1)
            end = time.time()
            times_two[k].append(end - start)
    return times_hoare, times_lomuto, times_middle_pivot, times_random_pivot, times_three, times_three_random, times_two

max_size = 25
min_size = 5
step = 2

times_hoare, times_lomuto, times_middle_pivot, times_random_pivot, times_three, times_three_random, times_two = return_times(min_size, max_size, step, 4)
for i in list(times_hoare.values()):
    for j in range(math.ceil((max_size - min_size)/step)):
        i[j] = "{:.10f}".format(float(i[j]))
for i in times_lomuto.values():
    for j in range(math.ceil((max_size - min_size)/step)):
        i[j]= "{:.10f}".format(float(i[j]))
for i in times_middle_pivot.values():
    for j in range(math.ceil((max_size - min_size)/step)):
        i[j]= "{:.10f}".format(float(i[j]))
for i in times_random_pivot.values():
    for j in range(math.ceil((max_size - min_size)/step)):
        i[j]= "{:.10f}".format(float(i[j]))
for i in times_three.values():
    for j in range(math.ceil((max_size - min_size)/step)):
        i[j]= "{:.10f}".format(float(i[j]))
for i in times_three_random.values():
    for j in range(math.ceil((max_size - min_size)/step)):
        i[j]= "{:.10f}".format(float(i[j]))
for i in times_two.values():
    for j in range(math.ceil((max_size - min_size)/step)):
        i[j]= "{:.10f}".format(float(i[j]))
'''
print('HOARE')
print(times_hoare)
print('\n')
print('LOMUTO')
print(times_lomuto)
print('\n')
print('MIDDLE PIVOT')
print(times_middle_pivot)
print('\n')
print('RANDOM PIVOT')
print(times_random_pivot)
print('\n')
print('THREE')
print(times_three)
print('\n')
print('THREE RANDOM')
print(times_three_random)
print('\n')
print('TWO PIVOT')
print(times_two)
'''

lens = list(range(min_size, max_size, step))
plt.plot(lens, times_hoare['fully sorted'], label='hoare')
plt.plot(lens, times_lomuto['fully sorted'], label='lomuto')
plt.plot(lens, times_middle_pivot['fully sorted'], label='middle pivot')
plt.plot(lens, times_random_pivot['fully sorted'], label='random pivot')
plt.plot(lens, times_three['fully sorted'], label='three')
plt.plot(lens, times_three_random['fully sorted'], label='three random')
plt.plot(lens, times_two['fully sorted'], label='two pivots')
plt.xlabel("Lenght of list")
plt.ylabel("Time in seconds")
plt.legend()
plt.title("Fully sorted comparison")
plt.show()

plt.plot(lens, times_hoare['partialy sorted'], label='hoare')
plt.plot(lens, times_lomuto['partialy sorted'], label='lomuto')
plt.plot(lens, times_middle_pivot['partialy sorted'], label='middle pivot')
plt.plot(lens, times_random_pivot['partialy sorted'], label='random pivot')
plt.plot(lens, times_three['partialy sorted'], label='three')
plt.plot(lens, times_three_random['partialy sorted'], label='three random')
plt.plot(lens, times_two['partialy sorted'], label='two pivots')
plt.xlabel("Lenght of list")
plt.ylabel("Time in seconds")
plt.legend()
plt.title("Partialy sorted comparison")
plt.show()

plt.plot(lens, times_hoare['reverse sorted'], label='hoare')
plt.plot(lens, times_lomuto['reverse sorted'], label='lomuto')
plt.plot(lens, times_middle_pivot['reverse sorted'], label='middle pivot')
plt.plot(lens, times_random_pivot['reverse sorted'], label='random pivot')
plt.plot(lens, times_three['reverse sorted'], label='three')
plt.plot(lens, times_three_random['reverse sorted'], label='three random')
plt.plot(lens, times_two['reverse sorted'], label='two pivots')
plt.xlabel("Lenght of list")
plt.ylabel("Time in seconds")
plt.legend()
plt.title("Reverse sorted comparison")
plt.show()

plt.plot(lens, times_hoare['fully random'], label='hoare')
plt.plot(lens, times_lomuto['fully random'], label='lomuto')
plt.plot(lens, times_middle_pivot['fully random'], label='middle pivot')
plt.plot(lens, times_random_pivot['fully random'], label='random pivot')
plt.plot(lens, times_three['fully random'], label='three')
plt.plot(lens, times_three_random['fully random'], label='three random')
plt.plot(lens, times_two['fully random'], label='two pivots')
plt.xlabel("Lenght of list")
plt.ylabel("Time in seconds")
plt.legend()
plt.title("Fully random comparison")
plt.show()

plt.plot(lens, times_hoare['low variety'], label='hoare')
plt.plot(lens, times_lomuto['low variety'], label='lomuto')
plt.plot(lens, times_middle_pivot['low variety'], label='middle pivot')
plt.plot(lens, times_random_pivot['low variety'], label='random pivot')
plt.plot(lens, times_three['low variety'], label='three')
plt.plot(lens, times_three_random['low variety'], label='three random')
plt.plot(lens, times_two['low variety'], label='two pivots')
plt.xlabel("Lenght of list")
plt.ylabel("Time in seconds")
plt.legend()
plt.title("Low variety comparison")
plt.show()

plt.plot(lens, times_hoare['triangle'], label='hoare')
plt.plot(lens, times_lomuto['triangle'], label='lomuto')
plt.plot(lens, times_middle_pivot['triangle'], label='middle pivot')
plt.plot(lens, times_random_pivot['triangle'], label='random pivot')
plt.plot(lens, times_three['triangle'], label='three')
plt.plot(lens, times_three_random['triangle'], label='three random')
plt.plot(lens, times_two['triangle'], label='two pivots')
plt.xlabel("Lenght of list")
plt.ylabel("Time in seconds")
plt.legend()
plt.title("Triangle sorted comparison")
plt.show()
