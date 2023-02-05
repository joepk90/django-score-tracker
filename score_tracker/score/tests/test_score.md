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
- [ ] test_date_and_time_fields_are_set


Unhappy Paths:
- [x] Should fail if throttle limit is reached
- [x] should fail if number is invalid
- [x] should fail if number is not provided

### GUEST/NORMAL USER
Happy Paths:
- [x] should be able to create score if user is authenticated
    - [x] response should return: number, uuid, date/times
- [x] created score should have user_id that matches the user id of the authenticated user
- [ ] test_date_and_time_fields_are_set


Unhappy Paths:
- [x] should fail if a score has already been created today
- [x] should fail if number is invalid
- [x] should fail if number is not provided



## SCORE UPDATE

### ANON USER
Unhappy Paths:
- [x] should fail if number is invalid
- [x] should fail if number is not provided
- [x] should fail user is anonymous
- [x] should fail user tried to update score not created by them

### GUEST/NORMAL USER

Happy Paths:
- [ ] Should succced if exists
    - [ ] should be possible to update: time, number
    - [ ] response should return: number, uuid, date, time

Unhappy Paths:
- [ ] should fail if it doesn't exist
- [ ] should fail if no uuid is passed or is invalid



## SCORE GET

### ANON USER
- [ ] Should always fail

### GUEST/NORMAL USER

Happy Paths:
- [ ] Shoud succced if exists
    - [ ] response should return: number, uuid, date/times

Unhappy Paths:
- [ ] should fail if it doesn't exist
- [ ] should fail if no uuid is passed or is invalid

## SCORE DELETE
- [ ] should always fail