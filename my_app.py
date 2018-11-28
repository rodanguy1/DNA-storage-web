from flask import Flask, render_template, url_for


app = Flask(__name__)

posts = [
    {
        'name': 'Guy Rodan',
        'date_of_birth': '8.3.1991',
        'hobbies': 'netflix&chill'
    },
{
        'name': 'Dor Stern',
        'date_of_birth': '11.11.1906',
        'hobbies': 'getting Fucked By Gutter'
    },
]

@app.route("/")
def hello():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)