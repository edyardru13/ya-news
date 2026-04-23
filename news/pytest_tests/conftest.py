from datetime import datetime, timedelta

import pytest

from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.forms import BAD_WORDS, WARNING
from news.models import Comment, News


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


@pytest.fixture
def news_id(news):
    return (news.id,)


@pytest.fixture
def comment_id(comment):
    return (comment.id,)


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Лев Толстой')


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Читатель простой')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст'
    )


@pytest.fixture
def comment(news, author, form_data):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text=form_data['text']
    )
    return comment


@pytest.fixture
def news_list():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    return News.objects.bulk_create(all_news)


@pytest.fixture
def comments_list(news, author):
    now = timezone.now()
    comments = []

    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
        comments.append(comment)

    return comments


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def url_to_comments(detail_url):
    return detail_url + '#comments'


@pytest.fixture
def delete_comment_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def edit_comment_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def form_data():
    return {'text': 'Текст комментария'}


@pytest.fixture
def new_form_data():
    return {'text': 'Обновлённый комментарий'}


@pytest.fixture
def bad_words_data():
    return {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}


@pytest.fixture
def warning():
    return WARNING


@pytest.fixture
def bad_words():
    return BAD_WORDS
