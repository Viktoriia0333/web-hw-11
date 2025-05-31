from collections import Counter

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Author, Quote
from .forms import AuthorForm, QuoteForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


def home(request):
    print("Starting home view processing.")
    quotes_data = []

    try:
        quotes = Quote.objects.all().select_related('author')
        print(f"Fetched {len(quotes)} quotes from database.")
    except Exception as e:
        print(f"Error fetching quotes: {e}")
        quotes = []

    all_tags = []
    for quote_obj in quotes:
        tags_list = []
        if quote_obj.tags:
            processed_tags = [tag.strip() for tag in quote_obj.tags.split(',') if tag.strip()]
            tags_list = processed_tags
            all_tags.extend(processed_tags)

        quotes_data.append({
            'quote': quote_obj.quote,
            'author': quote_obj.author,
            'tags_processed': tags_list,
        })

    print(f"Collected {len(all_tags)} tags in total.")
    tag_counts = Counter(all_tags)
    top_ten_tags = sorted(tag_counts.items(), key=lambda item: (-item[1], item[0]))[:10]

    top_ten_tags_plain = [
        {'name': tag, 'count': count}
        for tag, count in top_ten_tags
    ]
    print(f"Top 10 tags: {top_ten_tags_plain}")

    print("Home view processing finished.")
    return render(request, 'home1.html', {
        'quotes': quotes_data,
        'top_ten_tags': top_ten_tags_plain,
    })


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AuthorForm()
    return render(request, 'add_author.html', {'form': form})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = QuoteForm()
    return render(request, 'add_quote.html', {'form': form})


def author_detail(request, pk):
    author = Author.objects.get(pk=pk)
    return render(request, 'author_detail.html', {'author': author})


def tag_quotes(request, tag_name):
    quotes_with_tag = Quote.objects.filter(tags__icontains=tag_name).select_related('author')

    quotes_data = []
    for quote_obj in quotes_with_tag:
        tags_list = []
        if quote_obj.tags:
            processed_tags = [tag.strip() for tag in quote_obj.tags.split(',') if tag.strip()]
            tags_list = processed_tags

        quotes_data.append({
            'quote': quote_obj.quote,
            'author': quote_obj.author,
            'tags_processed': tags_list,
        })

    return render(request, 'home1.html', {
        'quotes': quotes_data,
        'selected_tag': tag_name,
    })


class MyPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    subject_template_name = 'registration/password_reset_subject.txt'
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
