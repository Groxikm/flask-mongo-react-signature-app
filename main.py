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

#test_img_path = r"C:\Users\dmitr\my_project\Untitled.png"

#test_save_dir = r"C:\Users\dmitr\my_project\flask-signature-app\test-folder"

current_dir = os.path.dirname(__file__)

# Relative paths to the file and save directory
relative_img_path = r"C:\Users\dmitr\my_project\Untitled.png"
relative_save_dir = r"C:\Users\dmitr\my_project\flask-signature-app\test-folder"

# Full paths based on the current directory
test_img_path = "Untitled.png" # os.path.join(current_dir, relative_img_path)
test_save_dir = "test-folder"# os.path.join(current_dir, relative_save_dir)

def upload_file(http_method, binary_data=None):
    if http_method == 'POST':
        # Encode file to binary data
        try:
            with open(test_img_path, 'rb') as file:
                binary_data = file.read()
            return binary_data
        except FileNotFoundError:
            print(f"File not found by {test_img_path} ")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    elif http_method == 'GET':
        # Decode binary data and save to a file
        if binary_data is None or test_save_dir is None:
            print("Binary data and save directory must be provided for GET request.")
            return None
        try:
            save_path = os.path.join(test_save_dir, os.path.basename(test_img_path))
            with open(save_path, 'wb') as file:
                file.write(binary_data)
            print(f"File saved successfully at {save_path}")
            return test_save_dir
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")
            return None

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
    signature = add_sig(signature_data().put_from_json_into_sign(request.json))
    signature.image = upload_file('POST')
    return signature.turn_sign_into_json()

@app.route('/getAllSignatures', methods=['GET'])
def get_all_signatures():
    global signatures
    signatures_jsons = []
    for signature in signatures:
        signatures_jsons.append(signature.turn_sign_into_json())
        upload_file(signature)
    return {
            "signatures": signatures_jsons
        }

@app.route('/getTheSignatureByID/<int:sign_id>', methods=['GET'])
def get_the_signature_by_id(sign_id):
    for signature in signatures:
        if signature.id == sign_id:
            saved_file_path = upload_file('GET', sign_id)  # Save the signature image
            print(f"Image saved to {saved_file_path}")  # Optional: Print or log the path where the image was saved
            return signature.turn_sign_into_json()  # Return the signature's JSON representation
    return {'message': 'Signature not found'}, 404
    

app.run(host='127.0.0.1', port=5000)
