from flask import Flask,request,url_for,redirect,render_template
from annoy import AnnoyIndex
import numpy as np
import pandas as pd
import re

app = Flask(__name__)

data=pd.read_csv("output.csv")
images=data["Image"]
captions=data["Caption"]
# print(captions)
cap=list(captions)
captionss=[]

from transformers import AutoTokenizer, AutoModel
tokenizer1 = AutoTokenizer.from_pretrained("bert-base-uncased")
model1 = AutoModel.from_pretrained("bert-base-uncased")

import torch
for caption in cap:
#     print(type(caption))
    inputs = tokenizer1(caption, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model1(**inputs)

    embed = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    captionss.append(embed)

captions=np.array(captionss)

search_index = AnnoyIndex(captions.shape[1], 'angular')
for i in range(len(captions)):
    search_index.add_item(i, captions[i])

search_index.build(10) # 10 trees
search_index.save('output.ann')

cap=np.array(cap)
def search(query):    
    similar_item_ids = search_index.get_nns_by_vector(query,3,include_distances=True)
    results = pd.DataFrame(data={'Image': images[similar_item_ids[0]],'texts': cap[similar_item_ids[0]],'distance': similar_item_ids[1]})

    print(cap[similar_item_ids[0]])
    
    return results["Image"]


def embedding(queryy):
    inputs = tokenizer1(queryy, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model1(**inputs)
    embed = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embed

@app.route('/',methods=['POST','GET'])
def home1():
    return render_template("index.html")

@app.route('/result',methods=['POST','GET'])
def home2():
    if(request.method=="POST"):
        features=[x for x in request.form.values()]
        query=features[0]
        print(query)
        embed=embedding(query)
        result=list(search(embed))
        print(result)
        print(type(result))
        addresses=[]
        for img in result:
            print(img)
            address="./static/Gallery/%s"%(img)
            addresses.append(address)
        address1=addresses[0]
        address2=addresses[1]
        address3=addresses[2]
        print(address1)        
    return render_template("output.html",add1=address1,add2=address2,add3=address3)

app.run()