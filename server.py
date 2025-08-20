# app.py

import json
from flask import Flask, render_template, request, redirect, url_for, session

# --- Your Original Classes, slightly modified for Flask integration ---
class SocialMedia:
    """Handles user registration and login/logout."""
    def _load_data(self):
        """Loads data from the JSON file."""
        try:
            with open('data.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"userData": []}

    def _save_data(self, data):
        """Saves data to the JSON file."""
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)

    def register(self, uname, passw):
        """Registers a new user."""
        if not uname or not passw:
            return False, "Username and password cannot be empty."

        data = self._load_data()
        if any(user['username'] == uname for user in data['userData']):
            return False, "Username already exists. Please choose a different username."

        data['userData'].append({"username": uname, "password": passw, "posts": []})
        self._save_data(data)
        return True, "Registration successful."

    def login(self, uname, passw):
        """Logs in a user and returns their data."""
        data = self._load_data()
        for user in data["userData"]:
            if user['username'] == uname and user['password'] == passw:
                return True, f"Welcome {uname}!", user.get('posts', [])
        return False, "Invalid username or password.", None

    def logout(self):
        """Clears the session on logout."""
        session.clear()

class Post(SocialMedia):
    """Handles post-related actions."""
    def create_post(self, uname, post_text):
        """Creates a new post for a given user."""
        if not post_text:
            return False, "Post cannot be empty."

        data = self._load_data()

        all_posts = [p for u in data['userData'] for p in u.get('posts', [])]
        post_id = max((p['id'] for p in all_posts), default=0) + 1

        new_post = {'id': post_id, 'post': post_text, 'likes': 0, 'dislikes': 0, 'author': uname}

        for user in data['userData']:
            if user['username'] == uname:
                user_posts = user.get('posts', [])
                user_posts.append(new_post)
                user['posts'] = user_posts
                break
        
        self._save_data(data)
        return True, f"Post created successfully with ID: {post_id}"

    def delete_post(self, uname, post_id):
        """Deletes a post by ID for a given user."""
        data = self._load_data()
        for user in data['userData']:
            if user['username'] == uname:
                original_post_count = len(user.get('posts', []))
                user['posts'] = [post for post in user.get('posts', []) if post['id'] != post_id]
                if len(user['posts']) < original_post_count:
                    self._save_data(data)
                    return True, f"Post ID {post_id} deleted successfully."
                else:
                    return False, f"Post ID {post_id} not found or you don't have permission."
        return False, f"Post ID {post_id} not found for user."

    def display_posts(self, for_user=None):
        """Displays all posts or posts for a specific user."""
        data = self._load_data()
        if for_user:
            user_posts = [post for user in data['userData'] if user['username'] == for_user for post in user.get('posts', [])]
            return True, user_posts
        else:
            all_posts = [post for user in data['userData'] for post in user.get('posts', [])]
            return True, all_posts
    
    def upvote_post(self, post_id):
        """Upvotes a post."""
        data = self._load_data()
        for user in data['userData']:
            for post in user.get('posts', []):
                if post['id'] == post_id:
                    post['likes'] += 1
                    self._save_data(data)
                    return True, f"Post ID {post_id} liked successfully."
        return False, f"Post ID {post_id} not found."

    def downvote_post(self, post_id):
        """Downvotes a post."""
        data = self._load_data()
        for user in data['userData']:
            for post in user.get('posts', []):
                if post['id'] == post_id:
                    post['dislikes'] += 1
                    self._save_data(data)
                    return True, f"Post ID {post_id} disliked successfully."
        return False, f"Post ID {post_id} not found."

# --- Flask Application Setup ---
app = Flask(__name__)
app.secret_key = 'a_very_secret_key_for_session_management'

social_media = SocialMedia()
post_manager = Post()

@app.route('/')
def index():
    """Main page to display all posts."""
    is_success, all_posts = post_manager.display_posts()
    return render_template('index.html', posts=all_posts, username=session.get('username'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_success, message = social_media.register(username, password)
        if is_success:
            return redirect(url_for('login'))
        return render_template('register.html', message=message)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_success, message, posts = social_media.login(username, password)
        if is_success:
            session['username'] = username
            return redirect(url_for('index'))
        return render_template('login.html', message=message)
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Handles user logout."""
    social_media.logout()
    return redirect(url_for('index'))

@app.route('/create_post', methods=['POST'])
def create_post():
    """Handles creation of a new post."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    post_text = request.form['post_text']
    post_manager.create_post(session['username'], post_text)
    return redirect(url_for('index'))

@app.route('/my_posts')
def my_posts():
    """Displays posts by the current user."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    is_success, user_posts = post_manager.display_posts(for_user=session['username'])
    return render_template('my_posts.html', posts=user_posts)

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    """Deletes a post by ID."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    post_manager.delete_post(session['username'], post_id)
    return redirect(url_for('my_posts'))

@app.route('/upvote/<int:post_id>')
def upvote_post(post_id):
    """Upvotes a post."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    post_manager.upvote_post(post_id)
    return redirect(url_for('index'))

@app.route('/downvote/<int:post_id>')
def downvote_post(post_id):
    """Downvotes a post."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    post_manager.downvote_post(post_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
