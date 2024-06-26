from django.shortcuts import get_object_or_404, render
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import os
# Create your views here.


def accept(request):
    if(request.method =='POST'):
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        summary = request.POST.get("summary", "")
        degree = request.POST.get("degree", "")
        school = request.POST.get("school", "")
        university = request.POST.get("university", "")
        previous_work = request.POST.get("previous_work", "")
        skills = request.POST.get("skills", "")

        profile = Profile(
                name = name,
                email = email,
                phone = phone,
                summary = summary,
                degree = degree,
                school = school,
                university = university,
                previous_work = previous_work,
                skills = skills
        )

        profile.save()

    return render(request, 'pdf/accept.html')

def resume(request, id):

    user_profile = get_object_or_404(Profile, pk=id)
    template = loader.get_template('pdf/resume.html')
    html = template.render({'user_profile': user_profile})
    path_wkhtmltopdf = 'C:/wkhtmltox/bin/wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
    }
    pdf = pdfkit.from_string(html, False, options, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    return response
