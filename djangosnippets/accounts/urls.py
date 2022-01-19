# LoginView, LogoutViewはdjangoで用意しているクラスビュー
# クラスビューは .as_viewを呼び出すと、ビュー関数のようなものが生成される
# オプションの指定で、処理内容を編集できる
from django.contrib.auth.views import LoginView, LogoutView 
from django.urls import path

urlpatterns = [
  path('login', LoginView.as_view(
    redirect_authenticated_user=True,
    template_name='accounts/login.html'
  ), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
]