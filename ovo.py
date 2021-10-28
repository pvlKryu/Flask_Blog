from flask import Flask, render_template, url_for  # Import FLASK
app = Flask(__name__)

posts = [  # list for posts
    {  # one post template
        'author': 'Pavel Kriuchkov',
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'October 08, 2021'
    },
    {
        'author': 'Pavel Kriuchkov',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': 'October 08, 2021'
    }
]


@app.route("/")  # Creating new app (main page)
@app.route("/home")  # Creating new app (main page)
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")  # Creating about page
def about():
    return render_template('about.html', title='About ')





if __name__ == '__main__':  # For debuge mode
    app.run(debug=True)
