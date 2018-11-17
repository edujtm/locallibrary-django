from django.shortcuts import render
from django.views import generic
from catalog.models import Book, Author, BookInstance, Genre


def index(request):
    """
        Função view da home do site.
    """

    # Gera contagems para os objetos principais
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Quantidade de livros disponíveis
    num_instances_available = BookInstance.objects.filter(status__exact='d').count()

    # Numero de livros com sophie no nome
    num_sophie = Book.objects.filter(title__icontains='sophie').count()

    num_science = Genre.objects.filter(name__icontains='science').count()

    # funcao all() implicita
    num_authors = Author.objects.count()

    context = {
        'num_books' : num_books,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_authors' : num_authors,
        'num_sophie': num_sophie,
        'num_science' : num_science,
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author
