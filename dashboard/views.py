import math
from datetime import datetime, timedelta, timezone
from django.shortcuts import redirect, render
from news.models import Headline, UserProfile

from notepad.forms import NoteModelForm
from notepad.models import Note

def home(request):
    user_p = UserProfile.objects.filter(user = request.user).first()
    now = datetime.now(timezone.utc)
    time_difference = now - user_p.last_scrape
    time_diff_in_hours = time_difference / timedelta(minutes=60)
    next_scrape = 24 - time_diff_in_hours

    if time_diff_in_hours < 24:
        hide_me = True
    else:
        hide_me = False

    headlines = Headline.objects.all()
    notes = Note.objects.filter(user=request.user)

    form = NoteModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect('/home')

    context = {
        'form': form,
        'notes_list':notes,
        'object_list':headlines,
        'hide_me':hide_me,
        'next_scrape': math.ceil(next_scrape),
    }
    return render(request, "news/home.html", context)