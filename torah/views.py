from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

import os
import json

from .models import Word

from .templatetags.torah_filters import fiej

def get_line(lang,c):
    fp = os.path.join(settings.BASE_DIR, 'torah', 'json', lang, f"{c['title']}.json")
    data = json.loads(open(fp).read())
    return data['text'][c['chapter']-1][c['line']-1]

def showline(request, title='genesis', chapter=1, line=1):
    if request.method=='POST':
        return redirect('/torah/%s/%s/%s/'%(request.POST['title'],request.POST['chapter'],request.POST['line']))

    context = {'current': {'title':title, 'chapter':chapter, 'line':line}}

    for lang in ['paleo', 'english_mtt']: #,'english' ,'hebrew']:
        context[lang] = get_line(lang,context['current'])

        if lang == 'paleo':
            context[lang] = context[lang][::-1]

    return render(request,'torah/line.html',context)

def showword(request):
    """
    To display data in jTip
    """
    fp = os.path.join(settings.BASE_DIR, 'torah', 'json', 'paleo', 'dictionary.json')
    w = request.GET.get('word','')
    trans = '----'
    if w:
        w = w[::-1]
        data = json.loads(open(fp).read())
        for i in range(len(data['text'])):
            word = data['text'][i][0]
            if word == w:
                trans = data['text'][i]
                break
    context = {
        'word': w,
        'pron': trans[1],
        'eng':trans[2],
        'def':trans[3]
    }
    return render(request,'torah/word.html',context)


class AjaxView(View):
    """
    To display data in Bootstrap Model
    """
    def get_word_details(self, w):
        item = Word.objects.get(name = w[::-1])  # reverse the word
        return json.dumps({
            'id':item.id,
            'description':item.desc,
            'translation': item.translation,
            'lines':[{'id':l.id,'t':l.title,'c':l.chapter,'l':l.line} for l in item.lines.all()]
        })

    def get_search_result(self, q):
        """
        English to Paleo Search
        """
        trans = Word.objects.filter(translation__icontains = q)
        results = [{'paleo':fiej(item.name[::-1]), 'translation': item.translation} for item in trans[:5] ]
        return json.dumps({'results':results, 'n': trans.count()})

    def get(self, request, *args, **kwargs):
        w = request.GET.get('word','')
        q = request.GET.get('q','')
        if w: resp = self.get_word_details(w)
        if q: resp = self.get_search_result(q)
        return HttpResponse(resp)

    def post(self, request, *args, **kwargs):
        w = Word.objects.get(id = request.POST['id'])
        w.desc = request.POST['description']
        w.save()
        print('saved: ', w.desc)
        return HttpResponse('saved')
