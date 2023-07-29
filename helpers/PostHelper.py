def post_helper(self, post):
    return {
        'id': str(post['_id']) if '_id' in post else '',
        'user': post['user'] if 'user' in post else '',
        'photo': post['photo'] if 'photo' in post else '',
        'subtitle': post['subtitle'] if 'subtitle' in post else '',
        'date': post['date'] if 'date' in post else '',
        'likes': post['likes'] if 'likes' in post else '',
        'comments': post['comments'] if 'comments' in post else '',
    }
