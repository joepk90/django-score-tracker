# ACCOUTNS TESTS


## UPDATE ACCOUNT

### ANON USER

Unhappy Paths:
- [x] Should return 401 if user is anon


### GUEST USER
Happy Paths:
- [ ] should succeed if valid email and password is provided
    - [ ] response should return: email, pasword? check
    - [ ] should update guest user to false


Unhappy Paths:
- [x] should fail if invalid email is provided
- [x] should fail if no email is provided
- [x] should fail if invalid password is provided
- [x] should fail if no password is provided
- [x] should fail if both invalid email and password is provided?
- [ ] should fail if user attemps to update an account they are not authenticated as
- [ ] should fail if user attemps to account with duplicate email address

### DEFAULT USER
- [x] Should return 401 if user is not a guest