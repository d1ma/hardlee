
import string


class NeighborGroups(object):
	group_distance = {'AA': [('AE', 0), ('AH', 0), ('AO', 0), ('AY', 0), ('EH', 0)], 'IY': [('IH', 0)], 'AE': [('AA', 0), ('AH', 0), ('AO', 0), ('AY', 0), ('EH', 0)], 'EH': [('AA', 0), ('AE', 0), ('AH', 0), ('AO', 0), ('AY', 0)], 'DH': [('D', 0)], 'AH': [('AA', 0), ('AE', 0), ('AO', 0), ('AY', 0), ('EH', 0)], 'UW': [('UH', 0)], 'AO': [('AA', 0), ('AE', 0), ('AH', 0), ('AY', 0), ('EH', 0)], 'IH': [('IY', 0)], 'UH': [('UW', 0)], 'W': [('V', 0)], 'V': [('W', 0)], 'AY': [('AA', 0), ('AE', 0), ('AH', 0), ('AO', 0), ('EH', 0)], 'ZH': [('Z', 0)], 'Z': [('ZH', 0)], 'D': [('DH', 0)]}

	def __item__(self, metric):		
		self.neighbors = group_distance

	def clean(self, syl):
		return syl.translate(None, string.digits)

	def get_neighbors(self, syl, budget=None):
		syl_clean = self.clean(syl)
		if budget:
			pass
		else:
			return self.neighbors.get(syl_clean, [])

