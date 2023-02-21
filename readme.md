# Django Score Tracker 
## API to track score ratings

Used https://github.com/joepk90/django-example-app as a base.
Includes an accounts app to handle + djoser to handle authentication


### Number Value Storage Strategy
https://stackoverflow.com/questions/2569015/django-floatfield-or-decimalfield-for-currency#answer-50376841

To prevent storing decimals in the database, the PositiveSmallIntegerField
The number field has the folliwing min/max values:
- min 0
- max: 1000

Clients should convert the the number to decimal to represent a decimal value between 1-10
```
console.log((999/100).toFixed(2));
# output 9.99
```

https://stackoverflow.com/questions/2569015/django-floatfield-or-decimalfield-for-currency#answer-50376841