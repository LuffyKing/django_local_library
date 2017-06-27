from django.db import models
from django.urls import reverse
import uuid
from datetime import date
from django.contrib.auth.models import User
# Create your models here.


class Genre(models.Model):
    """
    Model representing a book genre
    """
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction, French Poetry etc.')
    def __str__(self):
        """
        String for representing the Model object
        :return:
        """
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.TextField('ISBN',max_length=13,help_text='13 character')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ','.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = 'Genre'


class Language(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        return self.name


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
                ('d', 'Maintenace'),
                ('o', 'On loan'),
                ('a', 'Available'),
                ('r', 'Reserved'),
                   )
    status = models.CharField(max_length=1,choices=LOAN_STATUS,blank=True,default='d',help_text='Book availability')
    borrower = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned","Set book as returned"),)

    def __str__(self):
        return '%s (%s)' % (self.id,self.book.title)

    @property
    def is_overdue(self):
        if self.due_back:
            if date.today() > self.due_back:
                return True
        return False


class Author(models.Model):
    firstName = models.CharField(max_length=100, verbose_name='First Name')
    lastName = models.CharField(max_length=100, verbose_name='Last Name')
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died',null=True,blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '%s, %s'%(self.lastName, self.firstName)
