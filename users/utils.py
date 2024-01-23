def obj_to_contact(obj):
    post = dict(vars(obj))
    if post['sujet'] is None:
        post['sujet'] = ""

    if obj.create_dt:
        post['create_dt'] = obj.create_dt.strftime('%d / %m / %Y')
    else:
        post['create_dt'] = ''

    del post['_state']

    return post