from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest
from django.urls import resolve
from snippets.views import top, snippet_new, snippet_edit, snippet_detail
from django.contrib.auth import get_user_model
from snippets.models import Snippet

UserModel = get_user_model()

class SnippetDetailTest(TestCase):
  def setUp(self):
    self.user = UserModel.objects.create(
      username = "test_user",
      email="test2@test.com",
      password="pass",
    )
    self.snippet = Snippet.objects.create(
      title="title1",
      code="print('heelo')",
      desciption="desciption",
      created_by=self.user,
    )

  def test_should_use_expected_template(self):
    response = self.client.get('/snippets/%s/' % self.snippet.id)
    self.assertTemplateUsed(response, "snippets/snippet_detail.html")
  
  def test_top_page_returns_200_and_expected_heading(self):
    response = self.client.get("/snippets/%s/" % self.snippet.id)
    self.assertContains(response, self.snippet.title, status_code=200)

