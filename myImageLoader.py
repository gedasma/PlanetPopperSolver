import cv2
import numpy as np

imageMap = [(1, 'purple1.png'),
            (2, 'teal2.png'),
            (3, 'pink3.png'),
            (4, 'black4.png')]

def splitImage(image, size):
    height, width, _ = image.shape
    print(height, width)

    subImageHeight = height / size
    subImageWidth = width / size

    subImages = []

    for i in range(size):
        imageRow = []
        for j in range(size):

            rowStart = int(i * subImageHeight)
            rowEnd = int((i+1) * subImageHeight -5)

            colStart = int(j * subImageWidth)
            colEnd = int((j+1) * subImageWidth -5)

            subImage = image[rowStart:rowEnd, colStart:colEnd]
            
            imageRow.append(subImage)
        subImages.append(imageRow)

    return subImages

def find_dominant_color(image, k=1):
    # Read the image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB (OpenCV uses BGR by default)

    # Reshape the image to a list of pixels
    pixels = image.reshape((-1, 3))

    # Convert pixel values to float
    pixels = np.float32(pixels)

    # Define criteria and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert back to 8-bit values
    centers = np.uint8(centers)

    # Find the dominant color
    dominant_color = centers[0]

    return dominant_color.tolist()

def findMostSimilar(image, comparisonMap):
    comparisonArray = []
    mseArray = []
    for imageMapValue in imageMap:
        testImage = cv2.imread(imageMapValue[1])
        
        testHeight, testWidth, _ = testImage.shape
        scaled_image = cv2.resize(image, (testWidth, testHeight))

        gray1 = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(testImage, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(gray1, gray2, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        mseArray.append(max_val)
    
    return np.argmax(mseArray) + 1

def createSimilarityMap():
    comparisonMap = dict()
    for mapItem in imageMap:
        testImage = cv2.imread(mapItem[1])
        dominantColor = find_dominant_color(testImage)
        comparisonMap[mapItem[0]] = dominantColor
    return comparisonMap

def getSimilarColorIndex(image ,comparisonMap):
    imageColor = find_dominant_color(image)
    
    similarityMap = dict()

    for planetNumber, rgbValue in comparisonMap.items():
        comparedRGB = [x - y for x, y in zip(imageColor, comparisonMap[planetNumber])]
        absoluteSum = sum(abs(x) for x in comparedRGB)
        similarityMap[planetNumber] = absoluteSum

    return min(similarityMap, key=lambda k: similarityMap[k])


# inputMap = 'testMap2.png'
inputMap = 'Untitled.png'
mapImage = cv2.imread(inputMap)

# print( [157, 89, 120]  - [50,50,50])

imageMapArray = splitImage(mapImage, 9)
similarityMap = createSimilarityMap()

outputArray = [[0 for _ in range(len(imageMapArray[0]))] for _ in range(len(imageMapArray))]
# loopdepth = 0
for rowIndex in range(len(imageMapArray)):
    for colIndex in range(len(imageMapArray[rowIndex])):
        # cv2.imshow("test",imageMapArray[rowIndex][colIndex])
        # print(getSimilarColorIndex(imageMapArray[rowIndex][colIndex], similarityMap))
        # cv2.waitKey(0)
        outputArray[rowIndex][colIndex] = getSimilarColorIndex(imageMapArray[rowIndex][colIndex], similarityMap)


file_path = "matrix_from_image.txt"
with open(file_path, "w") as file:
    # Write each row of the matrix to the file
    for row in outputArray:
        file.write(", ".join(map(str, row)) + "\n")