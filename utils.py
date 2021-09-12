from uuid import uuid4
def gen_primarykey() -> str:
	return ''.join(str(uuid4()).split('-'))