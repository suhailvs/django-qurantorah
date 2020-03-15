from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
import json

from .models import Sura, Aya, TranslatedAya, Word

def showline(request, sura=1, line=1):
    if request.method=='POST':
        return redirect('/quran/%s/%s/'%(request.POST['sura'],request.POST['aya']))
    sura_data = Sura.objects.get(number = sura)
    aya = Aya.objects.get(sura = sura_data, number = line)
    translation = TranslatedAya.objects.get(aya = aya, translation_id=4) # change translation id for different translations
    
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

        return HttpResponse(json.dumps({'root':str(root), 'related_ayas':resp}))

    def post(self, request, *args, **kwargs):
        w = Word.objects.get(id = request.POST['id'])
        w.paleo = request.POST['paleo']
        w.save()
        return HttpResponse('saved')

class PlayAyaView(View):
    """
    To play an aya using VLC Player
    """
    def play(self, folder, filename):
        import time, pathlib, vlc
        file_list = sorted([str(p) for p in pathlib.Path(folder).glob(filename)])
        for wav_file in file_list:
            p = vlc.MediaPlayer(wav_file)
            p.play()
            time.sleep(1.5)
            duration = p.get_length() / 1000
            time.sleep(duration-1)

    def get(self, request):
        sura = int(request.GET['sura'])
        aya = request.GET['aya']
        folder = "/home/donams/Music/wav"
        if sura<58:
            folder = f'{folder}/{sura}/' #0.bin'
        else:
            folder = f'{folder}/58_114/'

        print(sura, aya)

        self.play(folder, f'S{sura}_{aya}_*.bin')
        return HttpResponse('played')