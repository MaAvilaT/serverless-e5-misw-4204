import logging

import cv2


logging.basicConfig(level=logging.INFO)


def process_video(file_path, image_path):
    edited_video_name = file_path.split('/')[-1] + '-output.mp4'
    new_video_path = file_path + '-output.mp4'

    logging.info(f'Processing video {file_path}')
    logging.info(f'Processing video {new_video_path}')

    change_aspect_ratio(file_path, new_video_path, image_path)

    logging.info(f'Success')

    return {
        'original_file_path': file_path,
        'status': 'processed',
        'new_file_path': new_video_path,
        'new_file_name': new_video_path.split('/')[-1],
        'edited_video_name': edited_video_name,
        'original_file_name': file_path.split('/')[-1],
    }


def change_aspect_ratio(video_path, output_path, image_path, num_frames: int = 30):
    # Read the video file
    cap = cv2.VideoCapture(video_path)

    # Get the video's width and height
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Calculate the new width and height for a 16:9 aspect ratio
    new_width = int(height * 16 / 9)
    new_height = height

    # Get the original frame rate
    frame_rate = cap.get(cv2.CAP_PROP_FPS)

    # Create a video writer object with the original frame rate
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, frame_rate, (new_width, new_height))

    logging.info(f'create video writer object')

    # Read start image
    start_image = cv2.imread(image_path)
    start_image = cv2.resize(start_image, (new_width, new_height))

    logging.info(f'read start image')

    # Read end image
    end_image = cv2.imread(image_path)
    end_image = cv2.resize(end_image, (new_width, new_height))

    logging.info(f'read end image')

    # Write start frames
    for _ in range(num_frames):
        out.write(start_image)

    logging.info(f'write start frames')

    # Loop over the frames in the video
    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # If the frame is empty, break out of the loop
        if not ret:
            break

        # Resize the frame to the new aspect ratio
        resized_frame = cv2.resize(frame, (new_width, new_height))

        # Write the resized frame to the output video
        out.write(resized_frame)

    logging.info(f'loop over the frames in the video')

    # Write end frames
    for _ in range(num_frames):
        out.write(end_image)

    logging.info(f'write end frames')

    # Release the video capture and writer objects
    cap.release()
    out.release()
