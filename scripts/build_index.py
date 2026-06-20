import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, required=True)
    args = parser.parse_args()
    print(f"Batch indexing directory {args.dir}...")

if __name__ == "__main__":
    main()
