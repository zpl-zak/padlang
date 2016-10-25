# PADLang [![Build Status](https://travis-ci.org/zaklaus/padlang.svg?branch=master)](https://travis-ci.org/zaklaus/padlang) [![Apache 2 licensed](https://img.shields.io/hexpm/l/plug.svg?maxAge=2592000)](https://github.com/arogan-group/DZMLang/blob/master/LICENSE)

Yet another language written in Python.

## Contains
* Basic parser for converting tokens into AST (Abstract syntax tree).
* Interpreter. Handles the flow of instructions in AST.
* Contains basic types: Integer, Real.
* Scoping, ie. scope can have its own local variables and still access those declared in outer scope.
* Methods with their own scope. They clone program's main scope rules, therefore they support nested methods.
* Conditional statements
* Case switch
* Basic variable existence checks when using variables.
* Variable references (ex. you can pass variable reference to a procedure, which can then modify it.)
* Supports basic Pascal-esque programs. (This won't be true soon.)

## How to use
* Either clone the repo or `pip install padlang`, see *samples* for an example of how to use the package.

## Copyright
* PADLang is licensed under the **Apache 2 License**, see LICENSE for more information.
