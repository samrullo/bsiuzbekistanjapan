# Dynamically populating SelectField choices

If you assign ```choices``` at initialization you can't change it afterwards.
In my case I wanted to set ```choices``` of ```from_country```
SelectField to countries saved in the database.

But I was getting error saying "No application found blah blah...".
Basically, flask was complaining that I am trying 
to access database outside of application context.

Solution was populating choices dynamically inside view function.

```python
form.from_country.choices = [(country.id, country.country_name) for country in Country.query.all()]
form.to_country.choices = [(country.id, country.country_name) for country in Country.query.all()]
form.represented_individual.choices = [(represented_individual.id, represented_individual.name) for
                                       represented_individual in current_user.represented_individuals]
form.recipient.choices = [(recipient.id, recipient.name) for recipient in current_user.recipients]
```

Then I was getting ``Not a valid choice`` error. 
Apparently this had to do ``id`` field being int, while SelectField expects a string value.

Solution was setting ```valid_choice``` argument of SelectField to False.

```python
from_country = SelectField(_("From country"), coerce=int, validate_choice=False)
to_country = SelectField(_("To country"), coerce=int, validate_choice=False)
represented_individual = SelectField(_("Represented individual"), coerce=int, validate_choice=False)
recipient = SelectField(_("Recipient"), coerce=int, validate_choice=False)
```