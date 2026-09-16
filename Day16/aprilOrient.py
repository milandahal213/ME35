import cv2
import numpy as np

# Initialize the AprilTag detector
detector = cv2.aruco.ArucoDetector(
    cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11),
    cv2.aruco.DetectorParameters()
)

# Option 1: Detect from webcam
def detect_from_webcam():
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect AprilTags
        corners, ids, rejected = detector.detectMarkers(gray)
        
        # Draw detected tags
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            
            # Print tag information
            for i, tag_id in enumerate(ids):
                # Get corner coordinates
                corner = corners[i][0]
                
                # Calculate center
                center_x = int(np.mean(corner[:, 0]))
                center_y = int(np.mean(corner[:, 1]))
                
                # Display ID and center on frame
                cv2.putText(frame, f"ID: {tag_id[0]}", 
                           (center_x - 20, center_y - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                print(f"Tag ID: {tag_id[0]}, Center: ({center_x}, {center_y})")
        
        # Display the frame
        cv2.imshow('AprilTag Detection', frame)
        
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Option 2: Detect from image file
def detect_from_image(image_path):
    # Read the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect AprilTags
    corners, ids, rejected = detector.detectMarkers(gray)
    
    # Draw detected tags
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(image, corners, ids)
        
        print(f"Found {len(ids)} AprilTag(s)")
        
        for i, tag_id in enumerate(ids):
            corner = corners[i][0]
            center_x = int(np.mean(corner[:, 0]))
            center_y = int(np.mean(corner[:, 1]))
            
            print(f"Tag ID: {tag_id[0]}")
            print(f"  Center: ({center_x}, {center_y})")
            print(f"  Corners: {corner}")
    else:
        print("No AprilTags detected")
    
    # Display result
    cv2.imshow('AprilTag Detection', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return corners, ids

# Option 3: Get orientation using corner analysis (no calibration needed)
def detect_with_orientation():
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = detector.detectMarkers(gray)
        
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            
            for i, tag_id in enumerate(ids):
                corner = corners[i][0]
                
                # Calculate orientation from corners
                # Corner 0 is top-left, goes clockwise
                top_left = corner[0]
                top_right = corner[1]
                
                # Calculate angle using top edge
                dx = top_right[0] - top_left[0]
                dy = top_right[1] - top_left[1]
                angle_rad = np.arctan2(dy, dx)
                angle_deg = np.degrees(angle_rad)
                
                # Calculate center
                center_x = int(np.mean(corner[:, 0]))
                center_y = int(np.mean(corner[:, 1]))
                
                # Draw orientation arrow
                arrow_length = 50
                end_x = int(center_x + arrow_length * np.cos(angle_rad))
                end_y = int(center_y + arrow_length * np.sin(angle_rad))
                cv2.arrowedLine(frame, (center_x, center_y), (end_x, end_y), 
                               (0, 255, 0), 3, tipLength=0.3)
                
                # Display info
                text = f"ID:{tag_id[0]} Angle:{angle_deg:.1f}"
                cv2.putText(frame, text, (center_x - 60, center_y - 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                print(f"Tag ID: {tag_id[0]}, Orientation: {angle_deg:.2f} degrees")
        
        cv2.imshow('AprilTag with Orientation', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Option 4: Full 3D pose estimation (requires camera calibration)
def detect_with_full_pose(camera_matrix, dist_coeffs, tag_size):
    """
    camera_matrix: 3x3 camera intrinsic matrix
    dist_coeffs: distortion coefficients
    tag_size: real-world size of the tag in meters (or any unit)
    """
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = detector.detectMarkers(gray)
        
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            
            for i in range(len(ids)):
                # Estimate pose
                rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
                    corners[i], tag_size, camera_matrix, dist_coeffs
                )
                
                # Draw 3D axis
                cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, 
                                 rvec, tvec, tag_size * 0.5)
                
                # Convert rotation vector to rotation matrix
                rotation_matrix, _ = cv2.Rodrigues(rvec)
                
                # Extract Euler angles (roll, pitch, yaw)
                sy = np.sqrt(rotation_matrix[0, 0]**2 + rotation_matrix[1, 0]**2)
                
                if sy > 1e-6:
                    roll = np.arctan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
                    pitch = np.arctan2(-rotation_matrix[2, 0], sy)
                    yaw = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
                else:
                    roll = np.arctan2(-rotation_matrix[1, 2], rotation_matrix[1, 1])
                    pitch = np.arctan2(-rotation_matrix[2, 0], sy)
                    yaw = 0
                
                # Convert to degrees
                roll_deg = np.degrees(roll)
                pitch_deg = np.degrees(pitch)
                yaw_deg = np.degrees(yaw)
                
                # Calculate distance
                distance = np.linalg.norm(tvec)
                
                # Display info
                info_text = f"ID:{ids[i][0]} D:{distance:.2f}m"
                cv2.putText(frame, info_text, (10, 30 + i*80),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.putText(frame, f"Roll:{roll_deg:.1f}", (10, 50 + i*80),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                cv2.putText(frame, f"Pitch:{pitch_deg:.1f}", (10, 70 + i*80),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                cv2.putText(frame, f"Yaw:{yaw_deg:.1f}", (10, 90 + i*80),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                
                print(f"Tag {ids[i][0]}: Distance={distance:.2f}, "
                      f"Roll={roll_deg:.1f}°, Pitch={pitch_deg:.1f}°, Yaw={yaw_deg:.1f}°")
        
        cv2.imshow('AprilTag with Full Pose', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Run the detector
if __name__ == "__main__":
    # Choose one:
    
    # For basic webcam detection:
    # detect_from_webcam()
    
    # For image file detection:
    # detect_from_image('path/to/your/image.jpg')
    
    # For 2D orientation (no calibration needed):
    detect_with_orientation()
    
    # For full 3D pose with roll/pitch/yaw (requires calibrated camera):
    # camera_matrix = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]], dtype=float)
    # dist_coeffs = np.zeros((5,1))
    # tag_size = 0.05  # 5cm tags
    # detect_with_full_pose(camera_matrix, dist_coeffs, tag_size)