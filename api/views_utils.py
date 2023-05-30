def obj_to_order(obj):
    post = dict(vars(obj))

    del post['_state']

    return post