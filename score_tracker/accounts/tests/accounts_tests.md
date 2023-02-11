# ACCOUTNS TESTS


## UPDATE ACCOUNT

### ANON USER

Unhappy Paths:
- [x] Should return 401 if user is anon


### AUTHENTICATED USER
Happy Paths:
- [ ] should succeed if valid email and password is provided
    - [ ] response should return: email, pasword? check
    - [ ] should update guest user to false


Unhappy Paths:
- [ ] should fail if invalid email is provided
- [ ] should fail if invalid password is provided
- [ ] should fail if both invalid email and password is provided?
- [ ] should fail if user attemps to update an account they are not authenticated as
- [ ] should fail if account being updated is not a guest only guest accounts can be updated using this endpoint)