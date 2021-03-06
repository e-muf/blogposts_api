from flask import request, g, Blueprint, json, Response
from marshmallow import ValidationError

from ..shared.Authentication import Auth
from ..models.BlogpostModel import BlogpostModel, BlogpostSchema
from ..models.UserModel import UserModel

blogpost_api = Blueprint('blogpost_api', __name__)
blogpost_schema = BlogpostSchema()

@blogpost_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create blogpost function
  """
  req_data = request.get_json()
  req_data['owner_id'] = g.user.get('id')
  
  try:
    data = blogpost_schema.load(req_data)
  except ValidationError as error:
    print(error)
    return custom_response(error.as_json, 400)

  post = BlogpostModel(data)
  post.save()
  post_data = blogpost_schema.dump(post)

  return custom_response(post_data, 201)

@blogpost_api.route('/', methods=['GET'])
def get_all():
  """
  Get all Blogposts
  """
  posts = BlogpostModel.get_all_blogpost()
  posts_data = blogpost_schema.dump(posts, many=True)
  
  return custom_response(posts_data, 200)

@blogpost_api.route('/<int:blogpost_id>', methods=['GET'])
def get_one(blogpost_id):
  """
  Get a Blogpost
  """
  post = BlogpostModel.get_one_blogpost(blogpost_id)

  if not post:
    return custom_response({'error': 'post not found'}, 404)

  post_data = blogpost_schema.dump(post)

  return custom_response(post_data, 200)

@blogpost_api.route('/<int:blogpost_id>', methods=['PUT'])
@Auth.auth_required
def update(blogpost_id):
  """
  Update a Blogpost
  """
  req_data = request.get_json()
  post = BlogpostModel.get_one_blogpost(blogpost_id)

  if not post:
    return custom_response({'error': 'post not found'}, 404)

  post_data = blogpost_schema.dump(post)

  if post_data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 400)

  try:
    data = blogpost_schema.load(req_data, partial=True)
  except ValidationError as error:
    return custom_response(error, 400)

  post.update(data)
  data = blogpost_schema.dump(post)

  return custom_response(data, 200)

@blogpost_api.route('/<int:blogpost_id>', methods=['DELETE'])
@Auth.auth_required
def delete(blogpost_id):
  """
  Delete a Blogpost
  """
  post = BlogpostModel.get_one_blogpost(blogpost_id)

  if not post:
    return custom_response({'error': 'post not found'}, 404)

  post_data = blogpost_schema.dump(post)

  if post_data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission_denied'}, 400)

  post.delete()

  return custom_response({'message': 'deleted'}, 204)

def custom_response(response, status_code):
  """
  Custom response function
  """

  return Response(
    mimetype="application/json",
    response=json.dumps(response),
    status=status_code
  )