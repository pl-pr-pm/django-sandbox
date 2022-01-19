from django.http import HttpResponse,HttpResponseForbidden
from snippets.models import Snippet
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required

from snippets.forms import SnippetForm

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
    context = {"snippet": snippet}
    return render(request, "snippets/snippet_detail.html", context)