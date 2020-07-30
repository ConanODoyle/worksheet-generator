def export_problems(problem_dict, name='problemset_count'):
	if name[-4:] != ".txt":
		name = name + ".txt"

	fo = open(name, 'w')

	problems = list(problem_dict.items())
	problems.sort()
	last_firstnum = None
	counter = 0
	for i, item in enumerate(problems):
		key, val = item
		output = str(key[1]) + str(key[0][0]) + str(key[2]) + ": " + str(val)
		spacer = [" "] * (24 - len(output))
		if counter % 5 == 0 or (last_firstnum is not None and last_firstnum != key[1]):
			fo.write("\n")
			counter = 0
		if last_firstnum is not None and last_firstnum != key[1]:
			fo.write("\n")
			counter = 0
		fo.write(output + "".join(spacer))
		counter = counter + 1

		last_firstnum = key[1]
