import csv

def main():
    provinces_list = read_provinces_list('provinces.txt')
    provinces_list.pop(0)
    provinces_list.pop()
    
    for i in range(len(provinces_list)):
        if provinces_list[i] == ['AB']:
            provinces_list[i] = ['Alberta']
    
    count = provinces_list.count(['Alberta'])
    print(provinces_list)
    print('\nNumber of times Alberta appeared in list:', count)

def read_provinces_list(filename):
    compound_list = []

    with open(filename, 'rt') as text_file:
        reader = csv.reader(text_file)

        for row_list in reader:
            if len(row_list) != 0:
                compound_list.append(row_list)

    return compound_list

if __name__ == '__main__':
    main()