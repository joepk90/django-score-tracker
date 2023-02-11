# ACCOUNTS TESTS

## CREATE USER
Note: a lot of logic is handled by Djoser - only test custom user/authentication logic

Unhappy Paths:
- [ ] User should not be able to login using username
- [ ] User should not be able to login using invalid email address

Happy Paths:
- [ ] User should be able to register using email address
- [ ] User should be able to login using email address
- [x] Guest users creation should have the is_guest property set to True


## UPDATE USER

### ANON USER

Unhappy Paths:
- [x] Should return 401 if user is anon


### GUEST USER
Happy Paths:
- [x] should succeed if valid email and password is provided
    - [x] should update guest user to false


Unhappy Paths:
- [x] should fail if invalid email is provided
- [x] should fail if no email is provided
- [x] should fail if invalid password is provided
- [x] should fail if no password is provided
- [x] should fail if both invalid email and password is provided?
- [x] should fail if user attemps to account with duplicate email address

### DEFAULT USER
- [x] Should return 401 if user is not a guest