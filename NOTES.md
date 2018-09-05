Install a Python 2 virtualenv
```bash
virtualenv venv2
. venv2/bin/activate
pip install -r requirements.txt
```

Launch an EC2 instance to build on
```bash
fab -f fabfile_builder.py launch
```

Build the runtime

```bash
fab -f fabfile_builder.py -R builder -i ~/.ec2/ec2-us-west-2.pem install_dev
#fab -f fabfile_builder.py -R builder -i ~/.ec2/ec2-us-west-2.pem build_single_runtime:default,3.6
fab -f fabfile_builder.py -R builder -i ~/.ec2/ec2-us-west-2.pem build_all_runtimes
#fab -f fabfile_builder.py -R builder -i ~/.ec2/ec2-us-west-2.pem deploy_runtimes:num_shards=50
fab -f fabfile_builder.py -R builder -i ~/.ec2/ec2-us-west-2.pem deploy_runtimes:num_shards=2
```

Don't forget to shut down the EC2 instance:
```bash
fab -f fabfile_builder.py -R builder -i ~/.ec2/ec2-us-west-2.pem terminate
```