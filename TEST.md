# Various test runs

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

BUGS WITH NEGATIVE NUMBERS/ UNARY OP
ShadowScript: -5>-6
-1 <=== BUG TO BE FIXED - SHOULD BE 1
ShadowScript: -3> -100 - NEGATIVE NUMBERS / UNARY OPS NOT WORKING PROPERLY!
-1 <=== BUG TO BE FIXED - SHOULD BE 1

ShadowScript: -5?=-6
0
ShadowScript: -5?=-5
0 <=== BUG TO BE FIXED - SHOULD BE 1 - NEGATIVE NUMBERS / UNARY OPS NOT WORKING PROPERLY!
ShadowScript: 5?=5
1
ShadowScript: -5 ?= -5
0 <=== BUG TO BE FIXED - SHOULD BE 1 - NEGATIVE NUMBERS / UNARY OPS NOT WORKING PROPERLY!


ShadowScript: -(5*5)
-25
ShadowScript: (-5*-5)
25
ShadowScript: -(-5*-5)
-25


ShadowScript: if 5 > 2 do make a = 3
{'a': 3}

ShadowScript: if 5 ?= ((5)) do make b = a
{'a': 3, 'b': a} <=== SHOULD BE {'a': 3, 'b': 3} - VARIABLES ARE NOT BEING 'READ' FOR EXPRESSIONS
ShadowScript: if 5?=5 do make b = 100
{'a': 3, 'b': 100}

CANNOT USE VARIABLES AT ALL IN EXPRESSIONS
ShadowScript: a+b
ShadowScript: a+1

YET THIS WORKS:
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

ALTHOUGH THIS WORKS HOWEVER 'a' IS BEING INTERPRETED AS floats

