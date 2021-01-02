from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import DeleteView, ListView, UpdateView
from django.urls import reverse_lazy

from .models import Note


CustomUser = get_user_model()


def page_not_found(request, exception):
    return render(
        request,
        '404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, '500.html', status=500)


def permission_denied(request, exception):
    return render(request, '403.html', status=403)


class NoteListView(UserPassesTestMixin, ListView):
    template_name = 'notes.html'
    paginate_by = 10

    def test_func(self):
        author = get_object_or_404(CustomUser, pk=self.kwargs['author_id'])
        return (self.request.user.is_authenticated and
                self.request.user == author)

    def get_queryset(self):
        author = get_object_or_404(CustomUser, pk=self.kwargs['author_id'])
        qs = author.notes.select_related()
        return qs


class NoteCreateUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    template_name = 'note_new.html'
    fields = ['text']
    success_url = reverse_lazy('notes:notes_list')

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NoteCreateUpdateView, self).form_valid(form)

    def get_success_url(self):
        author_id = self.object.author.id
        return reverse_lazy('notes:notes_list',
                            kwargs={'author_id': author_id})


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'note_delete.html'

    def get_success_url(self):
        success_url = reverse_lazy(
            'notes:notes_list', kwargs={'author_id': self.object.author.pk}
        )
        return success_url
