import re
import string
import sys

MAX_LINE_WIDTH = 72

# Max line width exceeded
too_long = lambda line: len(line) > MAX_LINE_WIDTH
def line_width_check(line, line_number, msg="Line %d: exceeded the \
maximum line width of %d characters by %d"):
	if too_long(line):
		print(msg % (line_number, MAX_LINE_WIDTH, len(line) - MAX_LINE_WIDTH))

# Ignore style inside of strings. String is in a group
in_single_quotes = r"'[^']*'"
in_double_quotes = r'"[^"]*"'
in_str = re.compile(r'(%s|%s)' % (in_single_quotes, in_double_quotes))
# Ignore stuff inside docstrings
in_docstr = re.M.compile(r'""".+"""', re.MULTILINE)
# Ignore style of things after comments. Comment is in a group
commented_out = r'\#\s*(\S+)'
def prepare_line(line):
	line = re.sub(commented_out, line)
	line = re.sub()

# Useless comment symbol (No comment but # used)
empty_comment = re.compile(r'\#\s*$')
def empty_comment_check(line, line_number, p=empty_comment, \
						msg="Line %d: no comment given after #"):
	if p.findall(line):
		print(msg % line_number)
# No space after comment
comment_space = re.compile(r'\#\S')
def comment_space_check(line, line_number, p=comment_space, \
						msg="Line %d: need a space after '#'"):
	if p.findall(line):
		print(msg % line_number)

# Operator spacing
non_pre_op = r'(?:\w|\d|\)|\])'
non_post_op = r'(?:\w|\d|\(|\[)'
arith_op = r'(?:\+|\-|\*|\/{1,2}|\%)'
eq_op = r'(?:(?:!|=)?=)'
ineq_op = r'(?:>|<(?:=)?)'
arith_eq_op = r'(?:(?:%s)=)' % arith_op
# Operator without space is in a group
pre_op_space = re.compile(r'(?:%s)(%s|%s|%s|%s)' % \
	(non_pre_op, arith_eq_op, eq_op, ineq_op, arith_op))
post_op_space = re.compile(r'(%s|%s|%s|%s)(?:%s)' % \
	(arith_eq_op, eq_op, ineq_op, arith_op, non_post_op))
# Unary '-' for negative check. Used to stop operator spacing message.
# Negative number in question is in a group
unary_minus = re.compile(r'(?:%s|%s|%s|%s|\[|\(|\:)\s*(-\d+)' % \
	(arith_eq_op, eq_op, ineq_op, arith_op))
def operator_space(line, line_number, p1=pre_op_space, \
					p2=post_op_space, p3=unary_minus, \
					msg="Line %d: need spaces around binary operators '%s'"):
	matches, operator = [f.findall(line) for f in (p1, p2, p3)], set()
	for unary_minus_found in matches[2]:
		matches[1].remove('-')
	for match in matches[:2]:
		if match:
			operator = operator.union(set(match))
	if operator:
		print(msg % (line_number, ', '.join(operator)))

# No space before line break
line_breaker = re.compile(r'\S\\')
def line_break_check(line, line_number, p=line_breaker, \
					msg="Line %d: need a space before '\\'"):
	if p.findall(line):
		print(msg % line_number)

# Stupid boolean comparisons
# Expression compared is in a group
bools = r'(?:True|False)'
bool_first_comp = r'(?:%s\s*==\s*([^\s:]+)(?=\s+|:))' % bools
bool_after_comp = r'(?:(?:(?:el)?if\s+)(?:\S+\s+)*(\S+)\s*==\s*%s)' % bools
bool_comp = re.compile(r'%s|%s' % (bool_after_comp, bool_first_comp))
"Line %d: unnecessary comparison of 'expression' to boolean"

# Comma spacing. Comma and next word in group. Doesn't match tuples
comma_space = re.compile(r'(,(?!\))[^ \n,)]+)')
"Line %d: need a space after comma ',something'"

# Bad list slicing. Entire slice in group
# Creating a new copy with [0:], [0::], [::], [::1]
new_copy = re.compile(r'(\[(?:0:+)|(?::{2}1?)\])')
"Line %d: use [:] to create a new copy rather than '[::0]'"
# Unnecessary colon
no_step_arg = re.compile(r'(\[[^:]+:[^:]+:\])')
"Line %d: unnecessary colon given with no step argument '[2:3:]'"

# Spacing after colons is required for lambdas and dictionary entries
# lambda to nonspace characters after colon in group.
lambda_colon = re.compile(r'(lambda.*:\S+)')
"Line %d: need space after colon for lambda expression 'lambda:x'"
# entry and nonspace characters after colon in group.
entry_colon = re.compile(r'(%s|%s:\S+)' % (in_single_quotes, in_double_quotes))
"Line %d: need space after colon for dictionary entry ''entry':value'"

# Use of semi-colon
semi_colon = re.compile(r';')
"Line %d: semicolons are not needed in Python"

# Trailing whitespace
eol_whitespace = re.compile(r'\s+\n')
"Line %d: trailing whitespace"

# Spacing after brackets such as ( 'Hello', 'World' ) or [ 1: 2 ]
# The offending bracket is in a group
post_bracket_space = re.compile(r'((?:(?:\(|\[)\s))')
"Line %d: space found after opening bracket '( '"
pre_bracket_space = re.compile('(\s(?:\)|\]))')
"Line %d: space found before closing bracket ' )'"

# Double-spacing
two_spaces = re.compile(r' [ ]+')
"Line %d: multiple consecutive spaces found"

# Spacing between function name and arguments
def_func_space = re.compile(r'def\s+(\S+)\s+\(')
"Line %d: space found before arguments in function definition for 'foo'"
call_func_space = lambda fn: re.compile(r'%s\s+\(' % fn)
"Line %d: space found before arguments in function call for 'foo'"

# Spacing between a list and slicing
lst_slice_space = re.compile(r'(?:\]|\)|\w)(\s+\[.*\])')
"Line %d: space found before slicing notation"

# Make sure they don't repeat function calls with the same argument
func_call_history = {}
"Line %d: repeated function call from line Y with function 'foo'"