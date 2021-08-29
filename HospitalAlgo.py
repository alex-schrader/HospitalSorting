'''
This program helps the user sort hospitals
via either using the beginning of the name
of one or getting the location the user is
looking for a hospital in.

November 11th
Alex Schrader
'''

def main():
    '''
    Main prints out the initial directions for
    the user, gets the data and stores it in a variable,
    and sends the user to either
    the function corresponding to there choice
    inputs: none
    outputs: none
    '''
    selection = 0
    data = open('hospitals.csv', 'r').readlines()
    for i in range(len(data)):
        data[i] = data[i].split(',')
        data[i][6] = data[i][6].strip('\n')
    print()
    print("To help consumers make informed decisions about health care,")
    print("the Centers for Medicare & Medicaid Services collects data")
    print("about the cost and quality of care at over 4,000 Medicare")
    print("qualified hospitals.")
    print()
    print("This program allows you to explore this data.")
    while selection != "5":
        print()
        print("1. Search by city and state")
        print("2. Search by hospital name")
        print("3. Rank hospitals by city and state")
        print("4. Find the ten most affordable treatment options by state")
        print("5. Quit")
        selection = get_input()
        if selection == "1":
            cityState(data)
        if selection == "2":
            hospitalName(data)
        if selection == "3":
            rankh(data)
        if selection == "4":
            mostAff(data)
        
    print("Goodbye! ")

def rankh(data):
    '''
    3. ranks hospitals by city and state
    inputs: data gathered from main
    outputs: none
    description: uses binary search to find all values in
    the city and state, and sorts them by rank with selection sort
    '''
    searchCity = input("Enter city: ")
    searchState = input("Enter state: ")
    names = []
    for i in range(len(data)):
        if data[i][1].lower() == searchCity.lower() and \
           data[i][2].lower() == searchState.lower():
            names.append(data[i])
    names = selection_sort(names, 3)
    names.reverse()
    formatted(names)
    
def selection_sort(lst, index):
    '''
    inputs: list of values, index of item in each item in the
    list from which to compare for sorting
    outputs: sorted list
    side effects: none
    description: sorts using selection sort
    '''
    n = len(lst)
    for i in range(n-1):
        min_index = i
        for j in range(i+1, n):
            if lst[j][index] < lst[min_index][index]:
                min_index = j
        lst[i], lst[min_index] = lst[min_index], lst[i]
    return lst

def mostAff(data):
    '''
    4. find the ten most affordable treament options by state
    inputs: none
    outputs: none
    effect: prints out results using formatted function
    '''
    searchState = input("Enter state: ")
    names = []
    print("1. Heart procedure")
    print("2. Pneumonia treatment")
    print("3. Hip/knee replacement")
    choice = input("Enter your choice: ")
    for i in range(len(data)):
        if data[i][2].lower() == searchState.lower():
            names.append(data[i])
    choice = int(choice)+3
    names = selection_sort(names, choice)
    highest = 0
    for i in range(len(names)):
        highest = i
        if int(names[i][choice]) != 0:
            break
    names = names[highest:]
    formatted(names[:10])
    
def get_input():
    '''
    description: used in menu to get user input for directory
    input: none
    output: Either the integer 1, 2, or 3
    side effects: none
    '''
    done = False
    while not done:
        number = input("Choice: ")
        if number == "1" or number == "2" or number == "3"\
           or number == "4" or number == "5":
            done = True
        else:
            print("Choice not valid. ")
    return number

def cityState(data):
    '''
    description: This function searches hospital by
    city and state. It first gets all the data from the file
    /data/cs21/hospital/hospitals,csv,  then sorts it
    then gets the desired city and state inputs
    from the user, and then uses binary search by testing each
    value from the data acquired to see if it fits the input from
    the user. It then prints out all the data through the function
    formatted.
    input: none
    outputs: none
    '''
    searchCity = input("Enter city: ")
    searchState = input("Enter state: ")
    names = []
    for i in range(len(data)):
        if data[i][1].lower() == searchCity.lower() and \
           data[i][2].lower() == searchState.lower():
            names.append(data[i])
    formatted(names)

def formatted(list):
    '''
    inputs: list of data with 7 items in each item of the list
    outputs: non
    side effects: prints out the data in a table with the headers
    prints out the average rating of the hopsitals
    hospital name, city, etc.
    '''
    average = 0
    nhosp = 0
    if len(list)>0:
        print(" "*12+"Hospital Name|"+" "*8+
              "City|ST|RATING|HEART($)|PNEUM($)|HIPKN($)")
        print("-"*75)
        for i in range(len(list)):
            print("%25s|%12s|%2s|%6s|%8s|%8s|%8s" % \
                  (list[i][0][:25],list[i][1][:12],list[i][2],list[i][3],
                   list[i][4],list[i][5],list[i][6]))
            if int(list[i][3]) != -1:
                average = average + int(list[i][3])
                nhosp = nhosp + 1
        print()
    print(len(list), "matches found. ")
    if nhosp>0:
        print("Average of reported ratings: %.1f (-1 means no\
 rating reported)" % (average/nhosp))

def expandlist(num, data, name):
    '''
    inputs:
          num: index of the first value found through
    binary search
          data: data from the hospitals containing the
    name of all the hospitals
          name: the input from the user with the desired
    prefix of name

    outputs: a list of the data from the all the hospitals
    that has the prefix the user entered. 
    '''
    hlist = []
    count = num
    while data[count][0].startswith(name):
        count = count - 1

    count += 1
    while data[count][0].startswith(name):
        hlist.append(data[count])
        count += 1
    return hlist


def binarySearch(item, ls):
    '''
    inputs: item the function will search for
    and the list of data from which to search
    for it

    outputs: index of value that has the item or
    -1 if no item in the list has it
    '''
    low = 0
    high = len(ls)-1
    while low<high:
        mid = (low + high)//2
        if ls[mid][0].startswith(item):
            return mid
        elif item < ls[mid][0]:
            high = mid - 1
        else:
            low = mid + 1
    return -1
        
def hospitalName(data):
    '''
    input: none
    output: none
    side effects: gets data, gets prefix of hospital from user,
    prints outs formatted data
    description: search by hospital name
    '''
    hname = input("Enter a hospital name or prefix of a name: ")
    formatted(expandlist((binarySearch(hname, data)), data, hname))

def printResults(indexes, data):
    '''
    description: prints out valid hospitals and data with it
    inputs: index of valid hospitals, list of all hospitals
    and all data
    outputs: none
    side effects: print statement
    '''
    for i in range(len(indexes)):
        print(data[i])

main()