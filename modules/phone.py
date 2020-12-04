from re import compile


def get(message):
    if message.contact and message.from_user.id == message.contact.user_id:
        if check(message.contact.phone_number):
            return message.contact.phone_number
        else:
            return f'+{message.contact.phone_number}'
    else:
        return message.text


def check(phone_number):
    pattern = compile(r'[/+](\b\d+\b)+$')
    is_valid = pattern.match(phone_number)
    return is_valid
