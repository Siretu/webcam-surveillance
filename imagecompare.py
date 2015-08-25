import Image
import sys


def compare(name1, name2):
    img = Image.open(name1).convert("LA")
    img2 = Image.open(name2).convert("LA")
    
    width,height = img.size
    
    pixels = list(img.getdata())
    pixels2 = list(img2.getdata())

    pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]
    pixels2 = [pixels2[i * width:(i + 1) * width] for i in xrange(height)]
    
    result = []
    sums = [0,0]
    for i,x in enumerate(pixels):
        for j,y in enumerate(x):
            sums[0] += y[0]
            sums[1] += pixels2[i][j][0]
            result.append(abs(y[0]-pixels2[i][j][0]))
            
    avg = sum(result) / (width*height)
    avgdiff = [x - avg for x in result if x >= avg]
            
    result2 = sum(avgdiff) / (width*height)
    return max(avgdiff),result2,avg,sums



if __name__ == "__main__":
    maxdiff, avgdiff, avg, sums  = compare(sys.argv[1],sys.argv[2])
    print maxdiff
    print avgdiff
    print avg
    print sums
    print sums[1] - sums[0]

