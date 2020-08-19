from flask import Flask, render_template, url_for, flash, redirect
from forms import ServerTableForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '276b5c0393f3e2ade9dd889dfddd6605014d6df6b5bab8a1a6f2f4949daebfa2'

@app.route('/')
@app.route('/home')
def home():
    return "Home Page"

@app.route('/serverTableMaintenance', methods=['GET','POST'])
def serverTableMaintenance():
    form = ServerTableForm()

    if form.validate_on_submit():
        flash(f'Submit for {form.serverName.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('serverTableMaintenance.html', title='Server Table Maintenance', form=form)

if __name__ == '__main__':
    app.run(debug=True)