from python_pixabay import Pixabay
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
    cis = self.api.image_search(q = self.query, lang = 'en', id = '',
                               response_group = 'medium_resolution',
                               image_type = 'all',
                               orientation = 'all',
                               category = '',
                               editors_choice = 'false',
                               safesearch = self.nfsw,
                               order = 'popular',
                               page = 1,
                               per_page = self.pics,
                               callback = '',
                               pretty = 'false'
                            )
    data = json.dumps(cis)
    l_data = json.loads(data)
    
    print l_data['hits'][1]


  def download():
    pass


print("Enter API key: ")
api = raw_input()
print("Enter Query: ")
query = raw_input()
print("Is Pics Safe for Work?: ")
nfsw = raw_input()
print("Enter Pics: ")
pics = raw_input()



app = Main(api,query,nfsw,pics)