from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import datetime

from catalog.models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookForm


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


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
        Funcao view para permitir que bibliotecarios renovem reservas de livros
    :param request: requisicao http do cliente
    :param pk: primary key da copia do livro a ser renovado
    :return: Formulario de revalidacao ou redireciona para a pagina de livros reservados
    """
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':

        # Cria uma instancia de formulario e popula com as informacoes do POST
        form = RenewBookForm(request.POST)

        if form.is_valid():

            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('see-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='r').order_by('due_back')


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}
    permission_required = 'catalog.can_alter_author'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.can_alter_author'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_alter_author'


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_alter_books'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_alter_books'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_alter_books'
