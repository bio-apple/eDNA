import os,sys,re
import subprocess
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-","--input",help="input file",required=True)