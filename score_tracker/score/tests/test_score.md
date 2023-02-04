# SCORE TESTS


# USER TYPES:
- ANON USER
- GUEST USER
- NORMAL USER


## SCORE CREATE

### ANON USER
Happy Paths:
- [x] should succeed if throttle limit not reached
    - [x] response should return: auth tokens, number, uuid
- [x] created score shold have user_id that matches the user id of the created user


Sad Paths:
- [x] Should fail if throttle limit is reached
- [x] should fail if number is invalid
- [x] should fail if number is not provided

### GUEST/NORMAL USER
Happy Paths:
- [x] should be able to create score if user is authenticated
    - [x] response should return: number, uuid, date/times
- [x] created score should have user_id that matches the user id of the authenticated user


Sad Paths:
- [x] should fail if a score has already been created today
- [x] should fail if number is invalid
- [x] should fail if number is not provided



## SCORE UPDATE

### ANON USER
- [ ] Should always fail

### GUEST/NORMAL USER

Happy Paths:
- [ ] Shoud succced if exists
    - [ ] should be possible to update: time, number
    - [ ] response should return: number, uuid, date, time

Sad Paths:
- [ ] should fail if it doesn't exist
- [ ] should fail if no uuid is passed or is invalid



## SCORE GET

### ANON USER
- [ ] Should always fail

### GUEST/NORMAL USER

Happy Paths:
- [ ] Shoud succced if exists
    - [ ] response should return: number, uuid, date/times

Sad Paths:
- [ ] should fail if it doesn't exist
- [ ] should fail if no uuid is passed or is invalid

## SCORE DELETE
- [ ] should always fail