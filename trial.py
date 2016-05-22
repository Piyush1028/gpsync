import gdata.media
import gdata.geo
import gdata.photos.service



#import argparse
import atom
#import atom.service
#import filecmp
import gdata
import gdata.photos.service
import gdata.media
import gdata.geo
import gdata.gauth
import getpass
import httplib2
#import os
import subprocess
import tempfile
import time
import webbrowser

from datetime import datetime, timedelta
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from gdata.photos.service import GPHOTOS_INVALID_ARGUMENT, GPHOTOS_INVALID_CONTENT_TYPE, GooglePhotosException
'''
gd_client = gdata.photos.service.PhotosService()
gd_client.email = 'piyush.bit1028@gmail.com'
gd_client.password = 'nkfsohrxnrwwttow'
gd_client.source = 'photo-sync'
gd_client.ProgrammaticLogin()
'''


#OAuth login function

def OAuth2Login(client_secrets, credential_store, email):
    scope='https://picasaweb.google.com/data/'
    user_agent='Web client 1'

    storage = Storage(credential_store)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(client_secrets, scope=scope, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
        uri = flow.step1_get_authorize_url()
        webbrowser.open(uri)
        code = raw_input('Enter the authentication code: ').strip()
        credentials = flow.step2_exchange(code)

    if (credentials.token_expiry - datetime.utcnow()) < timedelta(minutes=5):
        http = httplib2.Http()
        http = credentials.authorize(http)
        credentials.refresh(http)

    storage.put(credentials)

    gd_client = gdata.photos.service.PhotosService(source=user_agent,
                                                   email=email,
                                                   additional_headers={'Authorization' : 'Bearer %s' % credentials.access_token})

    return gd_client

#credentials for authentication
client_secrets = 'C:\Users\Piyush Kumar\Desktop\gdata-python-client-master\client_secrets.json'
credential_store = 'C:\Users\Piyush Kumar\Desktop\gdata-python-client-master\credentials.dat'
email = 'piyush.bit1028@gmail.com'


#creating gd_client with OAuth access
gd_client = OAuth2Login(client_secrets, credential_store, email)

'''
#viewing album details
albums = gd_client.GetUserFeed(user=email)
for album in albums.entry:
  print album.title.text
  print 'title: %s, number of photos: %s, id: %s' % (album.title.text,
      album.numphotos.text, album.gphoto_id.text)
'''
'''
#adding new Album
album = gd_client.InsertAlbum(title='New album', summary='This is an album')

print 'after adding album'
print ' '


#viewing album after adding new album
albums = gd_client.GetUserFeed(user=email)
for album in albums.entry:
  print album.title.text
  print 'title: %s, number of photos: %s, id: %s' % (album.title.text,
      album.numphotos.text, album.gphoto_id.text)

#modifying album
for album in albums.entry:
	if album.title.text=='New album':
		album.title.text = 'abcd';
		updated_album = gd_client.Put(album, album.GetEditLink().href,
		    converter=gdata.photos.AlbumEntryFromString)


#delete an album
for album in albums.entry:
	if album.title.text=='abcd':
		gd_client.Delete(album)

'''



'''
###trying to download album/pic

def download_remote(self, event):
        
        if self.type not in chosenFormats:
            print ("Skipped %s (because can't download file of type %s)." % (self.path, self.type))
        elif dateLimit is not None and self.remoteTimestamp < dateLimit:
            print ("Skipped %s (because remote album pre %s)." % (self.path, time.asctime(dateLimit)))
        else:
        
            url = self.webUrl
            path = os.path.split(self.path)[0]
            if not os.path.exists(path):
                os.makedirs(path)
            urllib.urlretrieve(url, self.path)
            os.utime(path, (int(self.remoteDate), int(self.remoteDate)))


'''
'''
import urllib

photos = gd_client.GetFeed(
    '/data/feed/api/user/%s/albumid/%s?kind=photo' % (
        'piyush.bit1028@gmail.com', '6285562680294463649'))

print photos.entry[0].content.src #or something like first_entry.media.content[0].url where first_entry=photos.entry[0]
print photos.entry[1].content.src

for photo in photos.entry:
	phototitle=photo.title.text
	print phototitle
	
	print photo.content.src
	

	location="F:\desktop\%s" %(phototitle)
	urllib.urlretrieve(photo.content.src, location)
	
	
'''
'''
#delete a photo

photos = gd_client.GetFeed(
    '/data/feed/api/user/%s/albumid/%s?kind=photo' % (
        'piyush.bit1028@gmail.com', '6286379407194888449'))
for photo in photos.entry:
  print 'Photo title:', photo.title.text
  gd_client.Delete(photo)

'''
'''
import os, sys

#os.listdir('F:\desktop\atemp')
dir=r'F:\desktop\atemp'+'\%s'%('428363_10151336692064407_477608438_n.jpg')
#print "The dir is: %s" %os.listdir('F:\desktop\atemp')
os.remove(dir)
print "The dir after removal of path : %s" %os.listdir(r'F:\desktop\atemp')

'''


album_url = '/data/feed/api/user/%s/albumid/%s' % ('piyush.bit1028@gmail.com', '6286379407194888449')
filename = 'F:\desktop\pic\IMG_20151112_101500.jpg'
metadata = gdata.photos.PhotoEntry()
metadata.title = 'My Photo Title'
metadata.media.keywords = 'keyword1, keyword2, keyword3'

gd_client.InsertPhoto(album_url, metadata, filename, content_type='image/jpeg')

filename = r'F:\desktop\pic\abc.jpg'
metadata = gdata.photos.PhotoEntry()
metadata.title = atom.Title(text=fileName)
metadata.summary = atom.Summary(text='', summary_type='text')
gd_client.InsertPhoto(album_url, metadata, filename, content_type='image/jpeg')

