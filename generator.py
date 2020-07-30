from PIL import Image, ImageDraw, ImageFont, ImageFile
import random as rand
import math


def generate_problems(num_problems, operators, values, op_weights=None, num_weights=None,
					  condition_check=None, can_reorder=True):
	problem_set = []
	solution_set = []
	problems = {}
	for i in range(num_problems):
		op = rand.choices(operators, op_weights)[0]
		while True:
			a, b = rand.choices(values, weights=num_weights, k=2)
			min_val, max_val = (min(a, b), max(a, b))
			problem = (op[0], a, b)
			solution = op[1](a, b)

			if condition_check is None or condition_check(a, b, op):
				if condition_check is not None:
					a, b, solution = condition_check(a, b, op)
				break

		problem_set.append(problem)
		solution_set.append(solution)
		if can_reorder:
			problem_key = (problem[0], min_val, max_val)
		else:
			problem_key = (problem[0], a, b)
		problems[problem_key] = problems.get(problem_key, 0) + 1
	return (problem_set, solution_set, problems)


def generate_problem_set_image(problem_set, solution_set, name="problemset.png", dir="output/"):
	# settings
	bg_color = (255, 255, 255, 255)  # white, full opacity
	txt_color = (0, 0, 0, 255)  # black, full opacity
	gap_w = 45  # horizontal space between problems
	h_mod = 10  # vertical space between problem elements
	row_count = 10  # number of problems per row
	problem_dim = (52 + gap_w, 72 * 2)
	page_dim = (1275, 1650)  # 150 dpi for 8.5x11 letter paper
	fnt = ImageFont.truetype("verdana.ttf", 20)

	if list(name)[-4:] != ".png":
		name = name + ".png"

	# dimensions based on problem_set count, and individual problem dimensions
	rows = math.ceil(len(problem_set) / row_count)
	set_dim = (problem_dim[0] * row_count, rows * problem_dim[1])  # problem set without margins
	page_ofst = (int((page_dim[0] - set_dim[0] - gap_w) / 2),
				 int((page_dim[1] - set_dim[1]) / 2))

	img = Image.new("RGBA", set_dim, bg_color)
	full_img = Image.new("RGBA", page_dim, bg_color)

	d = ImageDraw.Draw(img)

	# 0, 0 starting from top left
	def draw_text(xy, text):
		d.text(xy, text, font=fnt, fill=txt_color)

	def text_width(text):
		return d.textsize(text, font=fnt)[0]

	def text_height(text):
		return d.textsize(text, font=fnt)[1]

	def add_tuples(a, b):
		return (int(a[0] + b[0]), int(a[1] + b[1]))

	x, y = (0, 0)
	for problem in problem_set:
		ofst = (x * problem_dim[0], y * problem_dim[1])

		top_num = str(problem[1])
		bot_num = str(problem[2])
		top_h = text_height(top_num)
		bot_h = text_height(bot_num)
		right_ofst = problem_dim[0] - (gap_w / 2) - 10  # 10px in from right edge

		top_txt_ofst = (right_ofst - text_width(top_num), 0)
		bot_txt_ofst = (right_ofst - text_width(bot_num), top_h + h_mod)
		op_txt_ofst = (text_width(problem[0]) - (fnt.size / 2), top_h + h_mod)
		line_ofst_l = add_tuples(ofst, (10, top_h + bot_h + h_mod * 2))
		line_ofst_r = add_tuples(ofst,
								 (right_ofst,
								  top_h + bot_h + h_mod * 2))

		draw_text(add_tuples(ofst, top_txt_ofst), top_num)
		draw_text(add_tuples(ofst, bot_txt_ofst), bot_num)
		draw_text(add_tuples(ofst, op_txt_ofst), problem[0])
		d.line([line_ofst_l, line_ofst_r], fill=txt_color, width=2)

		x = x+1
		if (x >= row_count):
			x = 0
			y = y+1

	full_img.paste(img, page_ofst)
	full_img.save(dir + name)

	x, y = (0, 0)
	for solution in solution_set:
		ofst = (x * problem_dim[0], y * problem_dim[1])
		solution_str = str(solution)
		sol_h = text_height(solution_str)
		sol_w = text_width(solution_str)

		solution_ofst = add_tuples(ofst,
								   (right_ofst - sol_w,
									sol_h * 2 + h_mod * 3))
		draw_text(solution_ofst, solution_str)

		x = x+1
		if (x >= row_count):
			x = 0
			y = y+1

	full_img.paste(img, page_ofst)
	full_img.save(dir + "solution_" + name)
