from generator import *
from diagnostic import *
import numpy as np
import random as rand

def op_add(a, b):
	return a + b

def op_sub(a, b):
	return a - b

def op_mul(a, b):
	return a * b

def op_div(a, b):
	return round(a / b, 4)

add = ('+', op_add)
sub = ('−', op_sub)
mul = ('×', op_mul)
div = ('÷', op_div)

num_weights = [1 for i in range(1, 31)]
num_weights[0] = 0.1 #lower chance of 1
for i in range(4, 31, 5): #lower chance of multiples of 5
	num_weights[i] = 0.5
sub_num_weights = [0 if i <= 10 else -0.5 for i in range(1, 31)]
num_weights = list(np.add(num_weights, sub_num_weights))

# results = generate_problems(100, [add, sub, mul], range(1, 31), op_weights=[0.1, 0.3, 1], num_weights=num_weights, condition_check=function)


def hard_multiplication(a, b, op):
	a_str, b_str = (str(a), str(b))
	
	if len(a_str) == 1 and len(b_str) == 1: # two single digits
		return None
	return (a, b, int(op[1](a, b)))

dist = {}
for i in range(10):
	results = generate_problems(100, [mul], range(1, 31), num_weights=num_weights, condition_check=hard_multiplication)
	generate_problem_set_image(results[0], results[1], "multiplication_" + str(i + 1))
	
	for key, val in results[2].items():
		dist[key] = dist.get(key, 0) + val

export_problems(dist, "multiplication_set")