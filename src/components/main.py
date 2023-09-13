from flask import Flask, request
from flask_cors import CORS
import json
# a way to upload the input data is needed
app = Flask(__name__)
CORS(app, supports_credential=True)

@app.route('/indexlist',methods=["GET","POST"])
def indexlist():
    if request.method == 'POST':
        # use the data from font-end json.load(request.data)
        compressor_id = json.loads(request.data)['compressor_id']
        early_config = json.loads(request.data)['early_config']
        compressor_config = json.loads(request.data)['compressor_config']
        
        
        configration = {'compressor_id':json.dumps(compressor_id), 
                        'early_config':json.dumps(early_config),
                        'compressor_config':json.dumps(compressor_config)
                        }
        # after get the configuration, build a compressor based on the configration.
        # import libpressio, use comp = libpressio...to build 
        # export the compressed data/external matrix to the front-end

        return configration
    else:
        return 'something wrong'
if __name__ == '__main__':
   app.run(debug=True)