
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

GITHUB_API_URL = "https://api.github.com"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/search', methods=['GET'])
def search_user():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400

    user_url = f"{GITHUB_API_URL}/users/{username}"
    repos_url = f"{GITHUB_API_URL}/users/{username}/repos"

    user_response = requests.get(user_url)
    if user_response.status_code != 200:
        return jsonify({"error": "User not found"}), 404

    user_data = user_response.json()
    repos_response = requests.get(repos_url)
    repos = repos_response.json()

    top_repos = sorted(repos, key=lambda x: x['stargazers_count'] + x['forks_count'], reverse=True)[:4]

    result = {
        "avatar": user_data["avatar_url"],
        "username": user_data["login"],
        "followers": user_data["followers"],
        "repos_count": user_data["public_repos"],
        "top_repos": [{
            "name": repo["name"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "url": repo["html_url"]
        } for repo in top_repos]
    }

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)