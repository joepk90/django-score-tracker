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
- [ ] test date and time fields are set


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
- [x] should fail user tries to update score not owned by them

### GUEST/NORMAL USER

Happy Paths:
- [x] Should succed if exists and update number property
- [x] updating a score should update the time_updated property

Unhappy Paths:
- [x] should fail if score doesn't exist
- [x] should fail if uuid is invalid
- [x] should fail if number is invalid
- [x] should fail if no number is provied
- [x] should fail user tries to update score not owned by them
- [x] should fail to update scores created on previous days




## SCORE GET

### ANON USER
- [x] Should always fail

### GUEST/NORMAL USER

Happy Paths:
- [x] Shoud succced if exists
    - [x] response should return: number, uuid, date

Unhappy Paths:
- [x] should fail if it doesn't exist
- [x] should fail if uuid is invalid
- [x] should fail if user tries to retrieve score not owned by them
- [x] should fail if user tries to retrieve score not owned by anyone (None)

## SCORE DELETE
- [ ] should always fail