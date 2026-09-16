import cv2
import numpy as np

frame = cv2.imread("/Users/mdahal01/Downloads/IMG_4916.jpeg",1)
cv2.imshow("Image", frame)

# Print the array in the image 
# Notice how they are array of BGR array 

#Uncomment below
#print(frame)


#Split the image into color frames

b,g,r = cv2.split(frame)

#Uncomment below
#cv2.imshow("Red Frame", r)

#Uncomment below
#cv2.imshow("Blue Frame", b)

#Uncomment below
#cv2.imshow("Gren Frame", g)

# Extracting blue color 

new_blue = cv2.subtract(b,r)
new_blue = cv2.subtract(new_blue, g)


#Uncomment below
#cv2.imshow("only Blue", new_blue)

#After thresholding
_, blue_mask = cv2.threshold(new_blue, 20, 255, cv2.THRESH_BINARY)


#Uncomment below
#cv2.imshow("mask Blue", blue_mask)


kernel = np.ones((5, 5), np.uint8)
blue_after_open = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
#Uncomment below
#cv2.imshow("Blue mask open", blue_after_open)


blue_after_close = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernel)
#Uncomment below
#cv2.imshow("Blue mask close", blue_after_close)


blue_open_and_close = cv2.morphologyEx(blue_after_open, cv2.MORPH_CLOSE, kernel)
#Uncomment below
#cv2.imshow("Blue open and close", blue_open_and_close)

blue_close_and_open = cv2.morphologyEx(blue_after_close, cv2.MORPH_CLOSE, kernel)
#Uncomment below
#cv2.imshow("Blue close and open", blue_close_and_open)


#Try various kernels and see what results you get
kernel = np.array([[-2, -1 , 0 ],[-1,1,1],[0,1,2]])
new_frame = cv2.filter2D(blue_open_and_close, -1, kernel)
cv2.imshow("New image", new_frame)




cv2.waitKey(0)
cv2.destroyAllWindows()