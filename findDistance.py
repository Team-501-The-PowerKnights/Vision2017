
import math

def findDistance(image, Rect_coor, w, horizontal_cameraFOV):  ############## NEED TO UPDATE VARIABLES #############
    pegHeight = 13.25 / 12.0  # ft
    targetWidth = 2  # inches
    cameraHeight = 1.5  # ft
    robot2camera = 1.5  # distance from front of robot to camera (ft)

    def distance(targetActual, imagePx, targetPx, cameraFOV):
        totalDistance = (((targetActual * imagePx) / targetPx) / 2.0) / \
                        math.tan(((cameraFOV * math.pi) / 180.0) / 2.0)
        totalDistance = int((totalDistance * 100.0) / 12.0) / 100.0  # make into 2 decminal pt and ft
        return totalDistance

    def fixDistance(x):  # use polynomial fit to adjust for error
        pass

    def targetPixelWidth():
        # In Rect coor indexing first number is countour, second is corner, third is whether it's x or y
        w1 = math.fabs(Rect_coor[0][1][0] - Rect_coor[0][0][0])
        w2 = math.fabs(Rect_coor[0][2][0] - Rect_coor[0][3][0])
        w3 = math.fabs(Rect_coor[1][1][0] - Rect_coor[1][0][0])
        w4 = math.fabs(Rect_coor[1][2][0] - Rect_coor[1][3][0])
        width = (w1 + w2 + w3 + w4) / 4.0  # avg the widthes of the two targets
        return width

    totalDistance_W = distance(targetWidth, w, targetPixelWidth(),
                               horizontal_cameraFOV)  # diagonal distance from camera to tower (ft)

    try:
        distance_horizontal = math.sqrt(totalDistance_W ** 2.0 - (
                pegHeight - cameraHeight) ** 2.0) - robot2camera  # distance from front of robot to tower
        distance_final = int(fixDistance(distance_horizontal * 12) * 100.0) / 100.0  # in
    except:
        distance_final = totalDistance_W * 12.0  # in

    return distance_final