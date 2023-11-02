# PyUtils
Repository of general purpose utility functions in Python.

Curation of general purpose tools so that you don't have to write the basic stuff ever again.

## ToDo
- [x] create empty logging.json file
- [x] add sample logging.json (with and without stream handler)
- [x] add module for setting up (and showing the usage of) the argument parser
- [ ] sample code for `sphinx` setup
- [ ] create documentation for this repo
- [x] create a directory named `aws` containing the AWS related utils codebase
- [ ] add Python file for accessing RDS tables, creating and updating Secrets in Secrets Manager
  - [ ] for RDS:
    - [ ] add functions for adding, deleting, and altering columns
    - [ ] add functions for creating and altering tables
    - [ ] funcs for checking column names and respective datatypes
- [ ] multithreading s3 operations upload and download functions
- [ ] add another function for read and validate datatypes
- [x] add function for `timeit` decorator
- [ ] `poetry` dependency manager for the repo
- [ ] add functionalities for automatic retries using `retry`
- [ ] functions for raising `timeoutError`


## Miscellaneous 
- [ ] Milvus experiments as a new repo.
  - [ ] generate sample data for `/data` directory
- [ ] Repositories for:
  - [ ] Audio clipper (with file merger logic + denoiser*)
  - [ ] ASR comparisions (includes live transcription with multilingual support)
  - [ ] LLM notes
  - [ ] Memory profiling and identification of memory leaks
