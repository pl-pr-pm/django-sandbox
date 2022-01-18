from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest
from django.urls import resolve
from snippets.views import top, snippet_new, snippet_edit, snippet_detail
from django.contrib.auth import get_user_model
from snippets.models import Snippet

UserModel = get_user_model()

class TopPageRenderSnippetsTest(TestCase):
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

  def test_should_returns_snippet_title(self):
    request = RequestFactory().get("/")
    request.user = self.user
    response = top(request)
    self.assertContains(response,self.snippet.title)
  
  def test_should_return_username(self):
    request = RequestFactory().get("/")
    request.user = self.user
    response = top(request)
    self.assertContains(response, self.user.username)

