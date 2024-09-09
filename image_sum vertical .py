from tkinter import Tk, Label, Button, Entry, filedialog
from PIL import Image, ImageDraw, ImageFont
import os

# 폰트 경로 설정
NOTO_SANS_KR_PATH = "C:/Users/Admin/OneDrive/바탕 화면/Coding/viewbot/Noto_Sans_KR/NotoSansKR-Regular.otf"
ROBOTO_PATH = "C:/Users/Admin/OneDrive/바탕 화면/Coding/viewbot/Noto_Sans_KR/Roboto-Regular.ttf"

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

    # 이미지 세로로 합치기
    total_height = sum(img.height for img in images)
    combined_image = Image.new('RGB', (780, total_height), (255, 255, 255))  # 새로운 빈 이미지 생성

    y_offset = 0
    for img in images:
        combined_image.paste(img, (0, y_offset))  # 이미지를 세로로 붙이기
        y_offset += img.height

    # 상단과 하단에 텍스트 추가
    draw = ImageDraw.Draw(combined_image)

    # 폰트 설정
    font = ImageFont.truetype(NOTO_SANS_KR_PATH, 25)

    # 상단 텍스트 추가 (중앙 정렬)
    if top_text:
        bbox = draw.textbbox((0, 0), top_text, font=font)
        text_width = bbox[2] - bbox[0]
        top_text_x = (combined_image.width - text_width) // 2
        draw.text((top_text_x, 10), top_text, font=font, fill=(0, 0, 0))

    # 하단 텍스트 추가 (중앙 정렬)
    if bottom_text:
        bbox = draw.textbbox((0, 0), bottom_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        bottom_text_x = (combined_image.width - text_width) // 2
        draw.text((bottom_text_x, total_height - text_height - 10), bottom_text, font=font, fill=(0, 0, 0))

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
