from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import json, random
import os
from flask import send_from_directory

app = Flask(__name__)

class signature_data:
    def __init__(self, id:int, name:str, image:str, trojan:str):
        self.id = id
        self.name = name
        self.image = image
        self.trojan = trojan
    
    def __init__(self):
        self.id = None
        self.name = None
        self.image = None
        self.trojan = None
    
    def put_from_json_into_sign(self, json_data):
        self.id = None
        self.name = json_data.get("name")
        self.trojan = json_data.get("content")
        self.image = json_data.get("image")
        return self
    
    def __str__(self) -> str:
        return "signature:{id="+str(self.id)+", name="+self.name+", content="+self.trojan+"};"
    
    def turn_sign_into_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "content": self.trojan,
            "image": self.image
        }

ALLOWED_EXTENSIONS = ['png','img','jpg','jpeg']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

signatures = []
def add_sig(sig: signature_data) -> signature_data:
    global signatures
    sig.id = random.randrange(1, 100000000)
    signatures.append(sig)
    return sig

# //endpoints//
@app.route('/addSignature', methods=['POST'])
def add_signature():
    signature = add_sig(signature_data().put_from_json_into_sign(request.json))
    return signature.turn_sign_into_json()

@app.route('/getAllSignatures', methods=['GET'])
def get_all_signatures():
    global signatures
    signatures_jsons = []
    for signature in signatures:
        signatures_jsons.append(signature.turn_sign_into_json())
    return {
            "signatures": signatures_jsons
        }

@app.route('/getTheSignatureByID/<int:sign_id>', methods=['GET'])
def get_the_signature_by_id(sign_id):
    for signature in signatures:
        if signature.id == sign_id:
            return signature.turn_sign_into_json()
    return {'message': 'Signature not found'}, 404
    

app.run(host='127.0.0.1', port=5000)
