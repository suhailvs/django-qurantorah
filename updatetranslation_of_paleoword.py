import json
from torah.models import Word

"""
USAGE
=====
./manage.py shell
>>> import updatetranslation_of_paleoword
>>> updatetranslation_of_paleoword.wt()
"""

def save_to_db(c):

	fp_paleo = json.loads(open('torah/json/paleo/{c}.json'.format(c=c)).read())
	fp_trans = json.loads(open('torah/json/mtt/{c}.json'.format(c=c)).read())
	paleo_data = fp_paleo['text'] # [['line1','line2'...], ...]
	#trans_data = fp_trans['text'] # [[['word1', ...], ...], ...]
	errors = []
	for i in range(len(paleo_data)):
		"""
		paleo_data = [
			['line1','line2'.... 30lines], #chapter 1
			... chapter 2
		]
		"""
		
		for j in range(len(paleo_data[i])):
			line = paleo_data[i][j]
			try:
				trans = fp_trans['text'][i][j][::-1] #[  [  [
			except:
				#print('%d:%d line didnt exists in trans'%(i+1,j+1))
				errors.append('line didnt exists - %d:%d'%(i+1,j+1))
				continue
				
			if len(line.split(' ')) != len(trans):
				#print(i+1,j+1)
				errors.append('%d:%d'%(i+1,j+1))
				continue

			for n,word in enumerate(line.split(' ')):
				item, created = Word.objects.get_or_create(name = word)
				if not item.translation:
					item.translation = trans[n]
					item.save()
	return errors

import json

def wt():
	chap='genesis,exodus,deuteronomy,leviticus,numbers'
	for c in chap.split(','):
		errors = save_to_db(c)
		with open('errors_%s.json'%c, 'w') as outfile:
			json.dump(errors, outfile,indent = 4)