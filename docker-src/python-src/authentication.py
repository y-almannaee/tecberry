class auth_helper:

	def __init__(self,schema_prefix="unnamed",database=None):
		self.name = schema_prefix.lower()
		self.db = database

	def store_str(self, key, item):
		pass
	
	def store_encrypted_str(self, key, item, encryption_key):
		pass

	def get_str(self, key):
		pass

	def get_encrypted_str(self, key, encryption_key):
		pass

	def store_hash(self, key, dict):
		pass

	def register_and_store_cookie(self):
		pass