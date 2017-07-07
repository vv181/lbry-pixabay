import os, errno
from python_pixabay import Pixabay
import requests
import json


class Main():
  def __init__(self, api, query, nfsw, pics):
    self.api = Pixabay(api)
    self.query = query
    self.nfsw = nfsw
    self.pics = pics
    self.search()

  #img_search = pix.image_search()

  def search(self):
    cis = self.api.image_search(q=self.query, lang='en', id='',
                                response_group='medium_resolution',
                                image_type='all',
                                orientation='all',
                                category='',
                                editors_choice='false',
                                safesearch=self.nfsw,
                                order='popular',
                                page=1,
                                per_page=self.pics,
                                callback='',
                                pretty='false'
                                )
    data = json.dumps(cis)
    l_data = json.loads(data)

    #print l_data['hits'][1]
    # parse search
    parent = 0
    if parent <= self.pics:
      page_url = l_data['hits'][parent]['pageURL']
      tags = l_data['hits'][parent]['tags']
      download_url = l_data['hits'][parent]['webformatURL']
      self.download(page_url,tags,download_url)
      parent += 1

  def download(self,page_url,tags,download_url):
    self.page_url = page_url
    self.tags = tags
    self.download_url = download_url

    try:

      print("downloading file: ",download_url)
      filename = download_url.split('/')[-1]
      print filename

      r = requests.get(download_url, stream=True)

      #Create Folder
      try:
        os.makedirs("photos")
      except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir("photos"):
          pass
        else:
          raise

      #Download File
      with open(os.path.join("photos",filename), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
          if chunk:
            f.write(chunk)
      print("download succesfull")


    except Exception:
      pass

      
    






    except Exception:
      print("error")

  def publish():
    try:
      # Publish to lbry
      print "publishing "
      titles = local_filename
      title = titles.replace(".pdf", "")
      file_path = os.path.realpath("pdf/{0}".format(local_filename))
      description = str(link.contents)
      license = "Creative Commons Attribution 4.0 International License"
      payload = {"name": title, "file_path": file_path, "bid": 0.0001,
                 "title": title, "description": description, "author": "EbookFoundation", "license": license}
      logger.info(client.publish(payload))

    except Exception:
      print "publishing failed"


print("Enter API key: ")
api = raw_input()
print("Enter Query: ")
query = raw_input()
print("Is Pics Safe for Work?: ")
nfsw = raw_input()
print("Enter Pics: ")
pics = raw_input()


app = Main(api, query, nfsw, pics)
