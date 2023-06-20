# django-breche-backend
## Salaison de la breche server development
- api
- users
## 인증은 E-mail로
```js
 email = models.EmailField(_('email adress'), unique=True)

 USERNAME_FIELD = 'email'
 REQUIRED_FIELDS= ['username']
```
