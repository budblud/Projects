import functools

users = {'user': 'Jose', 'access_level1': 'admin'}

def make_secure(func):
    @functools.wrap(func)
    def secure_function():
        if users['access_level1'] == 'admin':
            return func()
        else:
            return f"No admin permissions for {users['user']}."

    return secure_function

@make_secure
def get_admin_pass():
    return '1234'

print(get_admin_pass())