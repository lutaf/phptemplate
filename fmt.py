#coding:utf-8
import sys
import re


TOKEN_TEXT = 0
TOKEN_VAR = 1
TOKEN_BLOCK = 2
TOKEN_COMMENT = 3

FILTER_SEPARATOR = '|'
FILTER_FUNC_CALL = ':'
FILTER_ARGUMENT_SEPARATOR = ':'
VARIABLE_ATTRIBUTE_SEPARATOR = '.'
BLOCK_TAG_START = '{%'
BLOCK_TAG_END = '%}'
VARIABLE_TAG_START = '{{'
VARIABLE_TAG_END = '}}'
COMMENT_TAG_START = '{#'
COMMENT_TAG_END = '#}'
SINGLE_BRACE_START = '{'
SINGLE_BRACE_END = '}'

# match a variable or block tag and capture the entire tag, including start/end delimiters
tag_re = re.compile('(%s.*?%s|%s.*?%s)' % (re.escape(BLOCK_TAG_START), re.escape(BLOCK_TAG_END),
                                          re.escape(VARIABLE_TAG_START), re.escape(VARIABLE_TAG_END)
                                        ))
       
class Token(object):
    def __init__(self, token_type, contents):
        # token_type must be TOKEN_TEXT, TOKEN_VAR, TOKEN_BLOCK or TOKEN_COMMENT.
        self.token_type, self.contents = token_type, contents

    def __str__(self):
    	return "%s\t%s" % (self.contents,len(self.contents))


    def compile(self):
    	return self.contents
	
	
class VarToken(Token):
	_VAR_NAME={
		'loop.index':'($loop_index+1)', #base 1
		'loop.index0':'$loop_index',
	}
	
	def _make_element(self,b):
		""" 构造单个元素 """
		#处理几个特殊元素
		if b in self._VAR_NAME:
			return self._VAR_NAME[b]
		L = b.split( VARIABLE_ATTRIBUTE_SEPARATOR )
		if len(L)==1:
			return "$%s" % L[0]
		elif len(L)==2:
			if L[1].isdigit():
				return "$%s[%s]" % (L[0],L[1])
			else:
				return "$%s['%s']" % (L[0],L[1])
		else:
			raise
	
	def _make_func_call(self,arg,fc):
		L = fc.split(FILTER_FUNC_CALL)
		if len(L)==1:
			return " %s(%s)" %(fc,arg)
		elif len(L)==2:
			return "%s(%s,%s)" %(L[0],L[1],arg)
		else:
			raise
		
	def compile(self):
		compiled_obj = None
		L = self.contents.split( FILTER_SEPARATOR )
		if len(L)==1:
			compiled_obj = self._make_element(L[0])
		elif len(L)==2:
			t= self._make_element(L[0])
			compiled_obj = self._make_func_call(t,L[1]) 
		else:
			raise		
		return "<?php echo %s;?>" % compiled_obj
        

class BlockToken(Token):
	def compile(self):
		if self.contents.startswith('endfor'):
			return "<?php endforeach;?>"
		elif self.contents.startswith('endif'):
			return "<?php endif;?>"
		elif self.contents.startswith('else'):
			return "<?php else: ?>"
			
		L = self.contents.split()
		if len(L)==4 and L[0]=='for' and L[2]=='in':
			return "<?php foreach($%s as $loop_index =>&$%s): ?>" %(L[3],L[1])
		elif len(L)==2 and L[0]=='if':
			return "<?php if ($%s): ?>" % (L[1])
		else:
			print L
			raise 
	
def create_token(token_string,in_tag):
	if in_tag:
		if token_string.startswith(VARIABLE_TAG_START):
			token = VarToken(TOKEN_VAR, token_string[len(VARIABLE_TAG_START):-len(VARIABLE_TAG_END)].strip())
		elif token_string.startswith(BLOCK_TAG_START):
			token = BlockToken(TOKEN_BLOCK, token_string[len(BLOCK_TAG_START):-len(BLOCK_TAG_END)].strip())
		elif token_string.startswith(COMMENT_TAG_START):
			token = Token(TOKEN_COMMENT, '')
	else:
		token = Token(TOKEN_TEXT, token_string)
    	return token


def run(fname):
	template_string = file(fname,'rt').read()
	result=[]
	in_tag = False
	for bit in tag_re.split(template_string):
		if bit:
			result.append(create_token(bit,in_tag))
		in_tag = not in_tag
	#join result...
	data=[]
	for r in result:
		try:
			data.append(r.compile())
		except:
			pass
	file(fname,'wt').write(''.join(data))
if __name__ == "__main__":
	if len(sys.argv)!=2:
		print "Usage:%s xxx" % sys.argv[0]
		sys.exit(-1)
	else:
		run(sys.argv[1])