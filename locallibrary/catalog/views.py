from django.db.models.fields import json
from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .models import Book, Author, BookInstance, Genre

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from datetime import datetime
from rest_framework import exceptions


@csrf_exempt
def time_now(request):
    print(request.__dict__)
    current_time = datetime.now().time()
    if request.method == 'POST':
        return JsonResponse({'time': current_time})

    elif request.method == 'GET':
        if request.GET['target'] == 'time':
            return JsonResponse({'time': current_time})

    else:
        return JsonResponse({'detail': 'invalid parameter'}, status=400)


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применён по умолчанию.
    num_genre = Genre.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    #
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5]  # Получить 5 книг, содержащих 'war' в заголовке


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author
