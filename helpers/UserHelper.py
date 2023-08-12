def user_helper(user):
    return {
        'id': str(user['_id']),  # turns the ObjectId into Str.
        'name': user['name'],
        'email': user['email'],
        'password': user['password'],
        'photo': user['photo'] if 'photo' in user else '',  # TERNARIO (?)
        'followers': [str(p) for p in user['followers']] if 'followers' in user else '',
        'following': [str(p) for p in user['following']] if 'following' in user else '',
        'total_followers': user['total_followers'] if 'total_followers' in user else '',
        'total_following': user['total_following'] if 'total_following' in user else '',
        'date': user['date'] if 'date' in user else '',
    }
