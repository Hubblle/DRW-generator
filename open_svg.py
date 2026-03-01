"""
This module is used to convert vectorial images (.svg format) containing a single path element into a .drw file;
see https://github.com/Hubblle/Drawing_lib for more informations
"""


import json
import xml.etree.ElementTree as ET
import os


def parse_svg(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # SVG namespace
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    
    # Find all path elements
    paths = root.findall('.//svg:path', ns)
    
    path_data = []
    for path in paths:
        d = path.get('d')
        if d:
            path_data.append(d)
    
    return path_data


def transform_svg_to_list(f:str)->list:
    rtrn = f.split("M")
    rtrn = rtrn[2:]
    return rtrn


def batch_float_convert(tab)->list:
    for i in range(len(tab)):
        try:
            tab[i] = float(tab[i])
        except ValueError:
            print("WARNING: non int value to convert ! ", tab[i])
            tab[i] = tab[i-1] if i !=0 else 0
    return tab


def svg_to_drw(path:str, fname:str="output", zoom=30, STARTING=(200,200)):
    """This function takes a .svg file with one main path element and convert it into the .drw format (as a processed format)

    Args:
        path (str): The path of the .drw file
        fname (str, optional): The file name (saved in ./generation). Defaults to "output".
        zoom (int, optional): The zoom. Defaults to 30.
        STARTING (tuple, optional): The starting coordinates of the drw. Defaults to (200,200).
    """
    svg : str = parse_svg('img/test.svg')[0]
    brute_path = transform_svg_to_list(svg)


    path = {"type":"processed","max-y": 0,"max-x": 0, "list":[] }
    max_y = 0
    max_x = 0

    min_x = 10e10
    min_y = 10e10

    brute_coordinate = []

    #Get the coordinates
    for path1 in brute_path:
        if not path1 == '':
            coordinates=[]
            
            paths : list = path1.split("L")
            

            for coordinate in paths:
                coordinates.append(batch_float_convert(coordinate[:-1].split(",")))
                

            
            #get the max and min
            for coo in coordinates:
                    
                if coo[0] < min_x:
                    min_x = coo[0]

                    
                if coo[1] < min_y:
                    min_y = coo[1]
            
        
            brute_coordinate.append(coordinates)
            
    print(min_x, min_y)
        

    #process the diff between the starting coordinates and the min

    for coo_list in brute_coordinate:
        
        for coo in coo_list:
            #apply the zoom and the correction
            
            
            
            coo[0]*= zoom
            coo[1]*= zoom
            
            coo[0] -= min_x*zoom
            coo[1] -= min_y*zoom

            
            coo[1] = int(round(coo[1]))
            coo[0] = int(round(coo[0]))
            
            if coo[0] > max_x:
                max_x = coo[0]

                    
            if coo[1] > max_y:
                max_y = coo[1]
                

                    
    #use the bresenham algorithm to get all the moves of the x and y axis

    for coordinate in brute_coordinate:
        mov_list = []
        
        start = coordinate[0]
        coordinate.pop(0)
        
        
        last_co = start
        for coo in coordinate:
            coordinate_by_step = []
            
            x0, y0 = last_co
            x1, y1 = coo

            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            sx = 1 if x1 >= x0 else -1
            sy = 1 if y1 >= y0 else -1

            if dx > dy:
                err = dx // 2
                while x0 != x1:
                    coordinate_by_step.append([x0, y0])
                    #print([x0, y0])
                    err -= dy
                    if err < 0:
                        y0 += sy
                        err += dx
                    x0 += sx
            else:
                err = dy // 2
                while y0 != y1:
                    coordinate_by_step.append([x0, y0])
                    #print([x0, y0])
                    err -= dx
                    if err < 0:
                        x0 += sx
                        err += dy
                    y0 += sy
            coordinate_by_step.append([x1, y1])
                    
            mov_list += coordinate_by_step
            last_co = coo

        path["list"].append({
            "start": start,
            "movement":mov_list
            })

    path["max-x"] = max_x
    path["max-y"] = max_y

    print("Processing the movement based on the value")
    i= -1

    for value in path["list"]:
        i=i+1
        mov_by_step = []
        total_x=0
        total_y=0
            
        last_co = [value["start"][0], value["start"][1]]
        
        for coordinate in value["movement"] :
            mov = [coordinate[0]-last_co[0], coordinate[1]-last_co[1]]
            #print(mov)
            mov_by_step.append(mov)
            
            total_x=total_x+mov[0]
            total_y=total_y+mov[1]
            
            last_co = coordinate
        
        path["list"][i]["movement"]=mov_by_step
        path["list"][i]["coordinates"]=(total_x,total_y)


    fpath = f"./generation/{fname}.drw"
    n=0
    while os.path.exists(fpath):
        n+=1
        fpath = f"./generation/{fname}_{n}.drw"

    with open(fpath, "x", encoding="utf-8") as file:
        path = json.dumps(path, ensure_ascii=False, indent=2)
        file.write(path)
        file.close()

    print("INFO: File saved successfully as "+ fpath)

