from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip,  concatenate_videoclips
import uuid


def process(image_path, video_path, video_size:tuple, desired_video_center_on_image:tuple):
    """
    将视频放在图片的指定位置上面
    :param video_path: 视频路径
    :param image_path: 图片路径
    """

    # 读取视频
    video_clip = VideoFileClip(video_path)

    # 重新调整视频的尺寸
    new_video_width, new_video_height = video_size
    video_clip = video_clip.resize((new_video_width, new_video_height))

    # 读取图片
    image_clip = ImageClip(image_path).set_duration(video_clip.duration)

    # 设置视频在图片上的位置
    desired_video_center_x, desired_video_center_y = desired_video_center_on_image

    # 计算视频左上角在图片上的位置
    video_position_x = desired_video_center_x - new_video_width / 2
    video_position_y = desired_video_center_y - new_video_height / 2
    # 设置视频在图片上的位置
    video_position = (video_position_x, video_position_y)

    # 合成视频
    final_clip = CompositeVideoClip([image_clip, video_clip.set_position(video_position)])

    # 保存合成后的视频
    video_path = f"./temp/composite_video{str(uuid.uuid4())}.mp4"
    final_clip.write_videofile(video_path, fps=video_clip.fps)


def concatenate_videos(video_files, output_file_path):
    # 读取所有视频片段
    video_clips = [VideoFileClip(file) for file in video_files]

    # 拼接视频片段
    final_clip = concatenate_videoclips(video_clips)

    # 保存为新视频文件
    final_clip.write_videofile(output_file_path)

    # 关闭所有视频片段
    final_clip.close()
    for clip in video_clips:
        clip.close()

    return output_file_path


def process_v2(image_path, video_path, video_size:tuple, desired_video_coord_on_image:tuple):
    """
    将视频放在图片的指定位置上面
    :param video_path: 视频路径
    :param image_path: 图片路径
    """

    # 读取视频
    video_clip = VideoFileClip(video_path)


    # 重新调整视频的尺寸
    new_video_height, new_video_width = video_size
    video_clip = video_clip.resize((new_video_width, new_video_height))

    # 裁剪视频
    crop_area = (0, 0, int(new_video_width*0.98), new_video_height)
    cropped_clip = video_clip.crop(x1=crop_area[0], y1=crop_area[1], width=crop_area[2], height=crop_area[3])


    # 读取图片
    image_clip = ImageClip(image_path).set_duration(cropped_clip.duration)

    # 设置视频在图片上的位置
    video_position_x, video_position_y = desired_video_coord_on_image
    video_position = (video_position_x, video_position_y)

    # 合成视频
    final_clip = CompositeVideoClip([image_clip, cropped_clip.set_position(video_position)])

    # 保存合成后的视频
    video_path = f"./temp/composite_video{str(uuid.uuid4())}.mp4"
    final_clip.write_videofile(video_path, fps=video_clip.fps)
    
    return video_path
