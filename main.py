"""
A simple .drw generator by __hubblle

"""


from handwriting_synthesis import Hand
import os
import open_svg
import subprocess
import platform


def clear():
    os.system("cls" if os.name == "nt" else "clear")

LOGO = r"""
░███████   ░█████████  ░██       ░██                                                                       ░██                            ░██████    ░████     ░████     ░████   
░██   ░██  ░██     ░██ ░██       ░██                                                                       ░██                           ░██   ░██  ░██ ░██   ░██ ░██   ░██ ░██  
░██    ░██ ░██     ░██ ░██  ░██  ░██     ░████████  ░███████  ░████████   ░███████  ░██░████  ░██████   ░████████  ░███████  ░██░████          ░██ ░██ ░████ ░██ ░████ ░██ ░████ 
░██    ░██ ░█████████  ░██ ░████ ░██    ░██    ░██ ░██    ░██ ░██    ░██ ░██    ░██ ░███           ░██     ░██    ░██    ░██ ░███          ░█████  ░██░██░██ ░██░██░██ ░██░██░██ 
░██    ░██ ░██   ░██   ░██░██ ░██░██    ░██    ░██ ░█████████ ░██    ░██ ░█████████ ░██       ░███████     ░██    ░██    ░██ ░██               ░██ ░████ ░██ ░████ ░██ ░████ ░██ 
░██   ░██  ░██    ░██  ░████   ░████    ░██   ░███ ░██        ░██    ░██ ░██        ░██      ░██   ░██     ░██    ░██    ░██ ░██         ░██   ░██  ░██ ░██   ░██ ░██   ░██ ░██  
░███████   ░██     ░██ ░███     ░███     ░█████░██  ░███████  ░██    ░██  ░███████  ░██       ░█████░██     ░████  ░███████  ░██          ░██████    ░████     ░████     ░████   
                                               ░██                                                                                                                               
                                         ░███████                                                                                                                                                                                                                                                                                                             
"""

CHAR_BREAK=30
CHAR_BREAK_D = CHAR_BREAK

menu=[
    f"""
    {LOGO}
    
    Welcome into the .drw generator, let's start !
    """,
    f"""
    {LOGO}
    
    Please choose an option below
    """
]

OPTIONS={
    "biases":0.85,
    "styles":[1] 
}

HELP={
    "BIASES":"The biases is the Legibility between 0 and 1, one is the best, more robotic, and 0 is the worst, more chaotic.",
    "STYLES":"There are several styles available, please refer to https://www.calligrapher.ai/ to test them all.",
    "CHAR_BREAK":"Imported text is automatically cut into several lines, this rules how much characters are kept on one line."
}



#### Functions

def line(n=1):
    for _ in range(n):print("\n")


def generate_svg(lines:list, fname:str="output", options:dict=OPTIONS ):
    """This function use the handwriting_synthesis to generate 

    Args:
        lines (list): The lines to generate
        fname (str, optional): The filename. Defaults to "output".
        options (dict, optional): The options dict. Defaults to OPTIONS.
    """
    
    hand = Hand()
    
    # DISABLE TF INFO LOG, please, set to '2' or lower if you want every informations.
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '-1'
    
    biases = [options.get("biases", 0.85) for i in lines]
    styles = options.get("styles", 1)

    try:
        hand.write(
            filename=f"img/{fname}.svg",
            lines=lines,
            biases=biases,
            styles=styles,
        )
    except Exception as e:
        print(f"ERROR: an error occurred during the SVG file generation: {e}","\n","Please consider debugging or setting os.environ['TF_CPP_MIN_LOG_LEVEL'] to 2 or lower for more infos. ")
        exit(0)
        
    print(f"INFO: SVG file successfully generated to 'img/{fname}.svg'!")
    
def parse_txt(path:str)->list:
    """This function parse a .txt file and return a list containing lines of predefine length

    Args:
        path (str): The path of the file

    Returns:
        list: The line list
    """
    lines = []
    
    with open(path, "r") as f:
        content = f.read()
        q = len(content) // CHAR_BREAK
        r = len(content) % CHAR_BREAK
        
        for i in range(q):
            s = i*CHAR_BREAK
            lines.append(content[s:s+CHAR_BREAK])
            
        if r!=0:
            lines.append(content[CHAR_BREAK*q:CHAR_BREAK*q+r])
            
    return lines
            

def choose_new(name:str, min:int, max:int, integer:bool)->int:
    clear()
    print("Please, enter the new value for "+name+" below")
    print("   > The value must be"+(" an integer " if integer else " ")+f"between {min} and {max}" )
    print("   > You can enter 'R' to reset")
    line()
    choice = input(">>> ")
    
    if choice.capitalize() == 'R':
        return 'R'
    
    try:
        if integer:choice = int(choice)
        else: choice = float(choice)
        
    except ValueError:
        return choose_new(name, min, max, integer)
    
    if not min<=choice<=max:
        return choose_new(name, min, max, integer)
    
    return choice
    



def gui_2():
    
    options = OPTIONS.copy()
    global CHAR_BREAK
    
    while True:
        
        
        clear()
        print(menu[1])
        line(2)
        
        print("Here are the default options, please select the one you want to modify")
        print("####################################")
        print(f"  [1] BIASES: {options['biases']}")
        print(f"  [2] STYLE: {options['styles'][0]}")
        print(f"  [3] CHAR_BREAK: {CHAR_BREAK}")
        print(f"  [4] See help")
        line(2)
        print("Type V and Enter to validate and exit.")
        line()
        choice=input('>>> ')
        
        if choice.capitalize() == "V":
            break
        
        
        try:
            choice = int(choice)
            
        except ValueError:
            #ask again :/
            continue
        
        if not 1<=choice<=4:
            #ask again (at least it was a parsable int)
            continue
        
        if choice == 1:
            choice = choose_new("BIASES", 0.1, 1.0, False)
            if choice == 'R':
                options["biases"] = OPTIONS["biases"]
                continue
            else:
                options["biases"] = choice
                
        if choice == 2:
            choice = choose_new("STYLES", 1, 9, True)
            if choice == 'R':
                options["styles"] = OPTIONS["styles"]
                continue
            else:
                options["styles"] = [choice]
                
        if choice == 3:
            choice = choose_new("CHAR_BREAK", 10, 1000, True)
            if choice == 'R':
                CHAR_BREAK = CHAR_BREAK_D
                continue
            else:
                CHAR_BREAK = choice
        
        if choice == 4:
            clear()
            line(2)
            print("Here are several informations about the settings:")
            line()
            print("#################################")
            for key, value in HELP.items():
                print(f"   >> {key.capitalize()}: {value}")
                
            line()
            input("Press enter to go back to the settings...")
            continue
        
    return gui_1(options)
            
            
            
            
  
    
def gui_1(option=OPTIONS)->tuple:
    clear()
    print(menu[1])
    line(2)
    
    print("[1] Enter the text directly")
    print("[2] Enter the path to a .txt file")
    choice=input('>>> ')
    
    try:
        choice = int(choice)
        
    except ValueError:
        #ask again :/
        return gui_1()
    
    if not 1<=choice<=2:
        #ask again (at least it was a parsable int)
        return gui_1()
    
    if choice == 1:
        line(2)
        lines = []
        text = input('>>> ')
        q = len(text) // CHAR_BREAK
        r = len(text) % CHAR_BREAK
        
        for i in range(q):
            s = i*CHAR_BREAK
            lines.append(text[s:s+CHAR_BREAK])
            
        if r!=0:
            lines.append(text[CHAR_BREAK*q:CHAR_BREAK*q+r])
        
    
    
    if choice == 2:
        while True:
            clear()
            print("Please, enter the file path below: ")
            line()
            fpath = input(">>> ")
            
            try:
                print("Reading file...")
                lines = parse_txt(fpath)
                
            except Exception as e:
                line(2)
                print("ERROR: an exception occurred during file reading, please make sure the file exist and is readable.\n", e)
                input("Press enter to retry")
                continue
            else:break
    clear()
    print("Preview: ")
    print("Here is the formatted text: ")
    line(2)
    [print(t) for t in lines]
    
    line(2)
    if input("Press enter to confirm, or enter R to restart >>> ").capitalize() == "R":
        return gui_1()
    return lines, option
    
    
        
    
    




#### Main while

while True:
    clear()
    print(menu[0])
    line(2)
    
    print(">>> What do you wanna do ?")
    print("   [1] Generate simple text using default setting (type 'default' to see)")
    print("   [2] Configure custom setting and generate text")
    print("   [3] Exit")
    print("\nNote: both option 1/2 support import from a .txt file")

    choice=input("[1-3]: ")
    
    if choice == "default":
        clear()
        print("Here are the default options: ")
        for key, value in OPTIONS.items():
            print(f">> {key.capitalize()}: {value}")
        
        line(2)
        input("Press enter to continue")
        continue
    
    
    try:
        choice = int(choice)
        
    except ValueError:
        #ask again :/
        continue
    

            
    if not 1<=choice<=3:
        #ask again (at least it was a parsable int)
        continue
    
    if choice == 1:
        lines, option = gui_1()
        
    else:
        lines, option = gui_2()
    
    
    clear()
    print("Please, choose a name for your file")
    fname = input(">>> ")
    
    #generate the file
    generate_svg(lines, fname, option)
    
    
    #Open the image with os default image viewer
    if platform.system() == "Windows":
        os.startfile(f"./img/{fname}.svg")
    else:  # Linux
        subprocess.run(["xdg-open", f"./img/{fname}.svg"])
    
    
    
    
    try:
        open_svg.svg_to_drw(f"./img/{fname}.svg", fname)
    except Exception as e:
        print("ERROR: an exception occurred during file parsing, please make sure the file exist and is readable.\n", e)
        input("Press enter to retry")
        continue
    else:
        input("Press enter to go back to main menu")
    
    
