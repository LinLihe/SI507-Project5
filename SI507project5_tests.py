import unittest
from datetime import datetime
from SI507project5_code import *

class testfortumblr(unittest.TestCase):

	def setUp(self):
		self.CREDS_DICTION = CREDS_DICTION
		self.CACHE_DICTION = CACHE_DICTION
		self.CLIENT_KEY = CLIENT_KEY1
		self.CLIENT_SECRET = CLIENT_SECRET1
		baseurl = "http://api.tumblr.com/v2/blog/{}.tumblr.com/posts".format("liamlin")
		params = {"api_key" : self.CLIENT_KEY}    
		self.IDENTIFIER = "tumblr"
		self.expire =  has_cache_expired(self.CREDS_DICTION["TUMBLR"]["timestamp"], self.CREDS_DICTION["TUMBLR"]["expire_in_days"])
		self.request_identifier = create_request_identifier(baseurl,params)
		self.data_from_api = get_data_from_api(baseurl,self.IDENTIFIER,params)
		self.from_cache = get_from_cache(self.IDENTIFIER,self.CREDS_DICTION)

		tumblr_search_baseurl = "http://api.tumblr.com/v2/blog/{}.tumblr.com/posts".format("peacecorps")
		tumblr_search_params = {"limit" : 20, "type": "text","api_key" : CLIENT_KEY}
		self.list = CACHE_DICTION[create_request_identifier(tumblr_search_baseurl, tumblr_search_params)]["values"]["response"]["posts"][0]		
		self.for_csv = return_for_csv(self.list)

	def tearDown(self):
		pass

	def test_cache_expired(self):
		cache_timestamp = datetime.strptime(self.CREDS_DICTION["TUMBLR"]["timestamp"], DATETIME_FORMAT)
		now = datetime.now()
		delta = now - cache_timestamp
		if delta.days > self.CREDS_DICTION["TUMBLR"]["expire_in_days"]:
			self.assertEqual(self.expire,True)
		else:
			self.assertEqual(self.expire,False)

	def test_create_request_identifier(self):
		self.assertEqual(self.request_identifier, "http://api.tumblr.com/v2/blog/liamlin.tumblr.com/posts?api_key_{}".format(self.CLIENT_KEY).upper())

	def test_get_data_from_api(self):
		self.assertIsInstance(self.data_from_api,dict)

	def test_get_from_cache(self):
		self.assertIsInstance(self.from_cache,list)
		self.assertEqual(self.from_cache[0],self.CLIENT_KEY)
		self.assertEqual(self.from_cache[1],self.CLIENT_SECRET)

	def test_return_for_csv(self):
		self.assertIsInstance(self.for_csv, str)
		self.assertIn(self.list["date"], self.for_csv)
		if self.list["tags"]:
			self.assertIn(", ".join(self.list["tags"]), self.for_csv)
		else:
			self.assertEqual(self.list["tags"],None)
 
if __name__ == "__main__":
    unittest.main(verbosity=2)
