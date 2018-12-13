from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
import json

from .models import Sura, Aya, TranslatedAya, Word

def showline(request, sura=1, line=1):
    if request.method=='POST':
        print(request.POST)
        return redirect('/quran/%s/%s/'%(request.POST['sura'],request.POST['aya']))
    sura_data = Sura.objects.get(number = sura)
    aya = Aya.objects.get(sura = sura_data, number = line)
    translation = TranslatedAya.objects.get(aya = aya, translation_id=1)
    
    context = {
    	'current': {'sura':sura_data, 'aya':line},
    	'arabic' : aya,
    	'translation': translation,
        'suras': Sura.objects.all(),
        'words' : aya.words.all()
    	}

    return render(request,'quran/line.html',context)

class AjaxView(View):
    """
    To display/save data in Bootstrap Model
    """
    def get(self, request, *args, **kwargs):
        resp = []
        w = request.GET.get('word','')
        if w: 
            word = Word.objects.get(id = w)
            root = word.root
            if root:
                ayas = root.ayas.distinct()
                for aya in ayas:
                    resp.append({'sura':aya.sura.number,'aya':aya.number })
            else:
                resp.append({'sura':word.sura.number,'aya':word.aya.number })

        return HttpResponse(json.dumps(resp))

    def post(self, request, *args, **kwargs):
        w = Word.objects.get(id = request.POST['id'])
        w.paleo = request.POST['paleo']
        w.save()
        return HttpResponse('saved')