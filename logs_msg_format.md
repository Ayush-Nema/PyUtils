Message formatting in logging.json
====================================

There are different ways for formatting the log message, the following ones are useful and widely used:  

1. Full filepath: too much verbose output  
```json
"formatters": {
    "package_formatter": {
      "format": "[%(asctime)s] - [%(levelname)s] - [%(pathname)s:%(lineno)d] : [%(name)s.%(funcName)s]: %(message)s",
      "datefmt": "%m/%d/%Y %I:%M:%S %p"
    }
```

2. File path relative to caller function: mildly verbose
```json
"formatters": {
    "package_formatter": {
      "format": "[%(asctime)s] ∷ [%(levelname)s] ∷ [%(name)s.%(funcName)s:%(lineno)d] ≔⊙⧟↣ %(message)s",
      "datefmt": "%m/%d/%Y %I:%M:%S %p"
    }
```

3. File name and function name: more useful and crisp
```json
"formatters": {
    "package_formatter": {
      "format": "[%(asctime)s] ∷ [%(levelname)s] ∷ [%(filename)s.%(funcName)s:%(lineno)d] ≔⊙⧟↣ %(message)s",
      "datefmt": "%m/%d/%Y %I:%M:%S %p"
    }
```


## Helpful links
1. More details to format the file with different handlers: [Click here](https://gist.github.com/kingspp/9451566a5555fb022215ca2b7b802f19)
