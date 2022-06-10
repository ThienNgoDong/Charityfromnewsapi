import sqlite3
import newspaper
from newspaper import Article
import nltk


def get_all(query):
    conn = sqlite3.connect("data/newsdb.db")
    data = conn.execute(query).fetchall()
    conn.close()

    return data


def get_news_by_id(news_id):
    conn = sqlite3.connect("data/newsdb.db")
    sql = '''
    SELECT N.subject, N.description, N.image, N.original_url, c.name, c.url
    FROM news N INNER JOIN category C ON N.category_id=C.id 
    WHERE id=?
    '''
    news = conn.execute(sql, (news_id,)).fetchone()
    conn.close()

    return news


def add_news(conn, url, category_id):
    sql = """
    INSERT INTO news(subject, description, image, original_url, category_id)
    VALUES (?, ?, ?, ?, ?)
    """
    article = Article(url)
    article.download()
    article.parse()

    conn.execute(sql, (article.title, article.text, article.top_image, article.url, category_id))
    conn.commit()


def get_news_url():
    cats = get_all("SELECT * FROM category")
    conn = sqlite3.connect("data/newsdb.db")
    for cat in cats:
        cat_id = cat[0]
        url = cat[2]
        cat_paper = newspaper.build(url)
        for article in cat_paper.articles:
            try:
                print("===", article.url)
                add_news(conn, article.url, cat_id)
            except Exception as ex:
                print("ERROR: " + str(ex))

    conn.close()


def test():
    cats = get_all("SELECT * FROM category")
    conn = sqlite3.connect("data/newsdb.db")
    for cat in cats:
        cat_id = cat[0]
        url = cat[2]
        cat_paper = newspaper.build(url)
        for article in cat_paper.articles:
            try:
                print("===", article.url)
                # add_news(conn, article.url, cat_id)
                article1 = Article(article.url)
                article1.download()
                article1.parse()
                check = article1.url.__contains__("tu-thien")
                print(check)
            except Exception as ex:
                print("ERROR: " + str(ex))

    conn.close()

    # article = Article("https://congan.com.vn/tu-thien/do-dang-viec-hoc-do-ung-thu-da-day_132163.html")
    # article.download()
    # article.parse()
    # # article.nlp()
    # t2 = article.url.__contains__("tu-thien")
    # print(t2)


def test2(pageIndex, pageSize):
    conn = sqlite3.connect("data/newsdb.db")
    query = """
    SELECT * 
    FROM( SELECT ROW_NUMBER() OVER(ORDER BY id) AS ROWNUMBER, 
    count(*) OVER() as TOTALNUMBERCOUNT,
    u.* from news u) post
    WHERE ROWNUMBER > ((:pageindex - 1) * :pagesize)
    AND ROWNUMBER < (:pageindex * :pagesize + 1); 
    """
    data = conn.execute(query, {"pageindex": pageIndex, "pagesize": pageSize}).fetchall()
    print(data)
    print(data.__len__())
    conn.close()
    return data


if __name__ == "__main__":
    test2(2, 6)
