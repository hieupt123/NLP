

posdata = []
line = []
with open('./data_2.txt', mode='r', encoding='utf-8') as my_file:
    lines = my_file.readlines()
    for c in lines:
        if len(c) == 1:
            if len(line) != 0:
                posdata.append(line)
            line = []
        else:
            if '_' in c:
                text = c.split("_")
                c = ' '.join(text)

            word, pos = c.split(':')
            # xóa khoảng trắng 2 đầu
            word = word.strip()
            pos = pos.strip()
            line.append((word, pos))

print(posdata)
print(len(posdata))


