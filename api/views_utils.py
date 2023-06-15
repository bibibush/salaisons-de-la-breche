def obj_to_order(obj):
    post = dict(vars(obj))

    if obj.order_file:
        post['order_file'] = obj.order_file.name
    else:
        post['order_file'] = ''
    
    if obj.date:
        post['date'] = obj.date.strftime('%d/%m/%Y')
    else:
        post['date'] = ''

    del post['_state']

    return post