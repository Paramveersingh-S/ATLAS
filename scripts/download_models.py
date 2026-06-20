import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str)
    parser.add_argument("--embedding", type=str)
    args = parser.parse_args()
    print(f"Downloading model {args.model} and embedding {args.embedding}...")
    
if __name__ == "__main__":
    main()
