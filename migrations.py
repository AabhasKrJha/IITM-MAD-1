import subprocess

def run_command(command):
    try:
        print(f"Running command: {command}")
        result = subprocess.run(command, shell=True, check=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
        exit(1)

def main():
    # List of commands to run sequentially

    migration = input("Enter Migration name : ")
    commands = [
        f'flask db migrate -m "{migration}"',
        'flask db upgrade'
    ]
    
    for cmd in commands:
        run_command(cmd)

if __name__ == "__main__":
    main()
