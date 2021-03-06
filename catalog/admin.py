from django.contrib import admin
from .models import Author, Genre, Book, BookInstance
# Register your models here.
#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('lastName', 'firstName', 'date_of_birth', 'date_of_death')
    fields = ['firstName','lastName' , ('date_of_birth','date_of_death')]
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','display_genre')
    inlines = [BooksInstanceInline]
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('book','status','borrower','due_back','id')
    fieldsets = (
        (None, {
         'fields':('book','imprint','id')
        }),
        ('Availability',{
            'fields':('status','due_back','borrower')
        }),
    )
admin.site.register(Author, AuthorAdmin)
