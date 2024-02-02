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
    
    def from_json(self, json_data):
        self.id = None
        self.name = json_data.get("name")
        self.trojan = json_data.get("content")
        self.image = json_data.get("image")
        return self
    
    def __str__(self) -> str:
        return "signature:{id="+str(self.id)+", name="+self.name+", content="+self.trojan+"};"
    
    def to_json(self):
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

test_path = "C:\Users\dmitr\my_project\Untitled.png"
test_dir = "C:\Users\dmitr\my_project\flask-signature-app\test_folder"

def upload_file(signature_got):
    if request.method == 'POST':
        # check if the post request has the file part
        # if 'file' not in request.files:
            # flash('No file found')
            # print("No file found.")
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            # flash('No selected file')
            return None # redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_binary = file.open(test_path, 'rb')
            return file_binary # send_from_directory('/path/to/save', filename, as_attachment=True)
        
    binary_data = open(signature_got.trojan, 'wb')
    test_dir = os.path.join(test_dir, "downloaded_signature")
    try:
        # Create the file and write binary data to it in binary write mode
        with open(test_dir, 'wb') as file:
            file.write(binary_data)
        print(f"File saved as {test_dir}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")    

# repo
signatures = []
def add_sig(sig: signature_data) -> signature_data:
    global signatures
    sig.id = random.randrange(1, 100000000)
    signatures.append(sig)
    return sig


# //endpoints//
@app.route('/addSignature', methods=['POST'])
def add_signature():
    signature = add_sig(signature_data().from_json(request.json))

    return signature.to_json()

@app.route('/getAllSignatures', methods=['GET'])
def get_all_signatures():
    global signatures
    signatures_jsons = []
    for signature in signatures:
        signatures_jsons.append(signature.to_json())
        upload_file(signature)
    return {
            "signatures": signatures_jsons
        }

@app.route('/getTheSignatureByID', methods=['GET'])
def get_the_signature_by_id(sign_id):
    global signatures
    signatures_jsons = []
    for signature in signatures:
        if signature.id == sign_id:
            upload_file(signature)
            return {
                "signature by {sign_id}is: ": signature
            }
    
    

app.run(host='127.0.0.1', port=5000)
