from create_data import create_data
import numpy as np
import pandas as pd

def create_matrix_A(posdata, tags, laplace = 0):
    tags = list(tags)
    tags.insert(0, '<s>')
    tags_matrix = np.zeros((len(tags), len(tags)-1), dtype=np.float32)
    A = pd.DataFrame(tags_matrix, columns=tags[1:], index=tags)

    for s in posdata:
        for i in range(len(s)-1):
            if i == 0:
                A.loc['<s>'][s[0][1]] += 1
            tag_left = s[i][1]
            tag_right = s[i+1][1]
            A.loc[tag_left][tag_right] +=1

    # print(A)
    A = A + laplace
    # print(A)
    for i in range(len(tags)):
        if A.iloc[i].sum() != 0:
            A.iloc[i] = A.iloc[i]/A.iloc[i].sum()

    return A

def create_matrix_B(posdata, tags, words, laplace = 0):
    words_matrix = np.zeros((len(tags), len(words)), dtype=np.float32)
    B = pd.DataFrame(words_matrix, columns=list(words), index=list(tags))

    for s in posdata:
        for tup in s:
            tag = tup[1]
            word = tup[0]
            B.loc[tag][word] += 1
    # print(B)
    B = B+ laplace
    # print(B)
    for i in range(len(tags)):
        if B.iloc[i].sum() != 0:
            B.iloc[i] = B.iloc[i] / B.iloc[i].sum()
    return B



def Viterbi(sentence, A, B, tags):
    backpointer = np.zeros((len(tags), len(sentence)), dtype=np.uint8)
    # print(sentence)
    matrix = np.zeros((len(tags), len(sentence)), dtype=np.float32)
    viterbi = pd.DataFrame(matrix, columns=sentence, index=list(tags))
    try:
        viterbi.iloc[:,0] = A.loc['<s>'] * B[sentence[0]]
    except:
        viterbi.iloc[:, 0] = A.loc['<s>']

    # viterbi.iloc[:, 0] = A.loc['<s>'] * B[sentence[0]]

    for t in range(1, len(sentence)):
        for s in range(len(tags)):
            try:
                viterbi.iloc[s, t] = (viterbi.iloc[:, t-1] * A.iloc[1:,s]*B[sentence[t]][s]).max()
                backpointer[s, t] = (viterbi.iloc[:, t - 1] * A.iloc[1:, s] * B[sentence[t]][s]).argmax()
            except:
                viterbi.iloc[s, t] = (viterbi.iloc[:, t - 1] * A.iloc[1:, s]).max()
                backpointer[s, t] = (viterbi.iloc[:, t - 1] * A.iloc[1:, s]).argmax()
    # print(viterbi)
    bestpathprob = viterbi.iloc[:,-1].max()
    bestpathpointer = viterbi.iloc[:,-1].argmax()
    bestpath = []
    # print('best path: \n', backpointer)
    # print('best pro: \n', viterbi)
    # bestpath.append(viterbi.index[bestpathpointer])
    for i in range(len(sentence)-1, 0, -1):
        bestpath.append(viterbi.index[bestpathpointer])
        bestpathpointer = backpointer[bestpathpointer, i]
    bestpath.append(viterbi.index[bestpathpointer])
    bestpath.reverse()
    # print(bestpath)
    #
    # print(bestpathpointer)
    # print(viterbi)
    # print(backpointer)
    # print(viterbi['mèo'].argmax())
    # print(viterbi.iloc[1, 1])
    return bestpath, bestpathprob, viterbi

def predict(wordtest, A, B, tags):
    pre = []
    for s in wordtest:
        word = [w[0] for w in s]
        bestpath, _, v = Viterbi(word, A, B, tags)
        bestpath2, _, v2 = Viterbi(word, A, B, tags)
        pos = [(w, t) for w, t in zip(word, bestpath)]
        pre.append(pos)
    return pre

def accuracy(pre, ground_truth):
    num_true_tags = 0
    num_tags = 0
    for p, g in zip(pre, ground_truth):
        for tup_p, tup_g in zip(p, g):
            if tup_p[1] == tup_g[1]:
                num_true_tags+=1
            num_tags+=1
    return num_true_tags/num_tags, num_true_tags, num_tags

if __name__=='__main__':
    np.random.seed(42)
    # ngữ liệu tách và gãn nhãn bằng VNcore
    file = 'data_tag/vncore_pos_tag.txt'

    # # Ngữ liệu tách và gãn nhãn bằng tay
    # file = 'data_tag/manual_pos_tag.txt'

    # Load data_tag
    posdata = create_data(file)

    # Create train test
    postraindata = posdata[:62]
    postestdata = posdata[62:]

    # unique tag
    tags = {tup[1] for s in postraindata for tup in s}
    tags = sorted(tags)

    # unique word
    words = {tup[0] for s in postraindata for tup in s}
    words = sorted(words)
    sooth = 1
    A, B = create_matrix_A(postraindata, tags, laplace=sooth), create_matrix_B(postraindata, tags, words, laplace=sooth)


    train_pre = predict(postraindata, A, B, tags)
    print('accurary train: ', accuracy(train_pre, postraindata))
    test_pre = predict(postestdata, A, B, tags)
    print('accurary test: ', accuracy(test_pre, postestdata))
    print("Test predicted: ",test_pre)
    print("Data_test: ",postestdata)
    # print(test_pre)