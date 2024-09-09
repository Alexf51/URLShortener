from django.contrib.auth.models import User
import random
import string
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import URL
from .forms import URLForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.db import DataError
from django.core.exceptions import ValidationError

def home(request):
    return render(request, 'shortener/home.html')

def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@login_required
def create_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        short_url = generate_short_url()
        try:
            # Проверка длины оригинального URL
            if len(original_url) > 200:
                messages.error(request, "URL слишком длинный, максимальная длина 200 символов.")
                return render(request, 'shortener/create_short_url.html', {'form': URLForm()})

            # Создание записи в базе данных
            URL.objects.create(user=request.user, original_url=original_url, short_url=short_url)
            messages.success(request, "Ссылка успешно создана!")
            return redirect('url_list')

        except DataError:
            messages.error(request, "Ошибка: данные не соответствуют формату.")
            return render(request, 'shortener/create_short_url.html', {'form': URLForm()})
        except ValidationError as e:
            messages.error(request, f"Ошибка валидации: {', '.join(e.messages)}")
            return render(request, 'shortener/create_short_url.html', {'form': URLForm()})
        except Exception as e:
            messages.error(request, f"Произошла ошибка: {str(e)}")
            return render(request, 'shortener/create_short_url.html', {'form': URLForm()})
    else:
        form = URLForm()
    return render(request, 'shortener/create_short_url.html', {'form': form})

def url_list(request):
    urls = URL.objects.all().order_by('-created_at')  # Сортируем по времени создания
    return render(request, 'shortener/url_list.html', {'urls': urls})

def url_list_ajax(request):
    urls = URL.objects.all().order_by('-created_at')  # Сортируем по времени создания
    return render(request, 'shortener/url_list_ajax.html', {'urls': urls})

def url_detail(request, pk):
    # urls = URL.objects.get(pk=pk)
    url = get_object_or_404(URL, pk=pk)
    return render(request, 'shortener/url_detail.html', {'url': url})

def redirect_to_original_url(request, short_url):
    short_url_obj = cache.get(f'short_url_{short_url}')
    if short_url_obj is None:
        short_url_obj = get_object_or_404(URL, short_url=short_url)
        cache.set(f'short_url_{short_url}', short_url_obj, 60 * 60)  # Кэшировать на 1 час

    with transaction.atomic():
        short_url_obj.clicks += 1
        short_url_obj.save()

    # Сохранить последние переходы в кэш
    last_redirects = cache.get('last_redirects', set())
    last_redirects.add(short_url)
    if len(last_redirects) > 10:  # Ограничить количество последних переходов до 10
        last_redirects.pop()
    cache.set('last_redirects', last_redirects, 60 * 60)  # Кэшировать на 1 час

    return redirect(short_url_obj.original_url)

def last_redirects(request):
    last_redirects = cache.get('last_redirects', set())
    urls = []
    for short_url in last_redirects:
        try:
            url = URL.objects.get(short_url=short_url)
            urls.append(url)
        except URL.DoesNotExist:
            # Обработка ситуации, когда запись не найдена
            pass
    return render(request, 'shortener/last_redirects.html', {'urls': urls})

@login_required
def admin_custom_index(request):
    urls = URL.objects.all()
    return render(request, 'shortener/admin_custom_index.html', {'urls': urls})

@login_required
def user_list(request):
    users = User.objects.all()
    urls = URL.objects.all().order_by('-created_at')
    return render(request, 'shortener/user_list.html', {'users': users})

@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    urls = URL.objects.filter(user=user)
    return render(request, 'shortener/user_detail.html', {'user': user, 'urls': urls})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для пользователя {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')