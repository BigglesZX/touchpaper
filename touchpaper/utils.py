def choice_prompt(choices, prompt, **args):
    # TODO: 'default' option implementation
    print prompt
    for i, choice in enumerate(choices):
        print " %d) %s" % (i, choice)
    selection = raw_input("Enter your choice: ")
    return int(selection)


def get_instance_types():
    return [
        "t1.micro",
        "m1.small",
        "m1.medium",
        "m1.large",
        "m1.xlarge",
        "m3.xlarge",
        "m3.2xlarge",
        "c1.medium",
        "c1.xlarge",
        "m2.xlarge",
        "m2.2xlarge",
        "m2.4xlarge",
        "cr1.8xlarge",
        "hi1.4xlarge",
        "hs1.8xlarge",
        "cc1.4xlarge",
        "cg1.4xlarge",
        "cc2.8xlarge",
        "g2.2xlarge",
        "c3.large",
        "c3.xlarge",
        "c3.2xlarge",
        "c3.4xlarge",
        "c3.8xlarge",
        "i2.xlarge",
        "i2.2xlarge",
        "i2.4xlarge",
        "i2.8xlarge",
    ]


def text_prompt(prompt, **args):
    # TODO: 'default' input implementation
    selection = raw_input('%s ' % prompt)
    return selection
