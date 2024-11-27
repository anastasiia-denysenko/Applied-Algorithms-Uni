import time
import random
import tracemalloc
import matplotlib.pyplot as plt
import pandas as pd

#-----------------------------------
#         FOR GENERATING
#-----------------------------------

def random_list(size):
    random.seed(0)
    L = [ random.random() for i in range(size) ]
    return L

#-----------------------------------
#              MERGE
#-----------------------------------

def merge_in_place(s1, s2) -> list:
    if type(s1) == int and type(s2) == int:
        return list(min(s1, s2), max(s1, s2))
    elif type(s1) == int and type(s2) == list:
        for i in range(len(s2)):
            if s1 > s2[i] and s1 < s2[i+1]:
                s2.insert(i+1, s1)
        return s2
    elif type(s1) == list and type(s2) == int:
        for i in range(len(s1)):
            if s2 > s1[i] and s2 < s1[i+1]:
                s1.insert(i+1, s2)
        return s1
    else:
        for i in range(len(s2) - 1, -1, -1):
            if s1[-1] > s2[i]:
                last = s1[-1]
                j = len(s1) - 2
                while j >= 0 and s1[j] > s2[i]:
                    s1[j + 1] = s1[j]
                    j -= 1
                s1[j + 1] = s2[i]
                s2[i] = last
        s1 += s2
        return s1
        

#-----------------------------------
#           TOP DOWN
#-----------------------------------

def top_down(lst:list) -> list:
    half = len(lst)//2
    s1, s2 = lst[:half], lst[half:]
    if len(s1) > 1:
        s1 = top_down(s1)
    if len(s2) > 1:
        s2 = top_down(s2)
    return merge_in_place(s1, s2)


#-----------------------------------
#        MERGE FOR COUNTING
#-----------------------------------

def merge_in_place_calculations(s1:list, s2:list, copies:list, comparisons:int) -> tuple:
    result = []
    if type(s1) == int and type(s2) == int:
        comparisons+=1
        return list(min(s1, s2), max(s1, s2)), copies, comparisons
    elif type(s1) == int and type(s2) == list:
        for i in range(len(s2)):
            if s1 > s2[i] and s1 < s2[i+1]:
                comparisons += 1
                s2.insert(i+1, s1)
        return s2, copies, comparisons
    elif type(s1) == list and type(s2) == int:
        for i in range(len(s1)):
            if s2 > s1[i] and s2 < s1[i+1]:
                comparisons += 1
                s1.insert(i+1, s2)
        return s1, copies, comparisons
    else:
        for i in range(len(s2) - 1, -1, -1):
            if s1[-1] > s2[i]:
                comparisons += 1
                last = s1[-1]
                j = len(s1) - 2
                while j >= 0 and s1[j] > s2[i]:
                    s1[j + 1] = s1[j]
                    j -= 1
                s1[j + 1] = s2[i]
                s2[i] = last
        s1 += s2
        return s1, copies, comparisons

#-----------------------------------
#     TOP DOWN CALCULATIONS
#-----------------------------------

def top_down_calculations(lst:list, copies:list, comparisons:int) -> tuple:
    half = len(lst)//2
    s1, s2 = lst[:half], lst[half:]
    copies.append(1)
    if len(s1) > 1:
        s1 = top_down_calculations(s1, copies, comparisons)[0]
    if len(s2) > 1:
        s2 = top_down_calculations(s2, copies, comparisons)[0]
    return merge_in_place_calculations(s1, s2, copies, comparisons)

def print_top_down_calculations(lst):
    res = top_down_calculations(lst,[],0)
    print('copies: ', len(res[1]), 'comparisons: ', res[2])

#-----------------------------------
#     TOP DOWN TIME AND SPACE
#-----------------------------------

def top_down_mesure_time(lst:list) -> float:
    start = time.time()
    top_down(lst)
    end = time.time()
    return end - start

def top_down_space(lst:list):
    tracemalloc.start()
    top_down(lst)
    snapshot = tracemalloc.take_snapshot()
    for stat in snapshot.statistics('lineno'):
        print(stat)

#-----------------------------------
#          BOTTOM UP
#-----------------------------------

def bottom_up(lst:list) -> list:
    a = [[n] for n in lst]
    while len(a) > 1:
        n = []
        for i in range(0, len(a), 2):
            n.append(merge_in_place(a[i], a[i+1] if i+1<len(a) else []))   
        a = n
    return a[0]

#-----------------------------------
#       BOTTOM UP COUNTING
#-----------------------------------

def bottom_up_calculations(lst:list) -> tuple:
    a = [[n] for n in lst]
    copies, comparisons = 0, 0
    while len(a) > 1:
        n = []
        for i in range(0, len(a), 2):
            if i+1<len(a):
                l = merge_in_place_calculations(a[i], a[i+1], copies, comparisons)
                n.append(l[0])  
                copies += 1
                comparisons = l[2]
            else:
                n.append([])
        a = n
    return a[0], copies, comparisons

#-----------------------------------
#     BOTTOM UP TIME AND SPACE
#-----------------------------------

def bottom_up_mesure_time(lst:list) -> float:
    start = time.time()
    bottom_up(lst)
    end = time.time()
    return end - start

def bottom_up_space(lst:list):
    tracemalloc.start()
    bottom_up(lst)
    snapshot = tracemalloc.take_snapshot()
    for stat in snapshot.statistics('lineno'):
        print(stat)

#-----------------------------------
# GENERATE DIFFERENT TYPES OF LISTS
#-----------------------------------

def generate_different_lists(min_size, max_size, step, max_low_variety) -> dict:
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
                'low variety':[]}
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
    return answear

#-----------------------------------
#      MORE EFFECTIVE VERSION
#-----------------------------------

def merge_efficient(s1, s2) -> list:
    aux = []
    i, j, k = 0, 0, 0
    n1, n2 = len(s1), len(s2)
    while i < n1 and j < n2:
        if s1[i] < s2[j]:
            aux.append(s1[i])
            i += 1
        else:
            aux.append(s2[j])
            j += 1
    while i < n1:
        aux.append(s1[i])
        i += 1
    while j < n2:
        aux.append(s2[j])
        j += 1
    return aux

def stop_if_already_sorted(lst:list) -> int:
    count = 0
    for i in range(len(lst)-1):
        if lst[i] <= lst[i+1]:
            continue
        else:
            count += 1
    return count

def stop_if_reverse_sorted(lst:list) -> int:
    count = 0
    for i in range(len(lst)-1):
        if lst[i] >= lst[i+1]:
            continue
        else:
            count += 1
    return count

def to_insertion(lst:list) -> list:
    for i in range(1, len(lst)):
        temp = lst[i]
        j = i - 1
        while j >= 0 and temp < lst[j]:
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = temp
    return lst

def bottom_up_efficient(lst:list, cutoff:int) -> list:
    if stop_if_already_sorted(lst) == 0:
        return lst
    elif stop_if_reverse_sorted(lst) == 0:
        return list(reversed(lst))
    a = [[n] for n in lst]
    while len(a) > 1:
        n = []
        for i in range(0, len(a), 2):
            if i+1<len(a):
                if len(a[i]) >= cutoff:
                    n.append(merge_efficient(a[i], a[i+1]))
                else:
                    n.append(to_insertion(a[i]+a[i+1]))
            else:
                n.append([])
        a = n
    return a[0]

#-----------------------------------
#  MORE EFFECTIVE VERSION COUNTING
#-----------------------------------

def merge_calculations(s1:list, s2:list, copies:list, comparisons:int) -> tuple:
    aux = []
    i, j, k = 0, 0, 0
    n1, n2 = len(s1), len(s2)
    while i < n1 and j < n2:
        comparisons += 1
        if s1[i] < s2[j]:
            aux.append(s1[i])
            i += 1
        else:
            aux.append(s2[j])
            j += 1
    while i < n1:
        aux.append(s1[i])
        i += 1
    while j < n2:
        aux.append(s2[j])
        j += 1
    return aux, copies, comparisons

def stop_if_already_sorted_counting(lst:list) -> tuple:
    count = 0
    comparisons = 0
    for i in range(len(lst)-1):
        comparisons += 1
        if lst[i] <= lst[i+1]:
            continue
        else:
            count += 1
    return count, comparisons

def stop_if_reverse_sorted_counting(lst:list) -> tuple:
    count = 0
    comparisons = 0
    for i in range(len(lst)-1):
        comparisons += 1
        if lst[i] >= lst[i+1]:
            continue
        else:
            count += 1
    return count, comparisons

def to_insertion_counting(lst:list, copies:int, comparisons:int) -> tuple:
    for i in range(1, len(lst)):
        temp = lst[i]
        copies += 1
        j = i - 1
        while j >= 0 and temp < lst[j]:
            comparisons += 1
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = temp
    return lst, copies, comparisons

def bottom_up_efficient_counting(lst:list, cutoff:int) -> tuple:
    comparisons, copies = 0, 0
    sifasc = stop_if_already_sorted_counting(lst)
    sirsc = stop_if_reverse_sorted_counting(lst)
    if sifasc[0] == 0:
        return lst, sifasc[1], 0
    elif sirsc[0] == 0:
        return lst, sirsc[1], 0
    a = [[n] for n in lst]
    while len(a) > 1:
        n = []
        for i in range(0, len(a), 2):
            if i+1<len(a):
                if len(a[i]) >= cutoff and len(a[i+1]) >= cutoff:
                    l = merge_calculations(a[i], a[i+1], copies, comparisons)
                    n.append(l[0])
                    comparisons += l[2]   
                    copies += 1
                else:
                    l = to_insertion_counting(a[i]+a[i+1], copies, comparisons)
                    n.append(l[0])
                    copies += 1
                    comparisons += l[2]
            else:
                n.append([])
        a = n
    return a[0], copies, comparisons

#-----------------------------------
#  MORE EFFECTIVE V TIME AND SPACE
#-----------------------------------

def bottom_up_efficient_mesure_time(lst:list, cutoff:int) -> float:
    start = time.time()
    bottom_up_efficient(lst, cutoff)
    end = time.time()
    return end - start

def bottom_up_efficient_space(lst:list, cutoff:int):
    tracemalloc.start()
    bottom_up_efficient(lst, cutoff)
    snapshot = tracemalloc.take_snapshot()
    for stat in snapshot.statistics('lineno'):
        print(stat)

#-----------------------------------
#      SORTING LINKED LIST
#-----------------------------------

class Node:
    def __init__(self, x):
        self.data = x
        self.next = None

# for creating linked list out of list

def append(head, item):
    temp = Node(item)
    if head is None:
        return temp
    last = head
    while last.next is not None:
        last = last.next  
    last.next = temp
    return head

def arr_to_linked(arr):
    head = None
    for i in arr:
        head = append(head, i)
    return head

# for merge sort

def split_linked(head):
    f, s = head, head
    while f and f.next:
        f = f.next.next
        if f:
            s = s.next
    res = s.next
    s.next = None
    return res

def merge_linked(s1, s2):
    if not s1:
        return s2
    if not s2:
        return s1
    if s1.data < s2.data:
        s1.next = merge_linked(s1.next, s2)
        return s1
    else:
        s2.next = merge_linked(s1, s2.next)
        return s2

def merge_sort_linked(head):
    if not head or not head.next:
        return head
    s2 = split_linked(head)
    head = merge_sort_linked(head)
    s2 = merge_sort_linked(s2)
    return merge_linked(head, s2)

# for printing

def print_linked_list(head):
    curr = head
    while curr:
        print(curr.data, end=" ")
        curr = curr.next
    print()

'''
k = [2, 5, 1, 8, 6, 0, 3, 2]
head = arr_to_linked(k)
n = merge_sort_linked(head)
print_linked_list(n)
'''

#-----------------------------------
#   SORTING LINKED LIST COUNTING
#-----------------------------------

def split_linked_counting(head, copies, comparisons) -> tuple:
    f, s = head, head
    copies += 1
    while f and f.next:
        f = f.next.next
        if f:
            s = s.next
    res = s.next
    copies += 1
    s.next = None
    return res, copies, comparisons

def merge_linked_counting(s1, s2, copies, comparisons) -> tuple:
    if not s1:
        return s2, copies, comparisons
    if not s2:
        return s1, copies, comparisons
    if s1.data < s2.data:
        comparisons += 1
        s1.next = merge_linked_counting(s1.next, s2, copies, comparisons)[0]
        return s1, copies, comparisons
    else:
        comparisons += 1
        s2.next = merge_linked_counting(s1, s2.next, copies, comparisons)[0]
        return s2, copies, comparisons

def merge_sort_linked_counting(head, copies, comparisons) -> tuple:
    if not head or not head.next:
        return head, copies, comparisons
    l = split_linked_counting(head, copies, comparisons)
    s2, copies, comparisons = l[0], l[1], l[2]
    m = merge_sort_linked_counting(head, copies, comparisons)
    head, copies, comparisons = m[0], m[1], m[2]
    k = merge_sort_linked_counting(s2, copies, comparisons)
    s2, copies, comparisons = k[0], k[1], k[2]
    return merge_linked_counting(head, s2, copies, comparisons)

'''
k = [2, 5, 1, 8, 6, 0, 3, 2]
head = arr_to_linked(k)
n = merge_sort_linked_counting(head, 0, 0)
print_linked_list(n[0])
print(n[1], n[2])
'''
#-----------------------------------
# SORTING LINKED LIST TIME AND SPACE
#-----------------------------------

def merge_sort_linked_mesure_time(lst:list) -> float:
    head = arr_to_linked(lst)
    start = time.time()
    merge_sort_linked(head)
    end = time.time()
    return end - start

def merge_sort_linked_efficient_space(lst:list):
    head = arr_to_linked(lst)
    tracemalloc.start()
    merge_sort_linked(head, 0, 0)
    snapshot = tracemalloc.take_snapshot()
    for stat in snapshot.statistics('lineno'):
        print(stat)

#-----------------------------------
#          COUNTING ALL
#-----------------------------------
'''
Cretates datasets with counted time, copies and comparisons, and plots the results.
d = generate_different_lists(10, 50, 1, 5)
res_top_down = {
        'index':list(range(10, 50, 1)),
        'fully sorted time':[], 
        'fully sorted copies':[], 
        'fully sorted comparisons':[], 
        'partialy sorted time':[], 
        'partialy sorted copies':[], 
        'partialy sorted comparisons':[], 
        'reverse sorted time':[], 
        'reverse sorted copies':[], 
        'reverse sorted comparisons':[], 
        'fully random time':[], 
        'fully random copies':[], 
        'fully random comparisons':[], 
        'low variety time':[],
        'low variety copies':[],
        'low variety comparisons':[]}
res_bottom_up = {
        'index':list(range(10, 50, 1)),
        'fully sorted time':[], 
        'fully sorted copies':[], 
        'fully sorted comparisons':[], 
        'partialy sorted time':[], 
        'partialy sorted copies':[], 
        'partialy sorted comparisons':[], 
        'reverse sorted time':[], 
        'reverse sorted copies':[], 
        'reverse sorted comparisons':[], 
        'fully random time':[], 
        'fully random copies':[], 
        'fully random comparisons':[], 
        'low variety time':[],
        'low variety copies':[],
        'low variety comparisons':[]}
res_more_efficient = {
        'index':list(range(10, 50, 1)),
        'fully sorted time':[], 
        'fully sorted copies':[], 
        'fully sorted comparisons':[], 
        'partialy sorted time':[], 
        'partialy sorted copies':[], 
        'partialy sorted comparisons':[], 
        'reverse sorted time':[], 
        'reverse sorted copies':[], 
        'reverse sorted comparisons':[], 
        'fully random time':[], 
        'fully random copies':[], 
        'fully random comparisons':[], 
        'low variety time':[],
        'low variety copies':[],
        'low variety comparisons':[]}
res_linked = {
        'index':list(range(10, 50, 1)),
        'fully sorted time':[], 
        'fully sorted copies':[], 
        'fully sorted comparisons':[], 
        'partialy sorted time':[], 
        'partialy sorted copies':[], 
        'partialy sorted comparisons':[], 
        'reverse sorted time':[], 
        'reverse sorted copies':[], 
        'reverse sorted comparisons':[], 
        'fully random time':[], 
        'fully random copies':[], 
        'fully random comparisons':[], 
        'low variety time':[],
        'low variety copies':[],
        'low variety comparisons':[]}
keys = list(d.keys())
for i in keys:
    for k in d[i]:
        # TOP DOWN
        tdc = top_down_calculations(k, [], 0)
        res_top_down[i+' time'].append(top_down_mesure_time(k))
        res_top_down[i+' copies'].append(len(tdc[1]))
        res_top_down[i+' comparisons'].append(tdc[2])
        # BOTTOM UP
        buc = bottom_up_calculations(k)
        res_bottom_up[i+' time'].append(bottom_up_mesure_time(k))
        res_bottom_up[i+' copies'].append(buc[1])
        res_bottom_up[i+' comparisons'].append(buc[2])
        # EFFICIENT
        buec = bottom_up_efficient_counting(k, 6)
        res_more_efficient[i+' time'].append(bottom_up_efficient_mesure_time(k, 6))
        res_more_efficient[i+' copies'].append(buec[1])
        res_more_efficient[i+' comparisons'].append(buec[2])
        # LINKED
        head = arr_to_linked(k)
        mslc = merge_sort_linked_counting(head, 0, 0)
        res_linked[i+' time'].append(merge_sort_linked_mesure_time(k))
        res_linked[i+' copies'].append(mslc[1])
        res_linked[i+' comparisons'].append(mslc[2])
# create dataframes out of results
df_res_top_down = pd.DataFrame(res_top_down)
df_res_bottom_up = pd.DataFrame(res_bottom_up)
df_res_more_efficient = pd.DataFrame(res_more_efficient)
df_res_linked = pd.DataFrame(res_linked)
# save data as csv
df_res_top_down.to_csv('df_res_top_down.csv', index=False)
df_res_bottom_up.to_csv('df_res_bottom_up.csv', index=False)
df_res_more_efficient.to_csv('df_res_more_efficient.csv', index=False)
df_res_linked.to_csv('df_res_linked.csv', index=False)


for i in ['fully sorted','partialy sorted','reverse sorted','fully random','low variety']:
    for j in ['time', 'copies', 'comparisons']:
        for k in [df_res_top_down, df_res_bottom_up, df_res_more_efficient, df_res_linked]:
            plt.plot(k['index'], k[i+' '+j])
            plt.xlabel("Number of elements in array")
            plt.ylabel(j)
        plt.title(i)
        plt.legend(['df_res_top_down', 'df_res_bottom_up', 'df_res_more_efficient', 'df_res_linked'], loc="lower right")
        plt.show()
'''