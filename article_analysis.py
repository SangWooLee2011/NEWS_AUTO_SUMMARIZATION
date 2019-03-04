from lexrank import STOPWORDS, LexRank
import re
from topic_model import Model, Prepro
import pprint

class ArticleText():
    # represeting an article with the data processed and needed to processed.

    def __init__(self, body="", title="", url=""):
        self.body = body
        self.title = title
        self.url = url
        self.sentences = []
        self.summary = []
        self.lrScore = 0

    def __init__(self, body="", title="", url="", summary="", sentences=[], lrScore=0):
        self.body = body
        self.title = title
        self.url = url
        self.sentences = sentences
        self.summary = summary
        self.lrScore = lrScore

    def __lt__(self, other):
        return self.lrScore > other.lrScore

class Data_by_category():
    def __init__(self, category="", doc_num=70):
        self.articleData = []
        self.topics = []
        self.create_data(category, doc_num)

    def create_data(self, category="", doc_num=70):
        for i in range(0,doc_num):
            self.articleData.append(ArticleText(self.read_body("korea_times", category, i + 1),
                                                self.read_info("korea_times", category, i + 1)[0],
                                                self.read_info("korea_times", category, i + 1)[1]))
            self.articleData.append(ArticleText(self.read_body("korea_herald", category, i + 1),
                                                self.read_info("korea_herald", category, i + 1)[0],
                                                self.read_info("korea_herald", category, i + 1)[1]))
        for article in self.articleData:
            article.sentences = self.split_to_sentence(article.body)
        lxr = LexRank(self.get_all_sentence_list(), stopwords=STOPWORDS['en'])
        for article in self.articleData:
            article.summary = lxr.get_summary(article.sentences,summary_size=3, threshold=.2)
        self.get_lrScore()
        self.articleData.sort()

    def read_body(self, newspaper="", category="", num=0):
        f = open("C:/news_data/"+ newspaper +"/"+category+"_article"+ str(num)+".txt", 'rt', encoding='UTF8')
        text = f.read()
        f.close()
        return text

    def read_info(self, newspaper="", category="", num=0):
        f = open("C:/news_data/"+ newspaper +"/"+category+"_title_url" + str(num) + ".txt", 'r', encoding='UTF8')
        infoList= f.read().split("@")
        return infoList

    def get_all_sentence_list(self):
        bodies = []
        for articleObj in self.articleData:
            bodies.append(articleObj.sentences)
        return bodies

    def get_all_summary_list(self):
        summaries = []
        for articleObj in self.articleData:
            summaries.append(articleObj.summary)
        return summaries

    def split_to_sentence(self, text):
        caps = "([A-Z])"
        prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
        suffixes = "(Inc|Ltd|Jr|Sr|Co)"
        starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
        acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
        websites = "[.](com|net|org|io|gov)"
        point_num = "([0-9])[.]([0-9])"
        shortForm1 = "(etc|et al|viz)[.]"
        shortForm2 = "(e|i)[.](g|e)[.]"
        text = " " + text + "  "
        text = text.replace("\n", " ")
        text = re.sub(shortForm1, "\\1<prd>", text)
        text = re.sub(shortForm2, "\\1<prd>\\2", text)
        text = re.sub(prefixes, "\\1<prd>", text)
        text = re.sub(websites, "<prd>\\1", text)
        text = re.sub(point_num, "\\1<prd>\\2", text)
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
        if "\\" in text: text = text.replace("\\","")
        text = text.replace(".", ".<stop>")
        text = text.replace("?", "?<stop>")
        text = text.replace("!", "!<stop>")
        text = text.replace("<prd>", ".")
        sentences = text.split("<stop>")
        sentences = sentences[:-1]
        sentences = [s.strip() for s in sentences]




        return sentences

    def get_lrScore(self):
        lxr = LexRank(self.get_all_summary_list(), stopwords=STOPWORDS['en'])

        summary_to_one_sentence =[]

        for article in self.articleData:
            str = ""
            for sen in article.summary:
                str += sen
            summary_to_one_sentence.append(str)

        scores_cont = lxr.rank_sentences(
            summary_to_one_sentence,
            threshold=None,
            fast_power_method=False,
        )
        for i, score in enumerate(scores_cont):
            self.articleData[i].lrScore = score

    def topic_modeling(self):
        raw_text =""
        for article in self.get_all_sentence_list():
            for sen in article:
                raw_text = raw_text+sen
        a = Model(raw_text)
        print(a.get_topics())



"""
test = Data_by_category("economy_Finance_times", 100)
for i in test.articleData:
    print("중요도 : ",i.lrScore)
    print("기사제목 : ",i.title)
    print("기사원문 : ",i.url)
    print("<기사 요약>")
    print(i.summary)
    print("----------------------------------------")
"""