from helpers.UserHelper import user_helper


def post_helper(post):
    return {
        'id': str(post['_id']) if '_id' in post else '',
        'user_id': str(post['user_id']) if 'user_id' in post else '',
        'photo': post['photo'] if 'photo' in post else '',
        'subtitle': post['subtitle'] if 'subtitle' in post else '',
        'date': post['date'] if 'date' in post else '',
        'likes': [str(p) for p in post['likes']] if 'likes' in post else '',
        'comments': [str(p) for p in post['comments']] if 'comments' in post else '',
        'total_likes': post['total_likes'] if 'total_likes' in post else '',
        'total_comments': post['total_comments'] if 'total_comments' in post else '',
        'user': user_helper(post['user'][0]) if 'user' in post and len(post['user']) > 0 else ''
    }


