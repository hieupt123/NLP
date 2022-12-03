with open('./data.txt', mode='r', encoding='utf-8') as my_file:
    lines = my_file.readlines()
    with open('./data_2.txt', mode='w', encoding='utf-8') as my_file2:
        for i in lines:
            if len(i) == 1:
                my_file2.write('\n')
            if ':' in i:
                my_file2.write(i)