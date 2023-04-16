def create_data(file_data):
    """
    Đưa file ngữ liệu txt vô list
    """
    posdata = []
    with open(file_data, mode='r', encoding='utf-8') as my_file:
        lines = my_file.readlines()
        sentence = []
        for i, c in enumerate(lines):
            if (c != "\n") and (i != len(lines) - 1):
                # Xóa dấu gạch dưới
                if '_' in c:
                    text = c.split("_")
                    c = ' '.join(text)
                # print('tu: ', c)
                try:
                    # Tách từ và nhãn
                    word, pos = c.split('\t')
                except:
                    print(c)
                    print('Error: Từ và nhãn phải cách nhau bởi dấu Tab')

                # xóa khoảng trắng 2 đầu
                word = word.strip()
                pos = pos.strip()

                sentence.append((word, pos))
            else:
                if len(sentence) != 0:
                    posdata.append(sentence)
                sentence = []
    return posdata

if __name__=='__main__':
    posdata = create_data('data_tag/manual_pos_tag.txt')
    print(posdata)
    print(len(posdata))


