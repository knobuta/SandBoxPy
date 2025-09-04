from datetime import date

from flask import Flask, render_template, request
import blog
import notification_manager

app = Flask(__name__)

@app.route('/')
def home():
    # Route for the home page.
    return render_template("index.html", posts=all_blogs, today=today)

@app.route('/post/<int:blog_id>')
def post(blog_id):
    # Route to display a specific blog post based on its ID.
    id = blog_id - 1 # index starts from 0
    return render_template("post.html", blog=all_blogs[id], today=today)

@app.route('/about')
def about():
    # Route for the about page.
    return render_template("about.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # Route for the contact page.
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        msg = request.form['message']

        # mail = notification_manager.NotificationManager(name, email, phone, msg)
        # mail.send_mail()

        return render_template("contact.html", message="Successfully sent your message")
    else:
        return render_template("contact.html")

if __name__ == "__main__":
    """ 
    Main entry point of the Flask application. 
    Initializes the Blog class to fetch blog data and starts the Flask server in debug mode.
    """

    # Initialize the Blog class and fetch all blog posts
    blog = blog.Blog()
    all_blogs = blog.get_blog_json()

    today = date.today().strftime("%B %d, %Y")

    app.run(debug=True)