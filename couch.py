import couchdb
#http://guide.couchdb.org/draft/security.html
#create a admin to log in with credentials 
couch = couchdb.Server('http://45.55.228.139:5984') #Server('ip')
try:
	db = couch.create('flixrdb')
except Exception as e:
	db = couch['flixrdb']

#doc_id, doc_rev = db.save({'type': 'Person', 'name': 'John Doe'})


#get movie data from flixr
#save data into couchdb
#asynchronsly sync movie data on pouchdb