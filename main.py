from flask import Flask, request
import json, random

app = Flask(__name__)

def decode_binary_to_file(binary_data, output_file_path):
    try:
        with open(output_file_path, 'wb') as file:  # Note 'wb' mode for writing binary
            file.write(binary_data)
    except Exception as e:
        print(f"Error writing file: {e}")

def encode_file_to_binary(file_path):
    try:
        with open(file_path, 'rb') as file:  # Note 'rb' mode for reading binary
            binary_content = file.read()
        return binary_content
    except FileNotFoundError:
        print("File not found.")
        return None


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
    
    return {
            "signatures": signatures_jsons
        }

app.run(host='127.0.0.1', port=5000)
