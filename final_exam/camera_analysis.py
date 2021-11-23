import matplotlib.pyplot as plt

def test_color(img,x, y):
    for i in range(y):
        for j in range(x):
            img[i][j] = [0,0,0]
            if img[i][j][1] >= 1.5*img[i][j][0] and img[i][j][1] >= 1.5*img[i][j][2] and img[i][j][1] > 99:
                img[i][j] == [0,255,0]
            elif img[i][j][0] >= 2*img[i][j][1] and img[i][j][1] >= 2 * img[i][j][2]:
                img[i][j] = [255,130, 0]
            elif img[i][j][0] >= 1.5*img[i][j][1] and img[i][j][0] >= 1.5 *img[i][j][2] and img[i][j][0] > 99:
                img[i][j] = [255,0,0]
            elif img[i][j][2] >= 1.5*img[i][j][0] and img[i][j][2] >= 1.5*img[i][j][1] and img[i][j][2] > 99:
                img[i][j] = [0, 0,255]
            elif img[i][j][2] >= 1.5*img[i][j][1] and img[i][j][0] >= 1.5*img[i][j][1] and img[i][j][2] > 99:
                img[i][j] = [230,230,250]
            else:
                img[i][j] = [0,0,0]
    plt.imshow(img)
    plt.show()
