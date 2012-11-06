def scrub_json_unicode_to_string(obj):
    # helper method to turn the unicode into string for a json import.
    new_obj = {}
    for k, values in obj.iteritems():
        key = str(k)
        if values is None:
            new_obj[key] = None
            continue

        new_values = []
        for v in values:
            if v:
                new_values.append(str(v))

        new_obj[key] = new_values
    return new_obj

