class Expr:
    pass

class Binary(Expr):
    def __init__(self, expr_left, operator_token, expr_right):
        self.expr_left = expr_left
        self.operator_token = operator_token
        self.expr_right = expr_right

class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

class Literal(Expr):
    def __init__(self, object_value):
        self.object_value = object_value

class Unary(Expr):
    def __init__(self, operator_token, expr_right):
        self.operator_token = operator_token
        self.expr_right = expr_right

