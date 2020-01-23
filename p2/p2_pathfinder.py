# Collaborated with Ishmael Chavesfrom heapq import heappop, heappushimport mathdef find_path(source_point, destination_point, mesh):    """    Searches for a path from source_point to destination_point through the mesh    Args:        source_point: starting point of the pathfinder        destination_point: the ultimate goal the pathfinder must reach        mesh: pathway constraints the path adheres to    Returns:        A path (list of points) from source_point to destination_point if exists        A list of boxes explored by the algorithm    """    path = []    boxes = {}    detailPoints = {}    srcBox = 0    destBox = 0    print(source_point)    print(destination_point)    for box in mesh["boxes"]:        if box[0] < source_point[0] < box[1] and box[2] < source_point[1] < box[3]:            srcBox = box            boxes[srcBox] = 0            # print("ding!")        if box[0] < destination_point[0] < box[1] and box[2] < destination_point[1] < box[3]:            destBox = box            # print("dong")        if srcBox != 0 and destBox != 0:            break    if srcBox == 0 or destBox == 0:        print("can't find box around endpoint", srcBox, destBox)        return path, boxes.keys()    # BFS    queue = [srcBox]    found = False    while queue:        currentBox = heappop(queue)        for adj in mesh["adj"][currentBox]:            if adj == destBox:                # print("found you")                found = True                boxes[adj] = currentBox                break            if adj not in boxes:                heappush(queue, adj)                boxes[adj] = currentBox        if found:            break    if not found:        print("No path found")    # Path making    temp = destBox  # (x1.x2.y1.y2)    trail = boxes[temp]    # calculating the x range    xLeft = {temp[0], trail[0]}    xRight = {temp[1], trail[1]}    xRange = (max(xLeft), min(xRight))    # calculating the y range    yLeft = {temp[2], trail[2]}    yRight = {temp[3], trail[3]}    yRange = (max(yLeft), min(yRight))    endPoint = [0, 0]    bestEndPoint = [0, 0]    bestLength = math.inf    for x in xRange:        endPoint[0] = x        for y in yRange:            endPoint[1] = y            length = math.pow((destination_point[0] - endPoint[0]), 2) + math.pow((destination_point[1] - endPoint[1]), 2)            if length < math.pow(bestLength, 2):                bestEndPoint = endPoint                bestLength = math.sqrt(length)    path.append((destination_point, (bestEndPoint[0], bestEndPoint[1])))    lastEndPoint = bestEndPoint    while trail != 0:        endPoint = [0, 0]        # calculating the x range        xLeft = {temp[0], trail[0]}        xRight = {temp[1], trail[1]}        xRange = (max(xLeft), min(xRight))        # calculating the y range        yLeft = {temp[2], trail[2]}        yRight = {temp[3], trail[3]}        yRange = (max(yLeft), min(yRight))        bestLength = math.inf        for x in xRange:            endPoint[0] = x            for y in yRange:                endPoint[1] = y                length = math.pow((lastEndPoint[0] - endPoint[0]), 2) + math.pow((lastEndPoint[1] - endPoint[1]), 2)                if length < math.pow(bestLength, 2):                    bestEndPoint = endPoint                    bestLength = math.sqrt(length)        path.append(((lastEndPoint[0], lastEndPoint[1]), (bestEndPoint[0], bestEndPoint[1])))        lastEndPoint = bestEndPoint        temp = trail        trail = boxes[temp]    path.append(((bestEndPoint[0], bestEndPoint[1]), source_point))    path.reverse()    print(path)    return path, boxes.keys()