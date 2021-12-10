class RegularExp:
    def __init__(self, regex, requires_parenthesis=False):
        self.regex = regex
        self.requires_parenthesis = requires_parenthesis
    
    def __add__(self, other):
        if self.requires_parenthesis and other.requires_parenthesis:
            template = "({})+({})"
        elif self.requires_parenthesis:
            template = "({})+{}"
        elif other.requires_parenthesis:
            template = "{}+({})"
        else:
            template = "{}+{}"
        return RegularExp(template.format(self.regex, other.regex), True)
    
    def __xor__(self, other):
        if (other.regex == "e"):
            return RegularExp(self.regex, self.requires_parenthesis)
        elif (self.regex == "e"):
            return RegularExp(other.regex, other.requires_parenthesis)

        if self.requires_parenthesis and other.requires_parenthesis:
            template = "({})({})"
        elif self.requires_parenthesis:
            template = "({}){}"
        elif other.requires_parenthesis:
            template = "{}({})"
        else:
            template = "{}{}"
        return RegularExp(template.format(self.regex, other.regex), False)

    def star(self):
        if (self.regex == "e"):
            return RegularExp("", False)
        if len(self.regex) == 1:
            template = "{}*"
        else:
            template = "({})*"
        return RegularExp(template.format(self.regex), False)

    def __str__(self):
        return self.regex

    def __len__(self):
        return len(self.regex)