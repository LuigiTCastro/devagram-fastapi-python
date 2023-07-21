def user_helper(user):
    return {
        'id': str(user['_id']),  # turns the ObjectId into Str.
        'name': user['name'],
        'email': user['email'],
        'password': user['password'],
        # 'photo': user['photo'] if 'photo' in user else ''  # TERNARIO (?)
    }
