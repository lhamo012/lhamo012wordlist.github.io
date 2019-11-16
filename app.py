from flask import Flask, request, Response, render_template, jsonify
import requests
import itertools
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Regexp, NumberRange, Optional, Required
import os 

class RequiredIf(object):
    # a validator which makes a field required if
    # another field is set and has a truthy value

    def __init__(self, *args, **kwargs):
        self.conditions = kwargs

    def __call__(self, form, field):
        for name, data in self.conditions.items():
            if name not in form._fields:
                Optional(form, field)
            else:
                condition_field = form._fields.get(name)
                if condition_field.data == data and not field.data:
                    Required()(form, field)
        Optional()(form,field)
       
class WordForm(FlaskForm):
    avail_letters = StringField("Letters", validators= [ RequiredIf(avail_pattern=''),
        Regexp(r'^[a-z]+$', message="must contain letters only")
    ])

    avail_length = IntegerField("WordLength", validators= [ Optional(),
        NumberRange(min=3, max=10, message="Wordlength must be equal to or between 3 & 10 characters")
    ])

    avail_pattern = StringField("Pattern", validators= [RequiredIf(avail_letters='')])

    submit = SubmitField("Go")

csrf = CSRFProtect()
app = Flask(__name__)
app.config["SECRET_KEY"] = "row the boat"
csrf.init_app(app)
length = 0

@app.route('/index')
def index():
    form = WordForm()
    return render_template("index.html", form=form)

def filterLength(word):
    return len(word) == length

def filterPattern(word):
    return re.search("^"+pattern+"$",word) 

@app.route('/words', methods=['POST','GET'])
def letters_2_words():

    form = WordForm()
    if form.validate_on_submit():
        letters = form.avail_letters.data
        global length;
        length  = form.avail_length.data
        global pattern;
        pattern = form.avail_pattern.data
    else:
        return render_template("index.html", form=form)

    with open('sowpods.txt') as f:
        good_words = set(x.strip().lower() for x in f.readlines())

    if (length != None):
        # filter words that are wordlength long
        good_words = set(filter(filterLength, good_words))

    if (pattern != ""):
        # filter words that fit a pattern
        good_words = set(filter(filterPattern, good_words))

    word_set = set()

    if (letters != ""):
        for l in range(3,len(letters)+1):
            for word in itertools.permutations(letters,l):
                w = "".join(word)
                if w in good_words:
                    word_set.add(w)
    else: 
        word_set = set(good_words)

    # sort alphabetically
    word_set = sorted(word_set)
    return render_template('wordlist.html',
        wordlist=sorted(word_set, key=len),
        name="CS4131")


@app.route('/proxy/<var>', methods=['GET'])
def proxy(var):
    result = requests.get('https://www.dictionaryapi.com/api/v3/references/collegiate/json/'+var+'?key='+ os.environ["PROJECT_API_KEY"])
    
    resp = Response(result.text)

    if result.status_code != 200:
        return "Error with API"
    else:
        jsonresponse = result.json()
        resp.headers['Content-Type'] = 'application/json'
        return str(jsonresponse[0]['shortdef'][0])

if __name__ == '__main__':
    app.run(debug=True)

