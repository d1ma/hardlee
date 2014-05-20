
def main():
	SKIP = ''
	groups = [[SKIP,'HH'],['AA', 'AE', 'AH', 'AO', 'AY','EH', 'EY'],['D','DH'],['IH','IY'],['V','W'],['Z','ZH'],['UH','UW']]

	d = {}

	for group in groups:
		for i, syl in enumerate(group):
			group_test = group[:]
			del group_test[i]
			d[syl] = zip(group_test,[.1]*len(group_test))

	return d
