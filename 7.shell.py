import subprocess
import sys
import os

def execute_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except FileNotFoundError as e:
        print(f"Error: Command not found: {command}")

def main():
    while True:
        user_input = input("$ ").strip()
        if not user_input:
            continue

        if '|' in user_input:  
            commands = user_input.split('|')
            processes = []
            for i, cmd in enumerate(commands):
                if i == 0:
                    processes.append(subprocess.Popen(cmd.strip().split(), stdout=subprocess.PIPE))
                elif i == len(commands) - 1:
                    processes.append(subprocess.Popen(cmd.strip().split(), stdin=processes[-1].stdout))
                else:
                    processes.append(subprocess.Popen(cmd.strip().split(), stdin=processes[-1].stdout, stdout=subprocess.PIPE))
            for process in processes:
                process.communicate()
        elif '>' in user_input:
            command, output_file = user_input.split('>')
            command = command.strip()
            output_file = output_file.strip()
            with open(output_file, 'w') as f:
                subprocess.run(command.split(), stdout=f)
        elif '<' in user_input:
            command, input_file = user_input.split('<')
            command = command.strip()
            input_file = input_file.strip()
            with open(input_file, 'r') as f:
                subprocess.run(command.split(), stdin=f)
        else:
            execute_command(user_input)

if __name__ == "__main__":
    main()