from flask import Flask, render_template, request, redirect, url_for
from models import db, StringRecord

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        new_record = StringRecord(content=content)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('index'))
    records = StringRecord.query.all()
    return render_template('index.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
