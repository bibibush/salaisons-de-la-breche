def obj_to_contact(obj):
    post = dict(vars(obj))

    del post['_state']

    return post