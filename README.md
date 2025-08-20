# Text Based Scoial Media App

## Flask Social Media Application - Detailed Good Points & Functionality

### Good Points
  •) Developed using Flask framework, which is lightweight, flexible, and widely used for web applications.
  
  •) Code is structured with modular classes (SocialMedia and Post), ensuring separation of responsibilities.
  
  •) Supports essential features: user registration, login/logout, post creation, deletion, upvote, and downvote.
  
  •) Implements session management for handling authenticated users securely within the app.
  
  •) JSON file-based persistence keeps the application simple and easy to understand for beginners and demonstrations.
  
  •) Readable and beginner-friendly code design with docstrings explaining purpose of methods.
  
  •) Integration of HTML templates (index, login, register, my_posts) provides dynamic rendering of content.
  
  •) Demonstrates Flask routing and request handling with both GET and POST methods.
  
  •) Uses unique post IDs and manages user-specific posts efficiently within JSON structure.

### Functionality & Working
  •) Users can register with a unique username and password. Registration checks prevent duplicate usernames.
  
  •) Users can log in with valid credentials; session stores the username to track login state.
  
  •) Logged-in users can create posts, each assigned a unique ID with initial likes/dislikes count set to zero.
  
  •) Users can view all posts on the main feed (/) or only their posts on the My Posts page.
  
  •) Posts can be deleted by their respective authors using the delete option.
  
  •) Logged-in users can interact with posts through upvotes and downvotes, updating like/dislike counts.
  
  •) Logout functionality clears the session and redirects users back to the homepage.
  
  •) Flask templates (index.html, register.html, login.html, my_posts.html) handle rendering and displaying data dynamically.

## Running the app 
1. python -m venv venv
2. pip install flask
4. python server.py
