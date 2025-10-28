Description of the taskfile
==============================

# Summary
This Taskfile defines automation tasks for managing AWS Lambda layer packaging and deployment. It includes tasks to build a Lambda layer zip file using a shell script, check the unzipped and zipped size of the layer to ensure it does not exceed AWS Lambda’s 250MB limit, and upload the layer zip to a specified S3 bucket and directory. The process ensures that only valid, size-compliant layers are pushed to S3, streamlining Lambda layer management and deployment.

# Task description
### 1. `create-layer-zip`
Description: Triggers the shell script create_layer.sh to build the Lambda layer zip file. This script typically installs dependencies and packages them into a zip archive suitable for AWS Lambda layers.

### 2. `check-layer-size`
Description: Checks the size of the Lambda layer zip file to ensure it does not exceed AWS Lambda’s 250MB unzipped layer size limit.
Steps:
  - Unzips the layer zip file into a temporary directory.
  - Calculates and prints the unzipped size.
  - Deletes the temporary directory.
  - Prints the size of the zip file itself.
  - If the unzipped size exceeds 250MB, prints an error and exits with a non-zero status; otherwise, confirms the size is within the limit.
    
### 3. `push-layer`
Description: Uploads the Lambda layer zip file to the specified S3 bucket and directory, but only after verifying the layer size with the check-layer-size task.
Steps:
  - Checks if the zip file exists in the specified directory.
  - If not found, prints an error and exits.
  - If found, uploads the zip file to the S3 bucket and directory using `aws s3 cp`.
  - Prints a success message after upload.

---

## Reference doc: https://medium.com/simform-engineering/creating-lambda-layers-made-easy-with-docker-a-developers-guide-3bcfcf32d7c3
