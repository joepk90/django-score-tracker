# SCORE TESTS


# USER TYPES:
- ANON USER
- GUEST USER
- NORMAL USER


## SCORE CREATE

### ANON USER
Happy Paths:
- [x] should succeed if throttle limit not reached
- [x] created score shold have user_id that matches the user id of the created user
    - [ ] response should return: auth tokens, number, uuid

Sad Paths:
- [ ] Should fail if throttle limit is reached

### GUEST/NORMAL USER
Happy Paths:
- [ ] Should succeed if no score has been created today
- [ ] created score should have user_id that matches the user id of the authenticated user
    - [ ] response should return: number, uuid, date/times

Sad Paths:
- [ ] should fail if a score has already been created today
- [ ] should fail if number is invalid



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