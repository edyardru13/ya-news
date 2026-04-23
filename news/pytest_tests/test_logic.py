from http import HTTPStatus

from news.models import Comment


def test_anonymous_user_cant_create_comment(client, form_data, detail_url):
    comments_count_before = Comment.objects.count()
    client.post(detail_url, data=form_data)
    assert Comment.objects.count() == comments_count_before


def test_user_can_create_comment(
    reader_client,
    reader,
    news,
    form_data,
    detail_url,
    url_to_comments
):
    comments_count_before = Comment.objects.count()

    response = reader_client.post(detail_url, data=form_data)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == url_to_comments
    assert Comment.objects.count() == comments_count_before + 1

    comment = Comment.objects.get(author=reader, news=news)

    assert comment.text == form_data['text']
    assert comment.author == reader
    assert comment.news == news


def test_user_cant_use_bad_words(
        reader_client,
        detail_url,
        bad_words,
        bad_words_data,
        warning
):
    comments_count_before = Comment.objects.count()

    response = reader_client.post(detail_url, data=bad_words_data)

    form = response.context['form']
    assert 'text' in form.errors
    assert form.errors['text'] == [warning]

    assert Comment.objects.count() == comments_count_before


def test_author_can_delete_comment(
    author_client,
    url_to_comments,
    delete_comment_url
):
    comments_count_before = Comment.objects.count()

    response = author_client.post(delete_comment_url)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == url_to_comments

    assert Comment.objects.count() == comments_count_before - 1


def test_user_cant_delete_comment_of_another_user(
    reader_client,
    url_to_comments,
    delete_comment_url
):
    comments_count_before = Comment.objects.count()

    response = reader_client.post(delete_comment_url)
    assert response.status_code == HTTPStatus.NOT_FOUND

    assert Comment.objects.count() == comments_count_before


def test_author_can_edit_comment(
    author_client,
    url_to_comments,
    edit_comment_url,
    new_form_data,
    comment
):
    response = author_client.post(edit_comment_url, data=new_form_data)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == url_to_comments

    comment.refresh_from_db()

    assert comment.text == new_form_data['text']


def test_user_cant_edit_comment_of_another_user(
    reader_client,
    edit_comment_url,
    form_data,
    new_form_data,
    comment
):
    response = reader_client.post(edit_comment_url, data=new_form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND

    comment.refresh_from_db()

    assert comment.text == form_data['text']
