import re
import logging
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models
from collections import defaultdict
from nltk.stem import WordNetLemmatizer

class Prepro:
    stoplist = set('for a of the and an be was were been is are but to it not in or from '
                    'we on that this have has ltd as ± by et al al. al, mm with kb ph wkg won percent year percent'.split())

    def __init__(self, raw_data):
        self.raw_data = raw_data;

    def get_preprocessed_text(self):
        data = self.split_into_sentences(re.sub('[%&<>;:()/?|\d]', '', self.raw_data))

        text_data = [[word for word in document.lower().split() if word not in self.stoplist]
                     for document in data] # 불필요한 단어는 제외하고 단어들의 리스트(=문장)를 리스트로 저장 -> [['word1','word2'],['word3','word4']]



        lemmatizer = WordNetLemmatizer()  # nltk 라이브러리의 WordNetLemmatizer : 단어를 원형복원시켜주는 메쏘드
        for i, word_bag in enumerate(text_data):  # 복수형, 과거형 등등의 다양한 형태를 원형복원을 통해서 모두 원형으로 바꿔줌.
            for j, word in enumerate(word_bag):
                text_data[i][j] = lemmatizer.lemmatize(word)

        for i, sen in enumerate(text_data):
            for j, word in enumerate(sen):
                text_data[i][j] = re.sub('[,.]', '', word)  # text에 포함된 불필요 문자열들을 제외시켜준다. 정규표현식 사용
            while '' in sen:
                text_data[i].remove('')  # 아무것도 안남은 단어들을 지워준다."

        while [] in text_data:
            text_data.remove([])  # 아무것도 안남은 문장들을 지워준다.

        frequency = defaultdict(int)
        for text in text_data:
            for token in text:
                frequency[token] += 1
        text_data = [[token for token in text if frequency[token] > 1] for text in text_data]  # 단 한번만 나타나는 단어 제거

        return text_data

    def split_into_sentences(self, text):
        caps = "([A-Z])"
        prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
        suffixes = "(Inc|Ltd|Jr|Sr|Co)"
        starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
        acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
        websites = "[.](com|net|org|io|gov)"
        text = " " + text + "  "
        text = text.replace("\n", " ")
        text = re.sub(prefixes, "\\1<prd>", text)
        text = re.sub(websites, "<prd>\\1", text)
        if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
        text = re.sub("\s" + caps + "[.] ", " \\1<prd> ", text)
        text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
        text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
        text = re.sub(caps + "[.]" + caps + "[.]", "\\1<prd>\\2<prd>", text)
        text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
        text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
        text = re.sub(" " + caps + "[.]", " \\1<prd>", text)
        if "”" in text: text = text.replace(".”", "”.")
        if "\"" in text: text = text.replace(".\"", "\".")
        if "!" in text: text = text.replace("!\"", "\"!")
        if "?" in text: text = text.replace("?\"", "\"?")
        text = text.replace(".", ".<stop>")
        text = text.replace("?", "?<stop>")
        text = text.replace("!", "!<stop>")
        text = text.replace("<prd>", ".")
        sentences = text.split("<stop>")
        sentences = sentences[:-1]
        sentences = [s.strip() for s in sentences]
        return sentences


class Model(Prepro):
    def __init__(self, raw_text):
        Prepro.__init__(self, raw_text)

    def get_topics(self):
        text_data = self.get_preprocessed_text()  #선처리 된 문서를 받아온다.

        dictionary = corpora.Dictionary(text_data)  # corpora.Dictionary : Dictionary encapsulates the mapping between normalized words and their integer ids. -> (integer id : word)
                                                    # corpora.Dictionary : 정규화된 단어들(중복된 단어는 제거된 단어들)과 그에게 부여된 숫자를 맵핑하여 객체화시킨다. -> (integer id : word)
        # print(dictionary.token2id) #  토큰-토큰ID 출력.
        # print(dictionary.dfs) # 토큰-토큰이 문서에 포함된 횟수(빈도수).

        corpus = [dictionary.doc2bow(normalized_word) for normalized_word in
                  text_data]  # doc2bow는 dictionary 값을 가공하여 (token_id, 문서에 포함된 횟수)의 형식으로 벡터값을 리턴해준다..



        tfidf = models.TfidfModel(corpus)  # tfidf 모델을 초기화 한다.
        corpus_tfidf = tfidf[corpus]  #백터를 tfidf 모델로 분석
        lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=5)  #lsi 모델을 초기화 하며 바로 tfidf 분석한 결과를 넣어서 lsi로 다시 분석.

        result = []
        for i, word in enumerate(lsi.print_topics(5)): # 메소드가 리턴해주는 값에서 필요한 단어와 확률부분만 추출해서 리스트형식으로 저장.
            x = word[1].split('"')
            for w in range(0, len(x), 2):
                if(w+1<len(x)):
                    result.append([i, float(re.sub('[ *+]', '', x[w])), x[w+1]])

        return result  # [[문장번호 ,등장확률, 단어]...] 의 형태로 리턴됨
