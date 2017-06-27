from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import  login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import RenewBookForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author
# Create your views here.

@permission_required('catalog.can_mark_returned')
def renewBookLibrarian(request,pk):
    book_inst = get_object_or_404(BookInstance,pk=pk)
    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date':proposed_renewal_date})
    return render(request,'catalog/book_renew_librarian.html',{'form':form,'bookinst':book_inst})
@login_required
def index(request):
    numBooks = Book.objects.all().count()
    numInstances = BookInstance.objects.all().count()
    numInstancesAvailable = BookInstance.objects.filter(status__exact='a').count()
    numAuthors = Author.objects.count()
    numVisits = request.session.get('num_visits', 0)
    request.session['num_visits'] = numVisits+1

    return render(request,'index.html',context={'numBooks':numBooks,'numInstances':numInstances,
                                                'numInstancesAvailable':numInstancesAvailable,
                                                'numAuthors':numAuthors,'numVisits':numVisits,
                                                })


class BookListView(LoginRequiredMixin,generic.ListView):
    model = Book
    #context_object_name = 'my_book_list' # your own name for the list as a template variable
    #queryset = Book.objects.all()
    #template_name = 'book_list.html'
    paginate_by = 2


class BookDetailView(LoginRequiredMixin,generic.DetailView):
    model = Book


class AuthorListView(LoginRequiredMixin,generic.ListView):
    model = Author


class AuthorDetailView(LoginRequiredMixin,generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class BorrowedBooksListStaffView(LoginRequiredMixin,generic.ListView,PermissionRequiredMixin):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_staffview.html'
    paginate_by = 10
    context_object_name = 'borrowedbookslist'
    permission_required = 'can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.all()


class AuthorCreate(CreateView,LoginRequiredMixin,PermissionRequiredMixin):
    model = Author
    fields = '__all__'
    permission_required = 'can_mark_returned'
#    initial = {'date_of_death':'12/10/2016'}


class AuthorUpdate(UpdateView,LoginRequiredMixin,PermissionRequiredMixin):
    model = Author
    permission_required = 'can_mark_returned'
    fields = ['firstName','lastName','date_of_birth','date_of_death']


class AuthorDelete(DeleteView,LoginRequiredMixin,PermissionRequiredMixin):
    model = Author
    permission_required = 'can_mark_returned'
    success_url = reverse_lazy('authors')