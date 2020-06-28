import boto3
from jinja2 import Environment, FileSystemLoader
import argparse
import json
from datetime import datetime
import base64

def create_stack(args, kw):

  read_config(args, kw)
  data = generate_template(kw)

  client = boto3.client('cloudformation')

  response = client.create_stack(
    StackName = kw['env'] + "-" + kw['app_name'] + "-" + kw['current_timestamp'],
    TemplateBody = data,
    TimeoutInMinutes = 20,
    Tags=kw['tags']
  )

  print(response)

def generate_template(kw):
  template_data = ""

  file_loader = FileSystemLoader('templates')
  env = Environment(loader=file_loader)

  template = env.get_template('cfn.jinja')

  output = template.render(kw=kw)
  print(output)
  return output

def read_config(args, kw):

  kw['current_timestamp'] = datetime.now().isoformat().replace(':','').replace('.','').replace('-','')
  kw['env'] = args.env

  with open(args.accConfigFile, "r") as account_config_file:
    kw1 = json.load(account_config_file)[args.account]

  kw.update(kw1)

  with open(args.configFile, "r") as app_config_file:
    kw1 = json.load(app_config_file)[args.env]

  kw.update(kw1)

  with open("user_data.sh", "r") as ud:
    user_data = ud.read()

  user_data_bytes = user_data.encode()
  user_data_base64 = base64.b64encode(user_data_bytes).decode('ascii')

  kw['user_data'] = user_data_base64

  tags=[
        {
            'Key': 'bu',
            'Value': kw['bu']
        },
        {
            'Key': 'product',
            'Value': kw['product']
        },
        {
            'Key': 'env',
            'Value': kw['env']
        }
  ]
  asg_tags=[
        {
            'Key': 'bu',
            'Value': kw['bu'],
            'PropagateAtLaunch': 'true'
        },
        {
            'Key': 'product',
            'Value': kw['product'],
            'PropagateAtLaunch': 'true'
        },
        {
            'Key': 'env',
            'Value': kw['env'],
            'PropagateAtLaunch': 'true'
        }
  ]
  kw['tags'] = tags
  kw['asg_tags'] = asg_tags

if __name__ == "__main__":

  description = "Code to create AWS Cloudformation stacks"
  parser = argparse.ArgumentParser(description=description)

  parser.add_argument("-a", "--account", help="AWS Account type: nonprod, prod etc.", default="nonprod")
  parser.add_argument("-e", "--env", help="Environment to deploy", default="dev")
  parser.add_argument("-f", "--configFile", help="App config file", default="config/app.json")
  parser.add_argument("-F", "--accConfigFile", help="AWS Account config file", default="config/accounts.json")

  args = parser.parse_args()

  create_stack(args, dict())