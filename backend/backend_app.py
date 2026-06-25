from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    """
    Posts route for both GET and POST, POST for create a new post and GET to show all posts
    """
    if request.method == 'POST':
        data = request.get_json()
        required_fields = ['title', 'content']
        missing = [field for field in required_fields if field not in data]

        if missing:
            return jsonify({'Error': f'Missing required field: {missing}'}), 400

        current_max_id = max([post['id'] for post in POSTS])
        new_post = {'id': current_max_id + 1, 'title': data['title'], 'content': data['content']}
        POSTS.append(new_post)
        return jsonify(new_post, 201)

    return jsonify(POSTS)


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Delete a post with given id
    """
    post_id = int(post_id)
    post = next((post for post in POSTS if post['id'] == post_id), None)

    if post:
        POSTS.remove(post)
        return jsonify({'message': f'Post with the id {post_id} has been deleted successfully.'}), 200
    return jsonify({'message': f'Post with the id {post_id} was not found.'}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
