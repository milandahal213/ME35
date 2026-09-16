import cv2
import numpy as np

cam = cv2.VideoCapture(0)
# initiate the MQTT

# Check if camera opened successfully
if not cam.isOpened():
    print("Error: Could not open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cam.read()
    
    if not ret:
        print("Error: Failed to capture frame")
        break
    
    # Split into BGR channels
    b, g, r = cv2.split(frame)
    #print("frame", frame) # contains RGB values
    #print("blue", b) # only print blue values
    
    #cv2.imshow("Only red", r)


    red_filtered = cv2.subtract(r, b)
    red_filtered = cv2.subtract(red_filtered, g)
    

    #cv2.imshow("Red filtered", red_filtered)
    # Threshold to create binary mask
    _, red_mask = cv2.threshold(red_filtered, 50, 255, cv2.THRESH_BINARY)
    
    #cv2.imshow("Red mask", red_mask)
    cv2.imshow(" red", red_mask)
    kernel = np.array([[1/16, 2/16, 1/16],[2/16,4/16,2/16],[1/16,2/16,1/16]])
    red_mask = cv2.filter2D(red_mask, -1, kernel)

    cv2.imshow("Only red", red_mask)

    # Press 'q' to quit and save
    if cv2.waitKey(1) & 0xFF == ord('q'):
        #cv2.imwrite('/Users/mdahal01/Downloads/test_original.jpg', frame)
        break


# Release everything when done
cam.release()
cv2.destroyAllWindows()

