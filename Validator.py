class Validator:
    def check_str(val):
        val = val.strip()
        if not val:
            raise ValueError("This can't be empty.")
        return val

    def check_num(val):
        return float(val)

    def check_unsigned_num(val):
        val = float(val)
        if val < 0:
            raise ValueError("That's not an unsigned number.")
        return val

    validators = {
        'Str'         : check_str,
        'Num'         : check_num,
        'UnsignedNum' : check_unsigned_num,
    }

    def __init__(self, forms):
        self.forms = forms

    def validate(self, what, fields):
        form    = self.forms[what]
        results = {}
        errors  = {}
        for f in form['fields']:
            key = f['name']
            val = getattr(fields, key)
            try:
                results[key] = Validator.validators[f['type']](val)
            except ValueError as e:
                errors [key] = str(e)
        return not errors, errors if errors else results
