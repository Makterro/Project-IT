from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *


def research_list(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    research_list = Research.objects.filter(building=building)
    context = {'building': building, 'research_list': research_list, 'building_id': building_id}
    return render(request, 'analyze_dash/research_list.html', context)


def research_detail(request, research_id):
    research = get_object_or_404(Research, id=research_id)
    if request.method == 'POST':
        form = ResearchFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.research = research
            file_instance.save()
            return redirect('research_detail', research_id=research.id)
    else:
        form = ResearchFileForm()

    files = ResearchFile.objects.filter(research=research_id)

    context = {
        'research': research,
        'form': form,
        'files': files
    }
    return render(request, 'analyze_dash/research_detail.html', context)


def create_research(request, building_id):
    building = Building.objects.get(pk=building_id)

    if request.method == 'POST':
        form = ResearchForm(request.POST)
        file_form = ResearchFileForm(request.POST, request.FILES)
        if form.is_valid() and file_form.is_valid():
            research = form.save(commit=False)
            research.building = building
            research.save()

            file_instance = file_form.save(commit=False)
            file_instance.research = research
            file_instance.save()

            return redirect('research_list', building_id=building_id)
    else:
        form = ResearchForm()
        file_form = ResearchFileForm()

    context = {'form': form, 'file_form': file_form, 'building': building}
    return render(request, 'analyze_dash/create_research.html', context)


from django.shortcuts import get_object_or_404, redirect

def delete_file(request, research_id, file_id):
    file_to_delete = get_object_or_404(ResearchFile, id=file_id)
    file_to_delete.file.delete()
    file_to_delete.delete()
    return redirect('research_detail', research_id=research_id)


from django.http import HttpResponse
from django.shortcuts import get_object_or_404


def download_research_file(request, research_id, file_id):
    research = get_object_or_404(Research, id=research_id)
    file_instance = get_object_or_404(ResearchFile, id=file_id, research=research)

    response = HttpResponse(file_instance.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{file_instance.file.name}"'
    return response