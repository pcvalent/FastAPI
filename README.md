# FastAPI
# Documentation on using FastAPI

This space provides information on the use of FastAPI from an approach that covers the basic concepts and its implementation for the development of APIs with python.

## General description

FastAPI is a high-performance framework for creating APIs with python. This is based on the frameworks of :

- **Starlette:**  is a lightweight ASGI framework/toolkit, which is ideal for building async web services in Python.
- **Pydanic:**  is a python library for performing data validation
- **Uvicorn:** A library that works as a server, allows any computer to become a server. Allows you to run applications

## Installation

1. **Creation of the virtual environment.**

```bash
  - pip install fastapi
  - pip install uvicorn
```

2. **Creation of main.py file.**
  This file contains variables, information about     versions and functions

3. **Execution**
```bash
  - uvicorn main:app --reload
  
```
