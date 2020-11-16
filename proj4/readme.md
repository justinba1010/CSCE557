# Quadratic Sieve

# Usage

## Help

`./driver.py -h`

## Input by File

`./driver.py -i inputfile`

Input is defined as a number on a line in a file

## Output to File

`./driver.py -o outputfile`

## Input by arg

`./driver -p N`

## Parameters

Changes the amount of searching that goes into the sieve

`./driver -k K`

Changes how smooth the numbers are

`./driver -f F`

## Libraries

I used `sympy` for linear algebra operations. If it is not installed,
`pip3 install sympy`
And if using `pypy3`
`pypy3 -m pip install sympy`


## Examples

```
➜  proj4 ✗ time (python3 driver.py -p 100020320266631 -k 40000 -f 50)
The factors are: 
10001891
10000141
( python3 driver.py -p 100020320266631 -k 40000 -f 50; )  0.84s user 0.08s system 97% cpu 0.947 total

➜  proj4 ✗ time (python3 driver.py -p 100020320266633 -k 40000 -f 50)
The factors are: 
3029
429271760801
233
33020904677
( python3 driver.py -p 100020320266633 -k 40000 -f 50; )  1.00s user 0.08s system 99% cpu 1.094 total

➜  proj4 ✗ time (python3 driver.py -p 15)              
The factors are: 
3
5
( python3 driver.py -p 15; )  0.43s user 0.08s system 98% cpu 0.515 total

➜  proj4 ✗ time (python3 driver.py -p 153)
The factors are: 
17
9
( python3 driver.py -p 153; )  0.43s user 0.07s system 98% cpu 0.511 total
```

## View output
`less -r examplescript`
