import gensim
model = gensim.models.KeyedVectors.load_word2vec_format('vector/model.vec', binary=False)

summer_word_list = ['夏', '暑い', '海', 'クーラー', 'スイカ', '山', 'サンダル', '宿題', '川', 'カブトムシ', '風鈴', 'キャンプ', 'かき氷', '夏休み']

negative_word_list = ['冬', '寒い', '暖房', '鍋', '雪', 'スキー', 'みかん', 'お湯', '温泉', '冬休み', '冬場']

def posi_nega_score(x):
    #ポジティブ度合いの判定
    posi = []
    for i in summer_word_list:
        try:
            n = model.similarity(i, x)
            posi.append(n)
        except:
            continue
    try:
        posi_mean = sum(posi)/len(posi)
    except:
        posi_mean = 0

    #ネガティブ度合いの判定
    nega = []
    for i in negative_word_list:
        try:
            n = model.similarity(i, x)
            nega.append(n)
        except:
            continue
    try:
        nega_mean = sum(nega)/len(nega)
    except:
        nega_mean = 0
    
    if posi_mean > nega_mean:
        return posi_mean
    if nega_mean > posi_mean:
        return -nega_mean
    else:
        return 0

print(posi_nega_score("雪だるま"))

# result = model.most_similar(positive=summer_word_list, negative=negative_word_list)

# print(result)

# first = ''
# second = ''

# print('「{}」と「{}」の単語的な一致度は{}%です．'.format(first, second, model.similarity(first, second)*100))