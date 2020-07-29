import sys


def scoring(mid, final):
    average = (float(mid) + float(final.strip())) / 2
    
    if average >= 90:
        grade = "A"
    elif 90 > average >= 80:
        grade = "B"
    elif 80 > average >= 70:
        grade = "C"
    elif 70 > average >= 60:
        grade = "D"
    else:
        grade = "F"
        
    return str(average), grade


def show():
    body_sortList = sorted(body_split, key=lambda x: x[4], reverse=True)
    body_sort = ''

    for i in body_sortList:
        body_sort += '\t'.join(i) + '\n'
    
    return head + body_sort


def search_index(stid):
    for idx, sid in enumerate(body_split):
        if sid[0].strip() == stid:
            return idx


def search(stid):
    idList = [i[0].strip() for i in body_split]
    
    if stid in idList:
        search_result = '\t'.join(body_split[search_index(stid)])
        return search_result
    else:
        return 'NO SUCH PERSON.'


def changescore(stid):
    first_search = search(stid)
    
    if first_search != 'NO SUCH PERSON.':
        test = input('Mid/Final? ')
        while test != ('mid' or 'final'):
            print('mid나 final 중 하나를 입력해주세요.')
            test = input('Mid/Final? ')

        if test == 'mid':
            new_score = int(input('Input new score: '))
            while new_score < 0 or new_score > 100:
                print('0에서 100 사이의 숫자를 입력해주세요.')
                new_score = int(input('Input new score: '))

            find = body_split[search_index(stid)]
            find[2] = str(new_score)
            find[-2:] = scoring(find[2], find[3])
                
            return first_search + '\nScore changed.\n' + search(stid)

        elif test == 'final':
            new_score = int(input('Input new score: '))
            while new_score < 0 or new_score > 100:
                print('0에서 100 사이의 숫자를 입력해주세요.')
                new_score = int(input('Input new score: '))

            find = body_split[search_index(stid)]
            find[3] = str(new_score)
            find[-2:] = scoring(find[2], find[3])

            return first_search + '\nScore changed.\n' + search(stid)
        else:
            pass
    else:
        return 'NO SUCH PERSON.'


def add(stid):
    if search(stid) == 'NO SUCH PERSON.':
        name = input('Name: ')
        mid_score = input('Midterm Score: ')
        final_score = input('Final Score: ')
        data = [stid, name, mid_score, final_score]
        new_line = ' {}\t{:>12}\t{}\t{}\t{}\t{}'.format(data[0], data[1], data[2], data[3].strip(), *scoring(data[-1], data[-2]))
        body_split.append(new_line.split('\t'))
        print('Student added')
        
    else:
        print('ALREADY EXISTS.')

        
def searchgrade(grade):
    if grade in ['A', 'B', 'C', 'D', 'F']:
        gradeList = [i[-1] for i in body_split]
        if gradeList.count(grade) >= 1:
            index = [i for i, j in enumerate(gradeList) if j == grade]
            search = ''
            for idx in index:
                search += '\t'.join(body_split[idx]) + '\n'
            print(head + search.rstrip())
        else:
            print('NO RESULTS.')

            
            
def remove(stid):
    if search(stid) != 'NO SUCH PERSON.':
        del body_split[search_index(stid)]
        print('Student removed.')
    else:
        print('NO SUCH PERSON.')


def quit(save):
    if save == 'yes':
        fname = input('File name: ')
        body_sortList = sorted(body_split, key=lambda x: x[4], reverse=True)
        with open(fname, 'w') as f:
            for data in body_sortList:
                f.write('\t'.join(list(map(lambda x: x.strip(), data[:4])))+'\n')
    else:
        pass


if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = 'students.txt'

with open('students.txt') as f:
    body = ''
    for line in f.readlines():
        data = line.split('\t')
        new_line = ' {}\t{:>12}\t{}\t{}\t{}\t{}\n'.format(data[0], data[1], data[2], data[3].strip(), *scoring(data[-1], data[-2]))
        body += new_line

head = '  Student               Name  Midterm  Final  Average Grade\n--------------------------------------------------------------\n'
body = body.rstrip()
body_split = list(map(lambda x: x.split('\t'), body.split('\n')))
print(show())

command = 'start'
while command != 'quit':
    command = input().lower()
    
    if command == 'show':
        print(show())

    elif command == 'search':
        stid = input('Student ID: ')
        if search(stid) == 'NO SUCH PERSON.':
            print(search(stid))
        else: 
            print(head + search(stid))

    elif command == 'changescore':
        stid = input('Student ID: ')
        if search(stid) == 'NO SUCH PERSON.':
            print(search(stid))
        else:
            print(head + changescore(stid))
               
    elif command == 'add':
        stid = input('Student ID: ')
        add(stid)

    elif command == 'searchgrade':
        grade = input('Grade to search: ')
        searchgrade(grade)        

    elif command == 'remove':
        if len(body_split) > 0:
            stid = input('Student ID: ')
            remove(stid)
        else:
            print('List is empty')

    elif command == 'quit':
        save = input('Save data?[yes/no]')
        while save != 'yes' or 'no':
            print('yes나 no 중 하나를 입력해주세요.')
            save = input('Save data?[yes/no]')
        quit(save)