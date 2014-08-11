class Validator:
    def check_str(val):
        val = val.strip()
        return (1, val) if val else (0, "This can't be empty")

    def check_num(val):
        try:
            return (1, float(val))
        except ValueError:
            return (0, "That's not a number.")

    def check_unsigned_num(val):
        try:
            val = float(val)
            if val < 0: raise ValueError
            return (1, val)
        except ValueError:
            return (0, "That's not an unsigned number.")

    validators = {
        'Str'         : check_str,
        'Num'         : check_num,
        'UnsignedNum' : check_unsigned_num,
    }

    def __init__(self, forms):
        self.forms = forms

    def validate(self, what, fields):
        form    = self.forms[what]
        valid   = 1
        results = {}
        errors  = {}
        for f in form['fields']:
            key     = f['name']
            ok, res = Validator.validators[f['type']](getattr(fields, key))
            valid   = valid and ok
            if valid:
                results[key] = res
            else:
                results      = errors
                errors[key]  = res
        return valid, results
