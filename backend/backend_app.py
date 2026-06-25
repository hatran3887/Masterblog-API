from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Posts route to show all posts or sorted posts
    """
    sort = request.args.get("sort")
    direction = request.args.get("direction")

    if not sort or not direction:
        return jsonify(POSTS)

    if sort not in ("title", "content") or direction not in ("asc", "desc"):
        return jsonify({'message': 'the values for sort should be title or content'
                                   'and the value for direction should be asc or desc'}), 400

    if sort == "title":
        return jsonify(sorted(POSTS, key=lambda x: x['title'], reverse=direction == "desc"))
    else:
        return jsonify(sorted(POSTS, key=lambda x: x['content'], reverse=direction == "desc"))


@app.route('/api/posts', methods=['POST'])
def create_posts():
    """
    Posts route for create a new post
    """
    data = request.get_json()
    required_fields = ['title', 'content']
    missing = [field for field in required_fields if field not in data]

    if missing:
        return jsonify({'Error': f'Missing required field: {missing}'}), 400

    current_max_id = max([post['id'] for post in POSTS])
    new_post = {'id': current_max_id + 1, 'title': data['title'], 'content': data['content']}
    POSTS.append(new_post)
    return jsonify(new_post, 201)


@app.route('/api/posts/<int:post_id>', methods=['DELETE', 'PUT'])
def handle_post(post_id):
    """
    Delete or update a post with given id
    """
    post_id = int(post_id)
    post = next((post for post in POSTS if post['id'] == post_id), None)

    if not post:
        return jsonify({'message': f'Post with the id {post_id} was not found.'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        post['title'] = data.get('title', post['title'])
        post['content'] = data.get('content', post['content'])
        return jsonify(post)
    else:
        POSTS.remove(post)
        return jsonify({'message': f'Post with the id {post_id} has been deleted successfully.'}), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search route to search all posts
    """
    searched_title = request.args.get('title')
    searched_content = request.args.get('content')

    posts = []
    if searched_title:
        posts = [post for post in POSTS if searched_title.lower() in post['title'].lower()]
    if searched_content:
        posts = [post for post in POSTS if searched_content.lower() in post['content'].lower()]

    return jsonify(posts), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
