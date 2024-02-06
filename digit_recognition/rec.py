import cv2
from process_frame import process_frame
import time


def process_video(input_video_path):
    frame_rate = 4
    prev = 0
    # Open the video file
    video_capture = cv2.VideoCapture(input_video_path)
    # Process each frame in the video
    fd = []
    while video_capture.isOpened():
        time_elapsed = time.time() - prev
        ret, frame = video_capture.read()

        if time_elapsed > 1.0 / frame_rate:
            prev = time.time()
            if not ret:
                break

            # Process frame by frame
            (
                output,
                digits,
            ) = process_frame(frame)
            fd.append(digits)

        # Exit if the 'q' key is pressed
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

    total = len(fd)
    correct = filter(lambda x: len(x) > 0, fd)
    correct = len(list(correct))

    print("Total digits: ", total)
    print("Recognized digits: ", correct)
    print(f"Accuracy:  {correct / total * 100:.2f}%")
    # Release the video capture and output video objects
    video_capture.release()

    # Close all windows
    cv2.destroyAllWindows()


# Example usage
input_video_path = "input.mp4"

process_video(input_video_path)
