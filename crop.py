# 根据中心线进行裁剪
def crop_face_central_line(img, bboxes):
    """
    对人脸框进行裁剪，以中心线为中心进行裁剪
    :param img: 原图的numpy数据
    :param bboxes: 人脸框的坐标
    :return: 左右图片的信息(face_image_left, face_image_left_coord, size_left_image)
    """

    # 判断左右框
    # 如果列表中的第一个元素为左框
    if bboxes[0][0] < bboxes[1][0]:
        x1 = bboxes[0][2]
        x2 = bboxes[1][0]
        # 计算两个框的之间的中心线
        center_line_x = int((x1+x2)/2)
    else:
        x1 = bboxes[1][2]
        x2 = bboxes[0][0]
        # 计算两个框的之间的中心线
        center_line_x = int((x1+x2)/2)


    face_image_left = img[:, :center_line_x]
    # 左上角坐标
    face_image_left_coord = (0,0)

    face_image_right = img[:, center_line_x:]
    # 左上角坐标
    face_image_right_coord = (center_line_x, 0)
    
    size_left_image = (img.shape[0], center_line_x)
    size_right_image = (img.shape[0], img.shape[1]-center_line_x)

    face_image_left_info = (face_image_left, face_image_left_coord, size_left_image)
    face_image_right_info = (face_image_right, face_image_right_coord, size_right_image)

    return (face_image_left_info, face_image_right_info)