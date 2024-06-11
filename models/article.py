from database.connection import get_db_connection
from models.magazine import Magazine
from models.author import Author

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        """
        Initializes an Article object with provided attributes.
        """
        self.id = id
        self._title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        if self.id is None:
            self.create_db_entry()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if isinstance(title, str) and 5 <= len(title) <= 50:
            self._title = title
        else:
            raise ValueError("Title must be a string between 5 and 50 characters.")

    @property
    def author(self):
        """
        Property method to retrieve the author of the article.
        """
        author_info = self.get_author_information_by_id(self.author_id)
        if author_info:
            return Author(author_info["id"], author_info['name'])
        return None

    @property
    def magazine(self):
        """
        Property method to retrieve the magazine of the article.
        """
        magazine_info = self.get_magazine_information_by_id(self.magazine_id)
        if magazine_info:
            return Magazine(magazine_info["id"], magazine_info['name'], magazine_info['category'])
        return None

    def create_db_entry(self):
        """
        Creates a database entry for the article if it doesn't already exist.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', 
            (self.title, self.content, self.author_id, self.magazine_id)
        )
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @staticmethod
    def get_magazine_information_by_id(magazine_id):
        """
        Retrieves information about a magazine from the database based on its ID.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (magazine_id,))
        magazine_info = cursor.fetchone()
        conn.close()
        return magazine_info

    @staticmethod
    def get_author_information_by_id(author_id):
        """
        Retrieves information about an author from the database based on their ID.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (author_id,))
        author_info = cursor.fetchone()
        conn.close()
        return author_info

    def __repr__(self):
        """
        Returns a string representation of the article, showing title, author, and magazine.
        """
        magazine_info = self.get_magazine_information_by_id(self.magazine_id)
        magazine_name = magazine_info['name'] if magazine_info else "No magazine"
        author_info = self.get_author_information_by_id(self.author_id)
        author_name = author_info['name'] if author_info else "No author"
        return f'Article: {self.title} | Author: {author_name} | Magazine: {magazine_name}'
