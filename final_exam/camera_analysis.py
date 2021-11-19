def test_color(img,x, y):
    for i in range(y):
        for j in range(x):
            if img[i][j][1] >= 1.5*img[i][j][0] and img[i][j][1] >= 1.5*img[i][j][2] and img[i][j][1] > 100:
                print("green", i, j)
            elif img[i][j][0] >= 1.5*img[i][j][1] and img[i][j][0] >= 1.5 *img[i][j][2] and img[i][j][0] > 100:
                print("red", i,j)
            elif img[i][j][2] >= 1.5*img[i][j][0] and img[i][j][2] >= 1.5*img[i][j][1] and img[i][j][2] > 100:
                print("blue",i,j)
