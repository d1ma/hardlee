
import string
from produce_group_dict import main
SKIP = ''
class NeighborGroups(object):
	group_distance ={SKIP: [('F', 0.1), ('TH', 0.1), ('HH', 0.1)], 'AA': [('AE', 0.1), ('AH', 0.1), ('AO', 0.1), ('AY', 0.1), ('EH', 0.1)], 'AE': [('AA', 0.1), ('AH', 0.1), ('AO', 0.1), ('AY', 0.1), ('EH', 0.1)], 'EH': [('AA', 0.1), ('AE', 0.1), ('AH', 0.1), ('AO', 0.1), ('AY', 0.1)], 'DH': [('D', 0.1)], 'F': [('', 0.1), ('TH', 0.1), ('HH', 0.1)], 'AH': [('AA', 0.1), ('AE', 0.1), ('AO', 0.1), ('AY', 0.1), ('EH', 0.1)], 'UW': [('UH', 0.1)], 'AO': [('AA', 0.1), ('AE', 0.1), ('AH', 0.1), ('AY', 0.1), ('EH', 0.1)], 'W': [('V', 0.1)], 'IH': [('IY', 0.1)], 'HH': [('F', 0.1), ('', 0.1), ('TH', 0.1)], 'IY': [('IH', 0.1)], 'UH': [('UW', 0.1)], 'TH': [('F', 0.1), ('', 0.1), ('HH', 0.1)], 'V': [('W', 0.1)], 'AY': [('AA', 0.1), ('AE', 0.1), ('AH', 0.1), ('AO', 0.1), ('EH', 0.1)], 'ZH': [('Z', 0.1)], 'Z': [('ZH', 0.1)], 'D': [('DH', 0.1)]}

	def __init__(self, metric='default'):		
		self.neighbors = main()

	def clean(self, syl):
		return syl.translate(None, string.digits)

	def get_neighbors(self, syl, budget=None):
		syl_clean = self.clean(syl)
		if budget:
			ns = self.neighbors.get(syl_clean,[])
			return [n for n in ns if n[1] < budget]
		else:
			return self.neighbors.get(syl_clean, [])

