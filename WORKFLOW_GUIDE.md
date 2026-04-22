# 📘 Quy trình làm việc: Code thử → Copy ổn định → Đẩy lên GitHub

> Bạn code ở thư mục con, khi nào ổn định thì copy sang thư mục chính và đẩy lên GitHub bằng GitHub Desktop.

---

## 🎯 Tóm tắt quy trình

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Thư mục DEV    │ ──► │  Thư mục MAIN    │ ──► │     GitHub      │
│  (Code thử)     │     │  (Code chính thức)    │     │  (Deploy Cloud) │
└─────────────────┘     └──────────────────┘     └─────────────────┘

Bước 1: Code, test, sửa lỗi trong thư mục DEV
        ↓
Bước 2: Khi chạy ổn định → Copy file sang thư mục MAIN
        ↓
Bước 3: Mở GitHub Desktop → Thấy file thay đổi → Commit → Push
        ↓
Bước 4: Streamlit Cloud tự động cập nhật
```

---

## Bước 1: Chuẩn bị cấu trúc thư mục

Giả sử thư mục gốc của bạn:
```
F:\Program Files\Tools_tu_code\tool_Auto_Presentation_file\
```

Tạo cấu trúc như sau (bạn có thể tạo thủ công hoặc dùng Explorer):

```
tool_Auto_Presentation_file/
│
├── 📁 dev/                          ← Thư mục bạn đang CODE THỬ
│   ├── app.py                       ← Bản đang sửa, test
│   ├── requirements.txt
│   ├── test_data.json
│   └── ... (các file test khác)
│
├── 📁 main/                         ← Thư mục CHÍNH THỨC (liên kết GitHub)
│   ├── app.py                       ← Bản ổn định
│   ├── requirements.txt
│   ├── DEPLOY_GUIDE.md
│   └── ... (các file đã hoàn thiện)
│
└── 📁 docs/                         ← Hướng dẫn, tài liệu
    ├── WORKFLOW_GUIDE.md
    └── GITHUB_DESKTOP_GUIDE.md
```

> 💡 **Quy tắc vàng:** Thư mục `main/` chỉ chứa code đã test kỹ và chạy ổn định.

---

## Bước 2: Liên kết thư mục MAIN với GitHub

### Trường hợp: Bạn ĐÃ CÓ repo trên GitHub

**Cách đơn giản nhất: Clone repo vào thư mục main**

1. **Xóa hoặc đổi tên** thư mục `main/` hiện tại (nếu đã có file ở đó)
   - Đổi tên thành `main_backup/` chẳng hạn

2. Mở **GitHub Desktop**

3. Menu **File** → **Clone repository...**

4. Chọn tab **GitHub.com** → Tìm repo của bạn (`aio-epic-slide-generator`)

5. Ở ô **Local path**, chọn đường dẫn:
   ```
   F:\Program Files\Tools_tu_code\tool_Auto_Presentation_file\main
   ```

6. Nhấn **Clone**

```
┌────────────────────────────────────────────────────────────┐
│  Clone a repository from the Internet                      │
│                                                            │
│  [ GitHub.com ] [ GitHub Enterprise ] [ URL ]              │
│                                                            │
│  ☑ aio-epic-slide-generator     ○ Other repo...            │
│                                                            │
│  Local path                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ...\tool_Auto_Presentation_file\main                │   │
│  └─────────────────────────────────────────────────────┘   │
│  [        Choose...           ]                            │
│                                                            │
│  [          Clone          ]                               │
└────────────────────────────────────────────────────────────┘
```

7. GitHub Desktop sẽ tải code từ GitHub về thư mục `main/`

---

## Bước 3: Copy code từ DEV sang MAIN

Khi bạn đã code xong ở thư mục `dev/` và test ổn định:

### Cách 1: Copy thủ công (Windows Explorer)

1. Mở Explorer → Vào `dev/`
2. Chọn các file cần copy (vd: `app.py`, `requirements.txt`)
3. **Ctrl+C** → Sang thư mục `main/` → **Ctrl+V** → Chọn **Replace** (Ghi đè)

```
┌──────────────────────────────┐      ┌──────────────────────────────┐
│  📁 dev/                     │      │  📁 main/                    │
│  ├── app.py  ────────────────┼─────►│  ├── app.py  ✅ Updated      │
│  ├── requirements.txt ───────┼─────►│  ├── requirements.txt ✅     │
│  └── test_data.json          │      │  └── DEPLOY_GUIDE.md         │
└──────────────────────────────┘      └──────────────────────────────┘
         Ctrl+C                              Ctrl+V (Replace)
```

### Cách 2: Dùng lệnh PowerShell (Nhanh hơn)

Mở PowerShell, gõ:

```powershell
# Copy file từ dev sang main (ghi đè nếu đã tồn tại)
Copy-Item "F:\Program Files\Tools_tu_code\tool_Auto_Presentation_file\dev\app.py" `
          "F:\Program Files\Tools_tu_code\tool_Auto_Presentation_file\main\app.py" -Force

Copy-Item "F:\Program Files\Tools_tu_code\tool_Auto_Presentation_file\dev\requirements.txt" `
          "F:\Program Files\Tools_tu_code\tool_Auto_Presentation_file\main\requirements.txt" -Force
```

> 💡 Dùng `-Force` để ghi đè file cũ không hỏi.

---

## Bước 4: Đẩy lên GitHub bằng GitHub Desktop

### 4.1 Mở GitHub Desktop

1. Trong GitHub Desktop, chọn repo `aio-epic-slide-generator` ở dropdown trên cùng
2. Đảm bảo đang ở đúng thư mục `main/`

### 4.2 Commit và Push

```
┌─────────────────────────────────────────────────────────────┐
│  Current repository ▼                                        │
│  ┌───────────────────────────────────────┐                  │
│  │  ⬇ aio-epic-slide-generator          │                  │
│  └───────────────────────────────────────┘                  │
│                                                              │
│  Changes (2) | History                                       │
│  ═══════════════════════════════════════════════════════    │
│                                                              │
│  ☑ app.py                                  [ Modified ]      │
│    Modified in main/                                         │
│                                                              │
│  ☑ requirements.txt                        [ Modified ]      │
│    Modified in main/                                         │
│                                                              │
│  Summary (required)                                          │
│  ┌───────────────────────────────────────┐                   │
│  │ Update: Thêm tính năng đa ngôn ngữ   │                   │
│  └───────────────────────────────────────┘                   │
│                                                              │
│  Description                                                 │
│  ┌───────────────────────────────────────┐                   │
│  │ - Thêm chế độ tiếng Việt/English     │                   │
│  │ - Sửa giao diện thân thiện hơn       │                   │
│  └───────────────────────────────────────┘                   │
│                                                              │
│  [     Commit to main     ]                                  │
│                                                              │
│  ═══════════════════════════════════════════════════════    │
│  Last fetched: Just now                                      │
│  [       Push origin      ]                                  │
└─────────────────────────────────────────────────────────────┘
```

**Thao tác:**
1. Tab **Changes** → thấy file đã thay đổi ✅
2. Tick ☑ các file muốn đẩy (thường tick hết)
3. Điền **Summary**: VD `"Update: Thêm tính năng X"`
4. Nhấn **Commit to main**
5. Nhấn **Push origin**
6. Đợi 3-5 giây → Thanh progress xanh chạy xong

> 🎉 **Vậy là xong!** Code đã lên GitHub, Streamlit Cloud sẽ tự động deploy sau 1-2 phút.

---

## ✅ Checklist mỗi lần cập nhật

```
┌────────────────────────────────────────┐
│  ☐ Code xong trong thư mục DEV         │
│  ☐ Test kỹ, chạy ổn định               │
│  ☐ Copy file từ DEV → MAIN             │
│  ☐ Mở GitHub Desktop                   │
│  ☐ Kiểm tra tab Changes                │
│  ☐ Điền Summary mô tả thay đổi         │
│  ☐ Nhấn Commit to main                 │
│  ☐ Nhấn Push origin                    │
│  ☐ Kiểm tra GitHub web đã cập nhật     │
│  ☐ Kiểm tra Streamlit app đã rebuild   │
└────────────────────────────────────────┘
```

---

## 🔥 Mẹo nâng cao

### Mẹo 1: Tạo file batch tự động copy (Windows)

Tạo file `copy_to_main.bat` trong thư mục gốc:

```batch
@echo off
echo ==========================================
echo Copying files from DEV to MAIN...
echo ==========================================

set SOURCE="F:\Program Files\Tools_tu_code\tool_Auto_Presentation_file\dev"
set TARGET="F:\Program Files\Tools_tu_code\tool_Auto_Presentation_file\main"

copy /Y %SOURCE%\app.py %TARGET%\app.py
copy /Y %SOURCE%\requirements.txt %TARGET%\requirements.txt
copy /Y %SOURCE%\*.py %TARGET%\

echo.
echo ✅ Copy completed!
echo Now open GitHub Desktop to Commit and Push.
pause
```

Khi cần copy, chỉ cần **double-click** file này!

### Mẹo 2: Xem trước thay đổi trước khi commit

Trong GitHub Desktop:
- Click vào tên file ở tab Changes
- Bên phải hiện diff (so sánh trước/sau) → Kiểm tra kỹ rồi mới commit

### Mẹo 3: Khôi phục nếu lỗi

Nếu đẩy lên rồi phát hiện lỗi:
1. GitHub Desktop → Tab **History**
2. Chuột phải vào commit trước đó → **Revert this commit**
3. Push lại → Code trên GitHub quay về phiên bản cũ

---

## ❓ Câu hỏi thường gặp

**Q: Tôi quên copy file, sửa trực tiếp trong main thì sao?**  
A: Vẫn được! GitHub Desktop sẽ thấy thay đổi ngay. Nhưng nên giữ thói quen: test ở dev trước, rồi mới copy sang main.

**Q: Streamlit Cloud không cập nhật sau khi push?**  
A: Vào https://share.streamlit.io → Chọn app → Tab **Manage app** → Nhấn **Reboot**.

**Q: Tôi muốn xem code cũ đã đẩy lên GitHub?**  
A: GitHub Desktop → Tab **History** → Click vào commit bất kỳ để xem.

---

**🎉 Chúc bạn code vui vẻ và deploy thành công!**
