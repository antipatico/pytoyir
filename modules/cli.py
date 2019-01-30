from .utils import lazyInt


def confirm(question):
    print(question, "(y/N) ", end="")
    return input() in ["y", "yes", "Y", "YES"]


def selectOptionsText(question, options):
    while True:
        r = range(len(options))
        for i in r:
            print(i, options[i])

        selection = lazyInt(input(question))
        if selection in r:
            return options[selection]
