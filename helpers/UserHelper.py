def user_helper(user):
    return {
        'id': str(user['_id']),  # turns the ObjectId into Str.
        'name': user['name'],
        'email': user['email'],
        'password': user['password'],
        'photo': user['photo'] if 'photo' in user else '',  # TERNARIO (?)
        'followers': [str(p) for p in user.get('followers', [])],
        'following': [str(p) for p in user.get('following', [])],
        'total_followers': user.get('total_followers', None),
        'total_following': user.get('total_following', None),
        # 'total_followers': user['total_followers'] if 'total_followers' in user else '',
        # 'total_following': user['total_following'] if 'total_following' in user else '',
        'datetime': user['datetime'] if 'datetime' in user else ''
    }
