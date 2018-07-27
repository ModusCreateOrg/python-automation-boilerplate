from gherkin.token_scanner import TokenScanner
from gherkin.parser import Parser


def get_feature(file_path):
    """ Read and parse given feature file"""
    print('Reading feature file ', file_path)
    file_obj = open(file_path, "r")
    steam = file_obj.read()
    parser = Parser()
    return parser.parse(TokenScanner(steam))
