from django.shortcuts import render, get_object_or_404
from .models import Language, Level

def language_list(request):
    languages = Language.objects.all()
    return render(request, 'englishlearn/language_list.html', {'languages': languages})

def level_list(request, language_id):
    language = get_object_or_404(Language, id=language_id)
    levels = language.levels.all()
    return render(request, 'englishlearn/level_list.html', {'language': language, 'levels': levels})

def level_details(request, level_id):
    level = get_object_or_404(Level, id=level_id)
    resources = level.learning_resources.split(',')
    return render(request, 'englishlearn/level_details.html', {'level': level, 'resources': resources})

def home_view(request):
    return render(request, 'home.html')
# Create your views here.
