import json
from flask import Flask, request, render_template, redirect, session
import uuid

app = Flask(__name__, static_url_path='', static_folder='static')

app.secret_key = b'asdfasdfasdfase234qwadfadersf/'

with open("other/data/contacts.json", mode="r", encoding="utf-8") as read_file:
    contact_data = json.load(read_file)

@app.route('/')
def index():
    return redirect("/contacts")

@app.get('/contacts')
def contacts():
    msg = session.pop('success', None)

    search = request.args.get("q")
    if search:
        contacts = []
        for contact in contact_data:
            if (search in contact['email']
                    or search in contact['first_name']
                    or search in contact['last_name']):
                contacts.append(contact)
    else:
      contacts = contact_data

    return render_template("index.html", contacts=contacts, message=msg)


@app.get('/contacts/new')
def contact_new():
    return render_template("new.html", contact={})

@app.post('/contacts/new')
def contact_create():
    contact = {}
    contact['first_name'] = request.form['first_name']
    contact['last_name'] = request.form['last_name']
    contact['email'] = request.form['email']
    contact['id'] = len(contact_data) + 1
    contact['guid'] = uuid.uuid4()

    valid = True
    for other_contact in contact_data:
        if contact['email'] == other_contact['email']:
            valid = False

    if valid:
        contact_data.insert(0, contact)
        session['success'] = "Created Contact " + str(contact['id'])
        return redirect("/contacts")
    else:
        return render_template("new.html", contact=contact, message="Email must be unique")

@app.get('/contacts/<id>')
def contact_detail(id):
    id_int = int(id)
    for contact in contact_data:
        if id_int == contact['id']:
            break
    return render_template("detail.html", contact=contact)

@app.post('/contacts/<id>/delete')
def contact_delete(id):
    id_int = int(id)
    for contact in contact_data:
        if id_int == contact['id']:
            break
    contact_data.remove(contact)
    session['success'] = "Deleted Contact " + id
    return redirect("/contacts")

if __name__ == '__main__':
    app.run(port=5000)
