def choice_prompt(choices, prompt, **args):
    # TODO: 'default' option implementation
    print prompt
    for i, choice in enumerate(choices):
        print " %d) %s" % (i, choice)
    selection = raw_input("Enter your choice: ")
    return int(selection)


def text_prompt(prompt, **args):
    # TODO: 'default' input implementation
    selection = raw_input('%s ' % prompt)
    return selection