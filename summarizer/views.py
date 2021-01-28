from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from summarizer.models import Summary
from .algorithms.scoring import scoring_algorithm, scoring_nepali
from .algorithms.frequency import  frequency_nepali, frequency_algorithm

from utils.algo import fetch_summary

# updated import 
from .utils.crawler import extract
from utils.scrap_google import get_google_news

def index(request):
    return render(request, 'summarizer/index.html')


def summarize_page(request):
    url = request.GET.get('url')
    long_text = request.GET.get('long-text')
    # sentence_no = int(request.GET.get('number'))
    result_list = []
    isURL = False
    is_para = True
    if url:
        long_text = extract(url)  # text extraction using BS
        original_text = str(url)
        isURL = True
        is_para = False
    else:
        original_text = long_text

    fs = fetch_summary(long_text)
    summ = fs.load_summary(long_text)
 
    summary = summ

    context = {'data': summary, 'original_text': original_text,'is_url':isURL,'is_para':is_para}

    return render(request, "summarizer/index.html", context)


def summarize_nepali_page(request):
    url = request.GET.get('url')
    long_text = request.GET.get('long-text')
    # sentence_no = int(request.GET.get('number'))
    # algorithm = request.GET.get('algorithm')
    result_list = []
    isURL  = False
    is_para = True
    if url:
        long_text = extract(url)
        original_text = url
        isURL = True
        is_para = False
    else:
        original_text = long_text

    fs = fetch_summary(long_text)
    summ = fs.load_summary(long_text)
 
    summary = summ

    context = {'data': summary, 'original_text': original_text,'is_url':isURL,'is_para':is_para}
    return render(request, "summarizer/index.html", context)


@login_required
def save_summary(request):
    summary = request.POST.get('summary')
    topic = request.POST.get('topic')
    if len(topic) < 50:
        heading = topic
    else:
        heading = topic[:50] + '...'

    summaryTb = Summary(user=request.user, body=summary, original_link=heading, date_created=date.today())
    summaryTb.save()
    context = {'message': 'success'}
    return render(request, "summarizer/index.html", context)


def history(request):
    summary = Summary.objects.filter(user=request.user).order_by('-id')
    context = {'data': summary}
    return render(request, "summarizer/history.html", context)


def history_topic(request):
    if request.method == 'GET':
        topic = request.GET.get('topic')
        summary = request.GET.get('body')
        context = {'topic': topic, 'body': summary}
        return render(request, "summarizer/history_topic.html", context)
