# install

ให้ใช้ Python version 3.7 ขึ้นไป

install library ต่าง ๆ จาก `requirements.txt` ด้วย pip

```bash
pip install -r requirements.txt
```

# run

```bash
python main.py
```

# ไฟล์ตั้งค่า

**กำหนดรูปแบบด่าน:** [`stage_layout.py`](stage_layout.py)

**ตัวแปรอื่น ๆ:** [`main.py`](main.py)

# logic การคำนวณ

**game loop:** [`pygame_fps/pygame/pygame.py`](pygame_fps/pygame/pygame.py)

**การเคลื่อนไหวของผู้เล่น:** [`pygame_fps/player/main.py`](pygame_fps/player/main.py)

**การคำนวณการตกกระทบของแสงกับกำแพง:** [`pygame_fps/vision/ray.py`](pygame_fps/vision/ray.py)

**การวาดกำแพงในมุมมอง first-person view:** [`pygame_fps/first_person_view/panel.py`](pygame_fps/first_person_view/panel.py)

