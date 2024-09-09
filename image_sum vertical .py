from tkinter import Tk, Label, Button, Entry, filedialog
from PIL import Image, ImageDraw, ImageFont
import os

# 폰트 경로 설정
NOTO_SANS_KR_PATH = r"NotoSansKR-Bold.ttf"
ROBOTO_PATH = r"Roboto-Bold.ttf"

def process_images(folder_path, top_text, bottom_text):
    # 이미지 파일을 불러오기
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    
    if not image_files:
        print("이미지 파일이 없습니다.")
        return

    images = []
    for image_file in image_files:
        img = Image.open(os.path.join(folder_path, image_file))
        img = img.resize((780, 780))  # 이미지 크기를 780x780으로 변환
        images.append(img)

    # 폰트 크기 100 (4배)
    font_size = 100
    font = ImageFont.truetype(NOTO_SANS_KR_PATH, font_size)

    # 텍스트 높이 계산
    dummy_img = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    
    # 상단 텍스트 높이 계산
    top_text_height = 0
    if top_text:
        bbox = draw.textbbox((0, 0), top_text, font=font)
        top_text_height = bbox[3] - bbox[1]

    # 하단 텍스트 높이 계산
    bottom_text_height = 0
    if bottom_text:
        bbox = draw.textbbox((0, 0), bottom_text, font=font)
        bottom_text_height = bbox[3] - bbox[1]

    # 텍스트 영역을 고려한 이미지 높이 계산
    total_image_height = sum(img.height for img in images)
    total_height = total_image_height + top_text_height + bottom_text_height + 100  # 여백을 위한 추가 공간

    # 이미지 세로로 합치기
    combined_image = Image.new('RGB', (780, total_height), (255, 255, 255))  # 새로운 빈 이미지 생성

    # 상단 텍스트 추가
    draw = ImageDraw.Draw(combined_image)
    y_offset = 0

    if top_text:
        bbox = draw.textbbox((0, 0), top_text, font=font)
        text_width = bbox[2] - bbox[0]
        top_text_x = (combined_image.width - text_width) // 2
        draw.text((top_text_x, y_offset + 10), top_text, font=font, fill=(0, 0, 0))
        y_offset += top_text_height + 50  # 여백 추가

    # 이미지들 추가
    for img in images:
        combined_image.paste(img, (0, y_offset))  # 이미지를 세로로 붙이기
        y_offset += img.height

    # 하단 텍스트 추가
    if bottom_text:
        bbox = draw.textbbox((0, 0), bottom_text, font=font)
        text_width = bbox[2] - bbox[0]
        bottom_text_x = (combined_image.width - text_width) // 2
        draw.text((bottom_text_x, y_offset + 10), bottom_text, font=font, fill=(0, 0, 0))

    # 결과 이미지 저장
    combined_image.save(os.path.join(folder_path, "combined_image_with_text.jpg"))
    print("이미지가 성공적으로 저장되었습니다!")

# 폴더 선택 및 이미지 처리 함수
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        top_text = top_text_entry.get()
        bottom_text = bottom_text_entry.get()
        process_images(folder_path, top_text, bottom_text)

# Tkinter GUI 설정
root = Tk()
root.title("이미지 합치기 및 텍스트 추가")

# 상단 라벨과 입력창
Label(root, text="상단에 넣을 텍스트:").pack()
top_text_entry = Entry(root)
top_text_entry.pack()

# 하단 라벨과 입력창
Label(root, text="하단에 넣을 텍스트:").pack()
bottom_text_entry = Entry(root)
bottom_text_entry.pack()

# 폴더 선택 버튼
Button(root, text="폴더 선택 및 이미지 처리", command=select_folder).pack()

# Tkinter 메인 루프 실행
root.mainloop()
