from random import randint

def pickACard(user,password):	
	s =['syd.socks.ipvanish.com', 'tor.socks.ipvanish.com', 'par.socks.ipvanish.com', 'fra.socks.ipvanish.com', 'lin.socks.ipvanish.com', 'nrt.socks.ipvanish.com', 'ams.socks.ipvanish.com', 'waw.socks.ipvanish.com', 'lis.socks.ipvanish.com', 'sin.socks.ipvanish.com', 'mad.socks.ipvanish.com', 'sto.socks.ipvanish.com', 'lon.socks.ipvanish.com', 'atl.socks.ipvanish.com', 'chi.socks.ipvanish.com', 'dal.socks.ipvanish.com', 'den.socks.ipvanish.com', 'iad.socks.ipvanish.com', 'lax.socks.ipvanish.com', 'mia.socks.ipvanish.com', 'nyc.socks.ipvanish.com', 'phx.socks.ipvanish.com', 'sea.socks.ipvanish.com']
	server = user+":"+password+"@"+ s[randint(0,len(s))]+":1080"
	return server
	

