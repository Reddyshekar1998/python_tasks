from flask import Flask, request, jsonify
app = Flask(__name__)

data = {
    'param1': 'value1',
    'param2': 'value2',
    'param3': 123,
    'param4': True,
    'param5': ['item1', 'item2', 'item3'],
    'param6': ' ',
    'param7': None,
    'param8': 3.14,
    'param9': '2023-05-29',
    'param10': 'Hello World!'
}

# Create operation
@app.route('/data', methods=['POST'])
def create_data():
    new_data = request.get_json()
    if new_data:
        for key, value in new_data.items():
            data[key] = value
        return jsonify({'message': 'Data created successfully',"data":data}), 201
    else:
        return jsonify({'error': 'Invalid data format'}), 400

# Read operation
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data)

# Update operation
@app.route('/data', methods=['PUT'])
def update_data():
    update_request = request.get_json()
    if update_request:
        for key, value in update_request.items():
            if key in data:
                data[key] = value
        return jsonify({'message': 'Data updated successfully',"data":data}), 200
    else:
        return jsonify({'error': 'Invalid data format'}), 400

# Delete operation
@app.route('/data', methods=['DELETE'])
def delete_data():
    key = request.args.get('key', None)
    if key in data:
        del data[key]
        return jsonify({'message': f'Data with key {key} deleted successfully','data' : data}), 200
    else:
        return jsonify({'error': 'Invalid key or key not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
