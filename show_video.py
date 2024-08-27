import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def show_video(filename, start_frame=0, end_frame=None, interval=50):
    """
    Show a video using Matplotlib.

    Parameters:
    - filename: str, path to the video file
    - start_frame: int, optional, index of the first frame to start with (default: 0)
    - end_frame: int, optional, index of the last frame to end with (default: None, meaning till end of video)
    - interval: int, optional, interval between frames in milliseconds (default: 50)
    """
    cap = cv2.VideoCapture(filename)

    if not cap.isOpened():
        raise ValueError("Failed to open video file. Please check the file path.")

    # Get total number of frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if end_frame is None or end_frame > total_frames:
        end_frame = total_frames - 1

    def update_frame(i):
        nonlocal start_frame
        nonlocal end_frame
        nonlocal cap
        if start_frame <= end_frame:
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            ret, frame = cap.read()
            if ret:
                im.set_array(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                start_frame += 1
        return im,

    fig, ax = plt.subplots()
    ret, frame = cap.read()
    im = ax.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    ax.axis('off')

    ani = FuncAnimation(fig, update_frame, frames=range(start_frame, end_frame + 1),
                        interval=interval, blit=True)

    plt.show()
    cap.release()


if __name__ == "__main__":
    # 示例用法
    show_video('input.mp4', start_frame=0, end_frame=200)
