from pipeline import process_annotations

def main():
    print(process_annotations('test.jpg', scale_factor = 1.2))
    
if __name__ == '__main__':
    main()