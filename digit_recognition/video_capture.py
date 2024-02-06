import cv2


def process_video(input_video_path, output_video_path):
    # Open the video file
    video_capture = cv2.VideoCapture(input_video_path)

    # Get the video properties
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create a VideoWriter object to save the processed video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Specify the video codec
    output_video = cv2.VideoWriter(
        output_video_path, fourcc, fps, (frame_width, frame_height), isColor=False
    )

    # Process each frame in the video
    while video_capture.isOpened():
        ret, frame = video_capture.read()

        if not ret:
            break

        # Flip the frame horizontally
        flipped_frame = cv2.flip(frame, 1)

        # Apply edge detection
        gray_frame = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY)
        edges_frame = cv2.Canny(gray_frame, 100, 200)

        # Display the output frame
        cv2.imshow("Processed Video", edges_frame)

        # Write the processed frame to the output video file
        output_video.write(edges_frame)

        # Exit if the 'q' key is pressed
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

    # Release the video capture and output video objects
    video_capture.release()
    output_video.release()

    # Close all windows
    cv2.destroyAllWindows()


# Example usage
input_video_path = "input.mp4"
output_video_path = "output.mp4"

process_video(input_video_path, output_video_path)
