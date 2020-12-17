from .models import Note


def notes_count(request):
    if request.user.is_authenticated:
        notes_count = request.user.notes.count()
        return {'notes_count': notes_count}
    else:
        return {'notes_count': None}
