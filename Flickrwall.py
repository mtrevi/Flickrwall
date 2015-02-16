#!/usr/bin/python

import logging
import json
from random import choice, shuffle
from time import sleep
import flickr_api as f
import subprocess
import config
import urllib
import sys
import os


#~ LOADING GENERAL SETTINGS 
PHOTOS_FOLDER = config.general['photos_folder']
NO_SCREENS = config.general['number_of_screens']
#~ Set output file for each screen
PHOTO_PATHS = []
for i in range(1,NO_SCREENS+1):
   PHOTO_PATHS.append( PHOTOS_FOLDER+'/'+config.general['photo_name'].replace('.jpg','-screen%d.jpg'%i) )

SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""


class Flickrwall:
   '''
   '''
   def __init__(self):
      self.set_logger()
      self.bg = '/System/Library/CoreServices/DefaultDesktop.jpg'
      self.flickr = self.authenticate()
      self.dowloaded_photos = []
      self.clean = False

   def authenticate(self):
      # IF FILE NOT FOUND
      FILENAME = config.auth['auth_file']
      if os.path.isfile(FILENAME):
         self.log.info('Loading Oauth Data from %s' %FILENAME )
         f.set_keys(api_key=config.auth['key'], api_secret=config.auth['secret'])
         f.set_auth_handler(FILENAME)
      else:
         print >> sys.stdout, '> Oauth Data not found.'
         f.set_keys(api_key=config.auth['key'], api_secret=config.auth['secret'])
         a = f.auth.AuthHandler(callback = "http://michele.trevisiol.com/")
         perms = "read"
         url = a.get_authorization_url(perms)
         # Let the user copy and paste the Oauth Token and Verifier
         print >> sys.stdout, '> Click on the following link and copy the Oauth Verifier'
         print url
         OAUTH_VERIFIER = input('Oauth Verifier: ')
         a.set_verifier(OAUTH_VERIFIER)
         # set the AuthHandler for the session
         f.set_auth_handler(a)
         a.save(FILENAME)
      # return f
      return f
   
   def load_settings(self):
      import config

   def set_logger(self):
      # Set Logger
      self.log = logging.getLogger('Flickrwall')
      self.log.setLevel(logging.INFO)
      # create file handler which logs even debug messages
      fh = logging.FileHandler(config.general['logfile'])
      # fh.setLevel(logging.INFO)
      # create console handler with a higher log level
      ch = logging.StreamHandler()
      ch.setLevel(logging.ERROR)
      # create formatter and add it to the handlers
      formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
      fh.setFormatter(formatter)
      # add the handlers to the logger
      self.log.addHandler(fh)
      self.log.addHandler(ch)

   def get_userid(self):
      return self.flickr.Person.findByUserName(config.auth['username'])['id']

   def get_photos_by_search(self):
      ''' return a list of photos objects '''
      photos = self.flickr.Photo.search(
         user_id=self.get_userid(),
         media='photos',
         orientation='landscape',
         per_page=config.general['last_n_photos'],
         tags=config.filtering['accepted_tags'],
         min_taken_date=config.filtering['min_taken_date'],
         max_taken_date=config.filtering['max_taken_date'])
      self.log.info( 'Downloaded a list of %d photos' %len(photos) )
      return photos

   def update_wallpaper(self, photos, defaultpath):
      # remove current photos
      if self.clean:
         for currentphoto in self.dowloaded_photos:
            os.system( 'rm "%s" &2>/dev/null' %currentphoto)
         self.clean = False
      # re-order photos
      shuffle(photos)
      pinfo = photos[0]
      self.log.debug( 'Photo Selected: %s' %(pinfo) )
      del(photos[0])
      #~ download photo
      finalpath = self.download_photo(pinfo)
      self.dowloaded_photos.append(finalpath)
      #~ change desktop(s)
      self.wallpaper_changer(finalpath, defaultpath)
      # self.set_command()
      return photos, finalpath

   def set_command(self):
      os.system('killall Dock')

   def get_photo_url(self, photo):
      dict_sizes = self.flickr.Photo.getSizes(photo, format='json')
      str_sizes = dict_sizes['Original']
      self.log.debug( 'Photo Details: %s' %str_sizes )
      return str_sizes['source']

   def download_photo(self, photo):
      photo_url = self.get_photo_url(photo)
      #~ download photo
      finalpath = PHOTOS_FOLDER+"/"+photo.title.replace(' ', '_')+".jpg"
      self.log.debug( 'Downloading photo to %s' %finalpath )
      urllib.urlretrieve(photo_url, finalpath)
      self.log.info( 'Downloaded photo to %s' %finalpath )
      return finalpath

   def wallpaper_changer(self, filepath, defaultpath):
      ''' Change the Desktop Wallpaper for Mavericks '''
      os.system( 'cp "%s" "%s"' %(filepath, defaultpath))
      self.log.info( 'Copied %s to %s' %(filepath, defaultpath) )

   def update_single_wallpaper(self, defaultpath):
      ''' Change current desktop wallpaper '''
      command = 'osascript -e \'tell application "Finder" to set desktop picture to POSIX file "%s"\'' %defaultpath
      # self.log.info( command )
      # os.system( command )
      subprocess.Popen(SCRIPT%defaultpath, shell=True)


   def run(self):
      while True:
         self.log.debug( 'Get photos by search' )
         photos = self.get_photos_by_search()
         if len(PHOTO_PATHS) > 1:
            for defaultpath in PHOTO_PATHS:
               photos, finalpath = self.update_wallpaper(photos,defaultpath)
            # reset the dock
            self.set_command()
         else:
            photos, finalpath = self.update_wallpaper(photos,PHOTO_PATHS[0])
            self.update_single_wallpaper(finalpath)
         self.log.info('Sleeping for %d minutes' %(config.general['time_seconds']/60))
         sleep(config.general['time_seconds'])
         # reload settings (in case of changes of time, etc..)
         self.load_settings()
         self.clean = True




fws = Flickrwall()
fws.run()


