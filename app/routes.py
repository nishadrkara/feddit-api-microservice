from flask_restx import Resource, Namespace
from datetime import datetime
from app.utils.utils import all_user_comments, fetch_user_comments
from app.parser import user_id_parser, comment_parser

api_namespace = Namespace('api', description='Feddit API')


@api_namespace.route('/')
class CommentsByUser(Resource):
    def get(self, id):
        user_comments = fetch_user_comments(id)
        if not user_comments:
            return {'message': 'user not found', 'status': 'error'}, 400
        return user_comments, 200


class UserCommentByPolarity(Resource):
    @api_namespace.expect(comment_parser)
    def get(self):
        try:
            args = comment_parser.parse_args()
            start_date = args['start_date']
            end_date = args['end_date']
            sort_order = args['sort_order']
            limit = args['limit']
            page = args['page']

            start_date = datetime.strptime(
                start_date, '%Y-%m-%d').date() if start_date else None
            end_date = datetime.strptime(
                end_date, '%Y-%m-%d').date() if end_date else None
            response = all_user_comments(start_date, end_date, sort_order)
            # Pagination
            total_comments = len(response)
            start_index = (page - 1) * limit
            end_index = start_index + limit
            paginated_comments = response[start_index:end_index]

            return {
                'total_comments': total_comments,
                'page': page,
                'limit': limit,
                'data': paginated_comments,
                'status': 'success',
            }, 200
        except Exception as e:
            return {'status': 'error',
                    'message': str(e)}, 400


def initialize_routes(api):
    api.add_resource(CommentsByUser, '/user-comments/<int:id>/')
    api.add_resource(UserCommentByPolarity, '/users-comments-by-polarity')
