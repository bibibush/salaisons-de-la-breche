def obj_to_order(obj):
    post = dict(vars(obj))

    if obj.order_file:
        post['order_file'] = obj.order_file.name
    else:
        post['order_file'] = ''

    del post['_state']

    return post