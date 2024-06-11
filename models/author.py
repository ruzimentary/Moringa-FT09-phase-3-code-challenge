from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError("The ID must be an integer.")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("The name must be a string.")
        if len(value) == 0:
            raise ValueError("The name cannot be empty.")
        if hasattr(self, '_name'):
            raise AttributeError("The name attribute cannot be modified once set.")
        self._name = value

    @property
    def articles(self):
        """
        Retrieves a list of Article objects authored by this author.
        """
        from models.article import Article
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles
            WHERE articles.author_id = ?
        ''', (self.id,))
        articles_data = cursor.fetchall()
        connection.close()
        return [Article(article["id"], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in articles_data] if articles_data else []

    @property
    def magazines(self):
        """
        Retrieves a list of Magazine objects that feature articles by this author.
        """
        from models.magazine import Magazine
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT DISTINCT magazines.id, magazines.name, magazines.category
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self.id,))
        magazines_data = cursor.fetchall()
        connection.close()
        return [Magazine(magazine["id"], magazine['name'], magazine['category']) for magazine in magazines_data] if magazines_data else []

    def __repr__(self):
        article_titles = "; ".join([article.title for article in self.articles]) if self.articles else "No articles"
        magazine_names = "; ".join([magazine.name for magazine in self.magazines]) if self.magazines else "No magazines"
        return f'AUTHOR: {self.name} || ID: {self.id} || MAGAZINES: {magazine_names} || ARTICLES: {article_titles}'
