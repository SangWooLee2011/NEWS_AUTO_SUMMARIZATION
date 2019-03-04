import requests
from bs4 import BeautifulSoup

class Crawaler_Korea_Times():
    def __init__(self):
        #category 별로 root 사이트 정의
        self.National_root = "http://www.koreatimes.co.kr/www/sublist_113_@.html"
        self.Sports_root = "http://www.koreatimes.co.kr/www/sublist_600_@.html"
        self.World_root = "http://www.koreatimes.co.kr/www/sublist_501_@.html"


    def get_page_urls(self, category):
        pages = []
        if category == "National":
            for i in range(1, 10):
                pages.append(self.National_root.replace("@", str(i)))
        elif category == "Sports":
            for i in range(1, 10):
                pages.append(self.Sports_root.replace("@", str(i)))
        elif category == "World":
            for i in range(1, 10):
                pages.append(self.World_root.replace("@", str(i)))
        else:
            raise Exception("Wrong category, only accept National, Sports and World.")

        urls_each_page = []
        for root_url in pages:
            source_code = requests.get(root_url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, features="html5lib")
            classes = soup.find_all(class_ = "list_article_headline HD")
            for one_class in classes:
                temp = one_class.find("a").get('href')

                if "photoview" not in temp : #사진만 있는 사진기사는 제외
                    urls_each_page.append("http://www.koreatimes.co.kr"+temp)
        return urls_each_page


    def crawal_and_save(self, category="National" or "Sports" or "World"):
        article_urls = self.get_page_urls(category)
        for i, url in enumerate(article_urls):
            source_code = requests.get(url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, features="html5lib")
            text = soup.find(id="startts")
            title = soup.find(class_="view_headline HD")

            f_title_url = open("C:/news_data/korea_times/" + category + "_title_url" + str(i) + ".txt", 'w',
                               encoding='UTF8')
            f_article = open("C:/news_data/korea_times/" + category + "_article" + str(i) + ".txt", 'w',
                             encoding='UTF8')

            if text is None:
                print(i, " article is error")
                f_title_url.write("error page" + "@" + url)
                f_title_url.close()

                f_article.write("error page")
                f_article.close()

            else:
                print("The Korea Times "+category+str(i),url)
                f_title_url.write(title.get_text() + "@" + url)
                f_title_url.close()

                f_article.write(text.get_text())
                f_article.close()


    def run_crawal(self, category="all"):
        if category == "all":
            self.crawal_and_save("National")
            self.crawal_and_save("Sports")
            self.crawal_and_save("World")
        else:
            self.crawal_and_save(category)
        print("(The Korea Times)crawalling for " +category+ " is done")

class Crawaler_Korea_Herald():
    def __init__(self):
        #category 별로 root 사이트 정의
        self.National_root = "http://www.koreaherald.com/list.php?ct=020100000000&ctv=0&np=@"
        self.Sports_root = "http://www.koreaherald.com/list.php?ct=020500000000&ctv=0&np=@"
        self.World_root = "http://www.koreaherald.com/list.php?ct=021200000000&ctv=0&np=@"

    def get_page_urls(self, category):
        pages = []
        if category == "National":
            for i in range(1, 10):
                pages.append(self.National_root.replace("@", str(i)))
        elif category == "Sports":
            for i in range(1, 10):
                pages.append(self.Sports_root.replace("@", str(i)))
        elif category == "World":
            for i in range(1, 10):
                pages.append(self.World_root.replace("@", str(i)))
        else:
            raise Exception("Wrong category, only accept National, Sports and World.")

        urls_each_page = []
        for root_url in pages:
            source_code = requests.get(root_url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, features="html5lib")
            classes = soup.find_all(class_ = "mb13")
            for one_class in classes:
                temp = one_class.find("a").get('href')
                if "photoview" not in temp : #사진만 있는 사진기사는 제외
                    urls_each_page.append("http://www.koreaherald.com"+temp)


        return urls_each_page


    def crawal_and_save(self, category="National" or "Sports" or "World"):
        article_urls = self.get_page_urls(category)
        for i, url in enumerate(article_urls):
            source_code = requests.get(url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, features="html5lib")
            text = soup.find(id="articleText")
            title = soup.find(class_="fontTitle6 mb16")

            if text is None:
                print(i, " article is error")
                continue #오류나서 아무것도 없는 페이지는 그냥 넘어간다.

            f_title_url = open("C:/news_data/korea_herald/"+category+"_title_url" + str(i) + ".txt", 'w', encoding='UTF8')
            print("The Korea Herald " + category + str(i), url)
            f_title_url.write(title.get_text()+"@"+url)
            f_title_url.close()

            f_article = open("C:/news_data/korea_herald/"+category+"_article"+ str(i)+".txt", 'w', encoding='UTF8')
            f_article.write(text.get_text())
            f_article.close()

    def run_crawal(self, category="all"):
        if category == "all":
            self.crawal_and_save("National")
            self.crawal_and_save("Sports")
            self.crawal_and_save("World")
        else:
            self.crawal_and_save(category)
        print("(The Korea Herald)crawalling for " +category+ " is done")

if __name__ == "__main__":
    print("starting crawaler..............")
    crawaler_t = Crawaler_Korea_Times()
    crawaler_h = Crawaler_Korea_Herald()
    crawaler_h.run_crawal()
    crawaler_t.run_crawal()





