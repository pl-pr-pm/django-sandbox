from django.http import HttpResponse,HttpResponseForbidden
from snippets.models import Snippet, Comment
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist

from snippets.forms import SnippetForm, CommentForm

def top(request):
  snippets = Snippet.objects.all()
  context = {"snippets": snippets}
  return render(request, "snippets/top.html", context)

@login_required
def snippet_new(request):
  if request.method == 'POST':
    form = SnippetForm(request.POST) #request.POST => form のパラメータ
    if form.is_valid():
      snippet = form.save(commit=False)
      snippet.created_by = request.user 
      snippet.save()
      return redirect('snippet_detail', snippet_id=snippet.pk)
  else:
    form = SnippetForm()
  return render(request, "snippets/snippet_new.html", {'form': form})

@login_required
def snippet_edit(request, snippet_id):
  snippet = get_object_or_404(Snippet, pk=snippet_id)
  if snippet.created_by_id != request.user.id:
    return HttpResponseForbidden("このスニペットは編集を許可されていません")

  if request.method == "POST":
    form = SnippetForm(request.POST, instance=snippet)# instanceに値を渡すと、フォーム画面のデフォルトの値になる
    if form.is_valid():
      form.save()
      return redirect('snippet_detail', snippet_id=snippet_id)
  else:
    form = SnippetForm(instance=snippet)
  return render(request, 'snippets/snippet_edit.html', {'form': form})

def snippet_detail(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    try:
      comments = Comment.objects.filter(commented_to=snippet.id)
    except ObjectDoesNotExist:
      comments = None
    print(comments)
    context = {"snippet": snippet, "comments": comments}
    return render(request, "snippets/snippet_detail.html", context)

def comment_new(request, snippet_id):
  print (snippet_id)
  print(request.body)
  if request.method == 'POST':
      form = CommentForm(request.POST)
      target_snippet = Snippet.objects.get(pk=snippet_id)
      if form.is_valid():
        comment = form.save(commit=False)
        comment.commented_to = target_snippet
        comment.commented_by = request.user
        comment.save()
      return redirect('snippet_detail', snippet_id=target_snippet.pk)