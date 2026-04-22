import pytest

from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm


pytestmark = pytest.mark.django_db

HOME_URL = reverse('news:home')


def test_news_count(client, news_list):
    response = client.get(HOME_URL)
    object_list = response.context['news_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_list):
    response = client.get(HOME_URL)
    object_list = response.context['news_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


# @pytest.mark.parametrize(
#     'parametrized_client, note_in_list',
#     (
#         (pytest.lazy_fixture('author_client'), True),
#         (pytest.lazy_fixture('not_author_client'), False),
#     )
# )
# def test_note_in_list_for_author(note, client, note_in_list):
#     url = reverse('notes:list')
#     response = client.get(url)
#     object_list = response.context['object_list']
#     assert note in object_list is note_in_list


# @pytest.mark.parametrize(
#         'name, args',
#         (
#         ('notes:add', None),
#         ('notes:edit', pytest.lazy_fixture('slug_for_args'))
#     )
# )
# def test_create_note_page_contains_form(author_client, name, args):
#     url = reverse('notes:add')
#     response = author_client.get(url)
#     assert 'form' in response.context
#     assert isinstance(response.contest['form'], NoteForm)
