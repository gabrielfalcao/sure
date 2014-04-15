import six

if six.PY3:
    def compat_repr(object_repr):
        return object_repr
else:
    def compat_repr(object_repr):
        # compat_repr is designed to return all reprs with leading 'u's
        # inserted to make all strings look like unicode strings.
        # This makes testing between py2 and py3 much easier.
        result = ''
        in_quote = False
        curr_quote = None
        for char in object_repr:
            if char in ['"', "'"] and (
                not curr_quote or char == curr_quote):
                if in_quote:
                    # Closing quote
                    curr_quote = None
                    in_quote = False
                else:
                    # Opening quote
                    curr_quote = char
                    result += 'u'
                    in_quote = True
            result += char
        return result

text_type_name = six.text_type().__class__.__name__
