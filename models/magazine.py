from database.connection import get_db_connection

class Magazine:
    def __init__(self, magazine_id, magazine_name, magazine_category):
        self._id = magazine_id
        self._name = magazine_name
        self._category = magazine_category

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError("ID must be an integer.")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise TypeError("Name must be a string of 2 to 16 characters in length.")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            raise TypeError("Category must be a non-empty string.")

    @property
    def articles(self):
        """
        Retrieves articles published in this magazine.
        """
        from models.article import Article
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT id, title, content, author_id, magazine_id FROM articles WHERE magazine_id = ?
        ''', (self.id,))
        article_data = cursor.fetchall()
        connection.close()
        return [Article(article['id'], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in article_data] if article_data else []

    @property
    def contributors(self):
        """
        Fetches a list of authors who have contributed to this magazine.
        """
        from models.author import Author
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.id, authors.name FROM authors
            JOIN articles ON authors.id = articles.author_id WHERE articles.magazine_id = ?
        ''', (self.id,))
        author_data = cursor.fetchall()
        connection.close()
        return [Author(author['id'], author['name']) for author in author_data] if author_data else []

    def article_titles(self):
        return [article.title for article in self.articles]

    def contributing_authors(self):
        contributors = [author for author in self.contributors if len([article for article in self.articles if article.author_id == author.id]) > 2]
        return contributors if contributors else None

    def __repr__(self):
        contributor_names = "; ".join([contributor.name for contributor in self.contributors]) if self.contributors else "None"
        key_contributors = "; ".join([contributor.name for contributor in self.contributing_authors()]) if self.contributing_authors() else "None"
        titles_of_articles = "; ".join([article.title for article in self.articles]) if self.articles else "None"
        return f'MAGAZINE: {self.name} | ID: {self.id} | ARTICLES: {titles_of_articles} | CONTRIBUTORS: {contributor_names} | KEY CONTRIBUTORS: {key_contributors}'
