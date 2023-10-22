#!/bin/sh
g++ poly.cpp -o poly -fconcepts -O0
strip -w -N _Z[0-9]* -N key -N secret[1-3] -N inv -N w poly
