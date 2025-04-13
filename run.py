from NovaNotes import NovaNotes
from config import *

text_mode = False
client = NovaNotes(gpt_api_key = API_KEY, el_api_key=EL_API_KEY, text_mode = text_mode)

def main():
    client.run_novanote()

if __name__ == '__main__':
    main()
