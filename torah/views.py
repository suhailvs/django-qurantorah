from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

import json

from .models import Word

def get_line(lang,c):
    data = json.loads(open('torah/json/%s/%s.json'%(lang,c['title'])).read())
    return data['text'][c['chapter']-1][c['line']-1]

def showline(request, title='genesis', chapter=1, line=1):
    if request.method=='POST':
        return redirect('/%s/%s/%s/'%(request.POST['title'],request.POST['chapter'],request.POST['line']))

    context = {'current': {'title':title, 'chapter':chapter, 'line':line}}

    for lang in ['paleo','english','english_mtt','hebrew']:
        context[lang] = get_line(lang,context['current'])

        if lang == 'paleo':
            context[lang] = context[lang][::-1]

    return render(request,'line.html',context)

def showword(request):
    """
    To display data in jTip
    """
    w = request.GET.get('word','')
    trans = '----'
    if w:
        w = w[::-1]
        data = json.loads(open('torah/json/paleo/dictionary.json').read())
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
    return render(request,'word.html',context)


class AjaxView(View):
    """
    To display data in Bootstrap Model
    """

    def get(self, request, *args, **kwargs):
        w = request.GET.get('word','')
        # try:
        #     item = Word.objects.get(name = w)
        # except:
        #     item = Word.objects.get(name = w[::-1])
        item = Word.objects.get(name = w[::-1])  # reverse the word
        return HttpResponse(json.dumps({
            'id':item.id,
            'description':item.desc,
            'translation': item.translation,
            'lines':[{'id':l.id,'t':l.title,'c':l.chapter,'l':l.line} for l in item.lines.all()]
        }))

    def post(self, request, *args, **kwargs):
        w = Word.objects.get(id = request.POST['id'])
        w.desc = request.POST['description']
        w.save()
        print('saved: ', w.desc)
        return HttpResponse('saved')