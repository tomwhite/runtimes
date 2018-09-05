import os
import hashlib

# Pin version numbers to match s3://pywren-public-us-east-1/pywren.runtimes/default_3.6.meta.json
CONDA_DEFAULT_LIST = [
    "numpy=1.13.1=py36_0",
    "numba=0.34.0",
    "scipy=0.19.1",
    "tblib=1.3.2",
    "pyyaml=3.12=py36_0",
    "six=1.10.0",
    "future=0.16.0",
    "numba=0.34.0",
    "mkl=2017.0.3=0"
]

PIP_DEFAULT_LIST = ['glob2==0.6', 'boto==2.48.0', 'boto3==1.4.7', 'certifi', 'zarr', 'git+https://github.com/tomwhite/numcodecs@lambda']
PIP_DEFAULT_UPGRADE_LIST = ['cloudpickle==0.4.0', 'enum34==1.1.6']

CONDA_ML_SET = ['scipy', 'pillow', 'cvxopt', 'scikit-learn']
PIP_ML_SET = ['cvxpy', 'redis']

CONDA_OPT_SET = ['scipy', 'cvxopt', ('mosek', 'mosek')]
PIP_OPT_SET = ['cvxpy' ]

RUNTIMES = {'default' : {'pythonvers' : ["3.6"],
                         'packages' : {
                             'conda_install' : CONDA_DEFAULT_LIST,
                             'pip_install' : PIP_DEFAULT_LIST,
                             'pip_upgrade' : PIP_DEFAULT_UPGRADE_LIST}}
}



CONDA_TEST_STRS = {'numpy' : "__import__('numpy')", 
                   'pytest' : "__import__('pytest')", 
                   "numba" : "__import__('numba')", 
                   "boto3" : "__import__('boto3')", 
                   "PyYAML" : "__import__('yaml')", 
                   "boto" : "__import__('boto')", 
                   "scipy" : "__import__('scipy')", 
                   "pillow" : "__import__('PIL.Image')", 
                   "cvxopt" : "__import__('cvxopt')", 
                   "scikit-image" : "__import__('skimage')", 
                   "scikit-learn" : "__import__('sklearn')"}
PIP_TEST_STRS = {"glob2" : "__import__('glob2')", 
                 "cvxpy" : "__import__('cvxpy')", 
                 "redis" : "__import__('redis')", 
                 "certifi": "__import__('certifi')"}

S3_BUCKET = "s3://tom-pywren-runtimes"
S3URL_STAGING_BASE = S3_BUCKET + "/pywren.runtime.staging"
S3URL_BASE = S3_BUCKET + "/pywren.runtime"

def get_staged_runtime_url(runtime_name, runtime_python_version):
    s3url = "{}/pywren_runtime-{}-{}".format(S3URL_STAGING_BASE, 
                                             runtime_python_version, runtime_name)

    return s3url + ".tar.gz", s3url + ".meta.json"

def get_runtime_url_from_staging(staging_url):
    s3_url_base, s3_filename = os.path.split(staging_url)
    release_url = "{}/{}".format(S3URL_BASE, s3_filename)

    return release_url

def hash_s3_key(s):
    """
    MD5-hash the contents of an S3 key to enable good partitioning.
    used for sharding the runtimes
    """
    DIGEST_LEN = 6
    m = hashlib.md5()
    m.update(s.encode('ascii'))
    digest = m.hexdigest()
    return "{}-{}".format(digest[:DIGEST_LEN], s)

def get_s3_shard(key, shard_num):
    return "{}.{:04d}".format(key, shard_num)

def split_s3_url(s3_url):
    if s3_url[:5] != "s3://":
        raise ValueError("URL {} is not valid".format(s3_url))


    splits = s3_url[5:].split("/")
    bucket_name = splits[0]
    key = "/".join(splits[1:])
    return bucket_name, key
