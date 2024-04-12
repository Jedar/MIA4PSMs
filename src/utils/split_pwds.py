import argparse

def init_cli():
    cli = argparse.ArgumentParser("Split query passwords")
    cli.add_argument("-i", dest="input")
    cli.add_argument("-o", dest="output")
    return cli.parse_args()

def main():
    args = init_cli()
    input_file = args.input 
    output_file = args.output 
    pwds = []
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip("\r\n")
            pwd = line.split("\t")[0]
            pwds.append(pwd)
    
    with open(output_file, "w") as f:
        for pwd in pwds:
            f.write(f"{pwd}\n")
    print(f"File saved: {output_file}")
    pass

if __name__ == '__main__':
    main()