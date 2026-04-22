import pytest

from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm


pytestmark = pytest.mark.django_db

HOME_URL = reverse('news:home')


def test_news_count(client, news_list):
    response = client.get(reverse('news:home'))
    object_list = response.context['news_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_list):
    response = client.get(reverse('news:home'))
    object_list = response.context['news_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, news, comments_list, detail_url):
    response = client.get(detail_url)
    assert 'news' in response.context
    news_obj = response.context['news']
    comments = news_obj.comment_set.all()
    all_timestamps = [comment.created for comment in comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_anonymous_client_has_no_form(client, news, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, news, detail_url):
    response = author_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
