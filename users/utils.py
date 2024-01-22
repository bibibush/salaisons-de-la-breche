def obj_to_contact(obj):
    post = dict(vars(obj))
    if post['sujet'] is None:
        post['sujet'] = ""

    del post['_state']

    return post