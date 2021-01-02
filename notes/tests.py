from django.test import Client, TestCase
from django.urls import reverse

from .models import Note
from users.models import CustomUser


class TestNotes(TestCase):
    
    AUTHOR_PK = 2
    NOTE_PK = 1
    URL_LOGIN = reverse('users:login')
    URL_NEW_NOTE = reverse('notes:note_new')
    URL_NOTES_LIST = reverse('notes:notes_list', args=(AUTHOR_PK,))
    URL_EDIT_NOTE = reverse('notes:note_edit', args=(NOTE_PK,))
    URL_DELETE_NOTE = reverse('notes:note_delete', args=(NOTE_PK,))

    TEST_PAGES = (URL_NEW_NOTE, URL_NOTES_LIST, 
                  URL_EDIT_NOTE, URL_DELETE_NOTE)
    
    def setUp(self):
        self.client_unlogged = Client()
        self.client_logged = Client()
        self.user = CustomUser.objects.create_user(
            username='sarah',
            email='1@g.ru',
            password='123456'
        )
        self.client_logged.force_login(self.user)


    def test_unlogged_user_not_have_access(self):
        """
        Проверить, что аноним не может попасть на запрещенные страницы.
        Его должно директить на страницу входа (login)
        """
        for page in self.TEST_PAGES:
            redirect_url = (f"{self.URL_LOGIN}?next={page}")
            response = self.client_unlogged.get(page, follow=True)

            with self.subTest(failed_page=page):
                self.assertRedirects(
                    response, redirect_url, status_code=302,
                    target_status_code=200,
                    fetch_redirect_response=True
                )


    def test_logged_user_can_create_and_edit_own_post(self):
        """
        Проверить, что авторизованный пользователь может создавать
        и редактировать записи.
        """
        note_request_args = (
            ("новая запись", self.URL_NEW_NOTE),
            ("отредактированная запись", self.URL_EDIT_NOTE),
        )
        for text, url in note_request_args:
            data = {"text": text, }
            self.client_logged.post(url, data=data, follow=True)
            with self.subTest(failed_url=url):
                # Проверяем: БД должна появиться запись с теми же атрибутами
                self.assertEqual(Note.objects.values("text").first(),
                                 data)

