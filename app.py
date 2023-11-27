from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to fetch and parse Coursera courses XML data
def get_courses():
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'xml')
    courses = []

    for loc in soup.find_all('loc'):
        courses.append(loc.text)

    return courses

# Function to filter courses based on keywords
def filter_courses(keyword):
    all_courses = get_courses()
    matching_courses = [course for course in all_courses if keyword.lower() in course.lower()]
    return matching_courses

@app.route('/')
def home():
    template_string = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Coursera Course Finder</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 20px;
                background-color: #f7f7f7;
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            h1 {
                color: #333;
                font-size: 40px;
            }

            form {
                margin-bottom: 20px;
            }

            label {
                font-size: 18px;
                margin-right: 10px;
            }

            input[type="text"] {
                width: 300px;
                padding: 10px;
                font-size: 16px;
            }

            button {
                padding: 10px 15px;
                font-size: 16px;
                cursor: pointer;
            }

            ul {
                list-style-type: none;
                padding: 0;
            }

            li {
                margin-bottom: 10px;
            }

            a {
                text-decoration: none;
                color: #007bff;
                font-weight: bold;
            }

            a:hover {
                text-decoration: underline;
            }

            .footer {
            background-color: #333; /* Dark gray background color */
            color: #fff; /* White text color */
            padding: 5px;
            text-align: center;
            position: fixed;
            bottom: 0;
            width: 100%;
            }

            .footer a {
                color: #fff; /* White color for links */
                text-decoration: none;
            }

            .footer a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1><large>Coursera Course Finder</large><sup><small> v1</small></sup></h1>
        <label for="user_message"><small><i>Discover Any Kind of Course That Ignites Your Passion!</i></small></label>
        <p></p>

        <form action="/chat" method="post">
            <input type="text" name="user_message" id="user_message" required>
            <button type="submit">Search</button><br>
            
            
        </form>

        {% if user_message %}
            <p>Your query: {{ user_message }}</p>
            {% if courses %}
                <h2>Matching Courses:</h2>
                <ul>
                    {% for course in courses %}
                        <li><a href="{{ course }}" target="_blank">{{ course }}</a></li>
                    {% endfor %}
                </ul>
            {% else %}
                <p>No matching courses found!</p>
            {% endif %}
        {% endif %}

        <div class="footer">
        <p>&copy; 2023 Edu-Con | <b>Powered By</b><sup><small> Edu-Con</small</sup></b></p>
        </div>
    </body>
    </html>
    """
    return render_template_string(template_string)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_message']
    courses = filter_courses(user_message)

    template_string = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Coursera Course Finder</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 20px;
                background-color: #f7f7f7;
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            h1 {
                color: #333;
            }

            form {
                margin-bottom: 20px;
            }

            label {
                font-size: 18px;
                margin-right: 10px;
            }

            input[type="text"] {
                width: 300px;
                padding: 10px;
                font-size: 16px;
            }

            button {
                padding: 10px 15px;
                font-size: 16px;
                cursor: pointer;
            }

            ul {
                list-style-type: none;
                padding: 0;
            }

            li {
                margin-bottom: 10px;
            }

            a {
                text-decoration: none;
                color: #007bff;
                font-weight: bold;
            }

            a:hover {
                text-decoration: underline;
            }

            .footer {
            background-color: #333; /* Dark gray background color */
            color: #fff; /* White text color */
            padding: 5px;
            text-align: center;
            position: fixed;
            bottom: 0;
            width: 100%;
            }

            .footer a {
                color: #fff; /* White color for links */
                text-decoration: none;
            }

            .footer a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Coursera Course Finder<sup><small> v1</small></sup></h1>

        <form action="/chat" method="post">
            <input type="text" name="user_message" id="user_message" required>
            <button type="submit">Search</button>
        </form>

        {% if courses %}
            <h2>Matching Courses:</h2>
            <ul>
                {% for course in courses %}
                    <li><a href="{{ course }}" target="_blank">{{ course }}</a></li>
                {% endfor %}
            </ul>
        {% else %}
            <p>No matching courses found.</p>
        {% endif %}

        <div class="footer">
        <p>&copy; 2023 Edu-Con | <b>Powered By</b><sup><small> Edu-Con</small</sup></b></p>
        </div>
    </body>
    </html>
    """
    return render_template_string(template_string, user_message=user_message, courses=courses)

if __name__ == '__main__':
    app.run(debug=True)
