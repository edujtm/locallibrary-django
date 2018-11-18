from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
import uuid

# Create your models here.


class Genre(models.Model):
    """
        Modelo que representa um genero de livro.
    """
    name = models.CharField(max_length=200, help_text='Digite um genero de livro (e.g. Ficcao Cientifica)')

    def __str__(self):
        """
            String que representa o modelo de generos.
        """
        return self.name


class Book(models.Model):
    """
        Modelo que representa um livro (mas não uma cópia específica dele presente na biblioteca).
    """
    title = models.CharField(max_length=200)

    # Relacao One to Many entre os livros e os autores - O livro possuira um autor mas o autor poderá ter vários livros
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Digite uma breve descricao do livro')
    isbn = models.CharField('ISBN', max_length=13, help_text='<a href="https://www.isbn-international.org/content/what-isbn">Numero ISBN</a> de 13 caracteres.')

    genre = models.ManyToManyField(Genre, help_text='Selecione um genero para este livro.')

    def __str__(self):
        """
            String que representa o modelo de livros
        """
        return self.title

    def get_absolute_url(self):
        """
            Retorna a url de acesso aos detalhes do livro selecionado.
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ", ".join((genre.name for genre in self.genre.all()[:3]))

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """
        Modelo que representa um copia fisica do livro.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID exclusivo para esta cópia do livro em toda a biblioteca')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    written_in = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    LOAN_STATUS = (
        ('m', 'Manutencao'),
        ('e', 'Emprestado'),
        ('d', 'Disponivel'),
        ('r', 'Reservado'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Disponibilidade do livro')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """
            String que representa o modelo de instancia do livro.
        """
        return f'{self.id} ({self.book.title})'

    @property
    def is_overduew(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    """
        Modelo que representa um autor.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
    
    def get_absolute_url(self):
        """
            Retorna a url de acesso aos detalhes do autor.
        """
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        """
            String de representacao do autor.
        """
        return f'{self.last_name}, {self.first_name}'


class Language(models.Model):
    """
        Modelo que representa a linguagem em que o livro foi escrito.
    """
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        """
            Retorna uma String que representa o livro.
        """
        return f'{self.name} ({self.country})'
