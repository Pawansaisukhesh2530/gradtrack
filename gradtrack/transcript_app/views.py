from django.shortcuts import render, get_object_or_404
from .models import Student, Participation, AttributeStrengthMap
from collections import defaultdict
from datetime import date
from django.http import HttpResponse
from django.template.loader import get_template
from django.urls import reverse
import qrcode
import io
import weasyprint
import base64


def home(request):
    return render(request, 'transcript_app/home.html')

def transcript_view(request):
    roll_no = request.GET.get('roll_no')
    student = get_object_or_404(Student, roll_no=roll_no)
    participations = Participation.objects.filter(student=student)

    all_attributes = set()
    for part in participations:
        all_attributes.update(part.event.attributes.all())

    strength_scores = defaultdict(list)
    for attr in all_attributes:
        mappings = AttributeStrengthMap.objects.filter(graduate_attribute=attr)
        for map in mappings:
            strength_scores[map.character_strength.name].append(map.weight)

    strength_data = []
    for strength, values in strength_scores.items():
        avg = round(sum(values) / len(values), 2)
        if avg >= 2.5:
            category = "ESTD"
        elif avg >= 1.5:
            category = "DEV"
        else:
            category = "EMER"
        strength_data.append({
            'name': strength,
            'average': avg,
            'category': category
        })

    strength_data.sort(key=lambda x: x['name'])

    # Top 5 most meaningful events based on number of graduate attributes
    sorted_events = sorted(participations, key=lambda p: len(p.event.attributes.all()), reverse=True)
    top_events = [p.event.name for p in sorted_events[:5]]

    qr_b64 = None
    if participations.count() > 5:
        all_events_url = request.build_absolute_uri(
            reverse('all_events', kwargs={'roll_no': student.roll_no})
        )
        qr = qrcode.make(all_events_url)
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        qr_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render(request, 'transcript_app/transcript.html', {
        'student': student,
        'strength_data': strength_data,
        'today': date.today(),
        'top_events': top_events,
        'qr_code': qr_b64
    })

def transcript_pdf(request, roll_no):
    student = get_object_or_404(Student, roll_no=roll_no)
    participations = Participation.objects.filter(student=student)

    all_attributes = set()
    for part in participations:
        all_attributes.update(part.event.attributes.all())

    strength_scores = defaultdict(list)
    for attr in all_attributes:
        mappings = AttributeStrengthMap.objects.filter(graduate_attribute=attr)
        for map in mappings:
            strength_scores[map.character_strength.name].append(map.weight)

    strength_data = []
    for strength, values in strength_scores.items():
        avg = round(sum(values) / len(values), 2)
        if avg >= 2.5:
            category = "ESTD"
        elif avg >= 1.5:
            category = "DEV"
        else:
            category = "EMER"
        strength_data.append({
            'name': strength,
            'average': avg,
            'category': category
        })

    strength_data.sort(key=lambda x: x['name'])

    # Top 5 most meaningful events based on number of graduate attributes
    sorted_events = sorted(participations, key=lambda p: len(p.event.attributes.all()), reverse=True)
    top_events = [p.event.name for p in sorted_events[:5]]

    qr_b64 = None
    if participations.count() > 5:
        all_events_url = request.build_absolute_uri(
            reverse('all_events', kwargs={'roll_no': student.roll_no})
        )
        qr = qrcode.make(all_events_url)
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        qr_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    template = get_template('transcript_app/transcript.html')
    html = template.render({
        'student': student,
        'strength_data': strength_data,
        'today': date.today(),
        'top_events': top_events,
        'qr_code': qr_b64
    })

    pdf_file = weasyprint.HTML(string=html).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="transcript_{student.roll_no}.pdf"'
    return response

def all_events_view(request, roll_no):
    student = get_object_or_404(Student, roll_no=roll_no)
    participations = Participation.objects.filter(student=student)
    all_event_names = [f"{p.event.name} - {p.event.date}" for p in participations]
    return render(request, 'transcript_app/student_events.html', {
        'student': student,
        'all_events': all_event_names
    })
