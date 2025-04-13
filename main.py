from NovaNotes import NovaNotes

client = NovaNotes()

def main():
    responses = client.run_inference('test.jpg')
    for r in responses:
        print(r)
    

if __name__ == '__main__':
    main()