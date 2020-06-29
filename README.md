# aws_deployment
deployment using boto3

## Run to create cloudformation stack
python3 stacks.py

This command has to be run after the jenkins build is successful in [helloworld_webapp](https://github.com/vishraparthi9/helloworld_webapp).
The jenkins build will create a helloworld-xxxx-yyyy.tar.gz. Extract the tar and then run `python3 stacks.py`
