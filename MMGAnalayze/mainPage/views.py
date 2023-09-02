from django.shortcuts import render
from django.views import View


class MainPage(View):
    def get(self, request):
        return render(request, 'main/mainPage.html')

class MapPage(View):
    def get(self, request):
        return render(request, 'proba_interactive_MAP.html')

class FeedBackPage(View):
    def get(self, request):
        return render(request, 'main/feedback.html')
