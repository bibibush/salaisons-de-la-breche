from random import *
import string

def obj_to_order(obj):
    post = dict(vars(obj))

    if obj.order_file:
        post['order_file'] = obj.order_file.name
    else:
        post['order_file'] = ''
    
    if obj.date:
        post['date'] = obj.date.strftime('%Y-%m-%d')
    else:
        post['date'] = ''
      
    if obj.modify_dt:
        post['modify_dt'] = obj.modify_dt.strftime('%d/%m/%Y')
    else:
        post['modify_dt'] = ''

    if obj.create_dt:
        post['create_dt'] = obj.create_dt.strftime('%d/%m/%Y')
    else:
        post['create_dt'] = ''
    
    if obj.user:
        post['user'] = obj.user.username
    else:
        post['user'] = ''

    del post['_state']

    return post

def random_letters(digit):
     string_pool = string.digits
     result = ""
     for i in range(int(digit)):
         result += choice(string_pool)
     return result
