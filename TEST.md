# Various test runs

* T01 - TESTS THE INITAL STATE OF ShadowScript - Highlighting any errors
* T02 - FIX UNARY BUG


# T01 - INITIAL TESTS
```
ShadowScript: 8
8
ShadowScript: 8+8
16
ShadowScript: 8-9
-1
ShadowScript: 9*7
63
ShadowScript: 5/6
0.8333333333333334


ShadowScript: -5/+5
-1
ShadowScript: -5 * -5
25
ShadowScript: -5 * +5  
-25
ShadowScript: (5 + 3) or (7 * 8)
1
ShadowScript: (5 + 30) and (8 ?= 9)
0
ShadowScript: 7>=9
0
ShadowScript: 7>=4
1
ShadowScript: 5<=9
1
ShadowScript: not 1?=2
1

ShadowScript: 5>6
0
ShadowScript: 5>2
1
```

**BUGS WITH NEGATIVE NUMBERS/ UNARY OP**<br>
ShadowScript: -5>-6<br>
-1 <=== BUG TO BE FIXED - SHOULD BE 1<br>
ShadowScript: -3> -100 - ``` **NEGATIVE NUMBERS / UNARY OPS NOT WORKING PROPERLY!**<br>
-1 <=== BUG TO BE FIXED - SHOULD BE 1
```

ShadowScript: -5?=-6
0
ShadowScript: -5?=-5
```
0 <=== BUG TO BE FIXED - **SHOULD BE 1 - NEGATIVE NUMBERS / UNARY OPS NOT WORKING PROPERLY!**<br>
ShadowScript: 5?=5<br>
1<br>
ShadowScript: -5 ?= -5
0 <=== BUG TO BE FIXED - **SHOULD BE 1 - NEGATIVE NUMBERS / UNARY OPS NOT WORKING PROPERLY!**<br>

```
ShadowScript: -(5*5)
-25
ShadowScript: (-5*-5)
25
ShadowScript: -(-5*-5)
-25


ShadowScript: if 5 > 2 do make a = 3
{'a': 3}

ShadowScript: if 5 ?= ((5)) do make b = a
```
**VARIABLES ARE NOT BEING 'READ' FOR EXPRESSIONS**<br>
{'a': 3, 'b': a} <=== SHOULD BE {'a': 3, 'b': 3}<br>
ShadowScript: if 5?=5 do make b = 100<br>
{'a': 3, 'b': 100}<br>

**CANNOT USE VARIABLES AT ALL IN EXPRESSIONS**<br>
ShadowScript: a+b<br>
ShadowScript: a+1<br>

**YET THIS WORKS:**
```
ShadowScript: if 5?=5 do make b=a+1
{'a': 3, 'b': 4}


ShadowScript: make a = 0
{'a': 0, 'b': 4}
ShadowScript: while a < 10 do make a = a + 1
{'a': 1, 'b': 4}
{'a': 2.0, 'b': 4}
{'a': 3.0, 'b': 4}
{'a': 4.0, 'b': 4}
{'a': 5.0, 'b': 4}
{'a': 6.0, 'b': 4}
{'a': 7.0, 'b': 4}
{'a': 8.0, 'b': 4}
{'a': 9.0, 'b': 4}
{'a': 10.0, 'b': 4}
```
**ALTHOUGH THE ABOVE WORKS HOWEVER 'a' IS BEING INTERPRETED AS floats**


# T02 - FIX UNARY BUG
```
ShadowScript: -5>-6
[-, [5, >, [-, 6]]]
-1

BEING PARSED INCORRECTLY
ShadowScript: -5>-6
TK - OP
TK 5 INT
TK - OP
TK 6 INT
[-, [5, >, [-, 6]]]
[-, [5, >, [-, 6]]]
100 [5, >, [-, 6]]
[-, 6]
100 6
101 [-, 6]
101 [-, [5, >, [-, 6]]] ==> SHOULD BE [[-, 5], >, [-, 6]]


BEING PARSED INCORRECTLY
ShadowScript: -5>6
TK - OP
TK 5 INT
TK 6 INT
[-, [5, >, 6]]
[-, [5, >, 6]]
100 [5, >, 6]
101 [-, [5, >, 6]] ==> SHOULD BE [[-, 5], >, 6]

PARSE.PY CHANGED:

        # not <expr>
        elif self.token.value == 'not':
            operator = self.token
            self.move()
            output = [operator, self.boolean_expression()] <=== CHANGE THIS
            return output
TO
	        output = [operator, self.factor()]


I ALSO MAKE THE SAME CHANGE HERE

        # not <expr>
        elif self.token.value == 'not':
            operator = self.token
            self.move()
            output = [operator, self.boolean_expression()] <=== CHANGE THIS
            return output
TO
	        output = [operator, self.factor()]


ShadowScript: -5>6
NOW PARSED AS
[[-, 5], >, 6]
WITH THE RESULT
0


ShadowScript: -5>-6
NOW PARSED AS
[[-, 5], >, [-, 6]]
WITH THE RESULT
1

DO THE TESTS AGAIN SHOWING THE PARSE TREE AS WELL
ShadowScript: -5>-6
[[-, 5], >, [-, 6]]
1

ShadowScript: -5>6
[[-, 5], >, 6]
0

ShadowScript: -3 > -100
[[-, 3], >, [-, 100]]
1

ShadowScript: -5?=-6
[[-, 5], ?=, [-, 6]]
0
ShadowScript: -5?=-5
[[-, 5], ?=, [-, 5]]
1
ShadowScript: 5?=5
[5, ?=, 5]
1
ShadowScript: -5 ?= -5
[[-, 5], ?=, [-, 5]]
1

ShadowScript: not 0
[not, 0]
1

ShadowScript: not not 0
[not, [not, 0]]
0

ShadowScript: not not not 0
[not, [not, [not, 0]]]
1

```