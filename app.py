from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

dossiers = {}
objects = {}
relationships = []

def next_id(entity):
    return str(len(entity) + 1)

@app.route('/')
def index():
    return redirect(url_for('dossiers_view'))

@app.route('/dossiers', methods=['GET', 'POST'])
def dossiers_view():
    if request.method == 'POST':
        name = request.form['name']
        did = next_id(dossiers)
        dossiers[did] = {'name': name, 'objects': [], 'relationships': []}
        return redirect(url_for('dossiers_view'))
    return render_template('dossiers.html', title='Dossiers', dossiers=dossiers)

@app.route('/objects', methods=['GET', 'POST'])
def objects_view():
    if request.method == 'POST':
        name = request.form['name']
        oid = next_id(objects)
        objects[oid] = {'name': name, 'relationships': []}
        return redirect(url_for('objects_view'))
    return render_template('objects.html', title='Objects', objects=objects)

@app.route('/relationships', methods=['GET', 'POST'])
def relationships_view():
    if request.method == 'POST':
        dossier_id = request.form['dossier_id']
        object_id = request.form['object_id']
        rel = {'dossier': dossier_id, 'object': object_id}
        relationships.append(rel)
        dossiers[dossier_id]['relationships'].append(rel)
        dossiers[dossier_id]['objects'].append(object_id)
        objects[object_id]['relationships'].append(rel)
        return redirect(url_for('relationships_view'))
    return render_template('relationships.html', title='Relationships',
                           dossiers=dossiers, objects=objects, relationships=relationships)

if __name__ == '__main__':
    app.run(debug=True)
