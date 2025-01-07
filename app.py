from flask import Flask, render_template, request
import requests

app = Flask(__name__)

GITHUB_API_URL = "https://api.github.com"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            return render_template('index.html', error="Please enter a username")

        user_url = f"{GITHUB_API_URL}/users/{username}"
        repos_url = f"{GITHUB_API_URL}/users/{username}/repos"

        user_response = requests.get(user_url)
        if user_response.status_code != 200:
            return render_template('index.html', error="User not found")

        user_data = user_response.json()
        repos_response = requests.get(repos_url)
        repos = repos_response.json()

        top_repos = sorted(repos, key=lambda x: x['stargazers_count'] + x['forks_count'], reverse=True)[:4]

        return render_template('index.html', user=user_data, top_repos=top_repos)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
