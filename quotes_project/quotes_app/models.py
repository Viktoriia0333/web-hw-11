from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=150, unique=True)
    born_date = models.CharField(max_length=100)
    born_location = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.fullname


class Quote(models.Model):
    quote = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.CharField(max_length=250)  # Можна зберігати як CSV

    def __str__(self):
        return self.quote[:50]

