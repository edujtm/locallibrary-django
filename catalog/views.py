from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
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

    # Numero de visitas para esta view.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_sophie': num_sophie,
        'num_science': num_science,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


@permission_required('catalog.can_mark_returned')
def see_all_borrowed_books(request):
    """
        Metodo disponivel apenas para bibliotecarios
    :param request: A requisicao http enviada pelo cliente
    :return: pagina html renderizada.
    """

    borrowed_books = BookInstance.objects.filter(status__exact='r')

    context = {
        "borrowed_books": borrowed_books,
    }

    return render(request, 'catalog/librarian_borrowed_bookinstance.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='r').order_by('due_back')
