import os, json, errno, logging
from python_pixabay import Pixabay
import requests
from lbrynet import conf
from lbrynet.daemon.auth.client import LBRYAPIClient

logging.basicConfig(filename='log.log',level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class Main():
  def __init__(self, api, query, nfsw, pics):

    conf.initialize_settings()
    client = LBRYAPIClient.get_client()
    self.api = Pixabay(api)
    self.query = query
    self.nfsw = nfsw
    self.pics = int(pics) - 1
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

    # print l_data['hits'][1]
    # parse search
    parent = 0
    while parent <= self.pics:
      try:
        page_url = l_data['hits'][parent]['pageURL']
        tags = l_data['hits'][parent]['tags']
        download_url = l_data['hits'][parent]['webformatURL']
        self.download(page_url, tags, download_url)
      except Exception as e:
        pass

      parent += 1

  def download(self, page_url, tags, download_url):
    self.page_url = page_url
    self.tags = tags
    self.download_url = download_url

    try:

      print("downloading file: ", download_url)
      filename = download_url.split('/')[-1]

      r = requests.get(download_url, stream=True)

      # Create Folder
      try:
        os.makedirs("photos")
      except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir("photos"):
          pass
        else:
          raise

      # Download File
      with open(os.path.join("photos", filename), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
          if chunk:
            f.write(chunk)
      print("download succesfull")
      prit("pubishing")
      logger.info(filename)

      self.publish(page_url,tags,filename)

    except Exception:
      pass

    except Exception:
      print("error")

  def publish(self, page_url, tags):
    self.page_url = page_url
    self.tags = tags
    self.filename = filename
    try:
      # Publish to lbry
      print "publishing "
      title = page_url.split('/')[-2]
      file_path = os.path.realpath("photos/{0}".format(filename))
      description = tags
      license = "Creative Commons CC0"
      payload = {"name": title, "file_path": file_path, "bid": 0.0001,
                 "title": title, "description": description, "license": license}
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
