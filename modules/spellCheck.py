import enchant

d = enchant.Dict("en_US")


def correct(query):
    corrected = []
    for word in query.split(" "):
        if not d.check(word):
            suggested = d.suggest(word)
            corrected.append(suggested[0] if len(suggested) else word)
        else:
            corrected.append(word)
    return " ".join(corrected)
