# python-bootcamp# Python Bootcamp - Week 1 Homework

Repository này chứa mã nguồn và bài làm tuần 1, 2, 3 của **Nhóm 03**

---

## Thành viên nhóm & Phân công công việc

| No. | Member   | GitHub Username          | STUDENT ID NUMBER |
| :-: | :------- | :----------------------- | :---------------- |
|  1  | Member 1 | `@chp0703`               | 25127224          |
|  2  | Member 2 | `@AIVIETNAM-AIO-TheHien` | 25127327          |
|  3  | Member 3 | `@phkhoiit-1508`         | 25127390          |
|  4  | Member 4 | `@kentlatoi`             | 25127369          |
|  5  | Member 5 | `@thanhhuong107`         | 25127197          |
|  6  | Member 6 | `@dmh612`                | 25127340          |

---

## Cấu trúc thư mục (Repository Structure)

```text
python-bootcamp/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/          # Cấu hình GitHub Actions CI
├── members/                # Thư mục chứa bài làm cá nhân
│   ├── phat_ch/
│   │   └── w1/             # Bài tập Week 1 của Member 1
│   │       ├── translate.py
│   │       ├── timetable.py
│   │       ├── rules.py
|   |       └──...
│   └── ...
├── samples/              # Code mẫu và tài liệu tham khảo
├── shared/               # Chứa contract.py và mã nguồn dùng chung
|
├── tests/                  # Kiểm thử tự động (pytest)
│   ├── conftest.py
│   ├── test_w1.py
|   ├── test_w2.py
|   └── test_w3.py
|
├── PROGRESS.md             # Bảng theo dõi tiến độ công việc nhóm
└── README.md               # Tài liệu hướng dẫn dự án
```

## Reviewer rotation

Reviewer luân phiên theo vòng sau:

1. Member 1 review Member 2.
2. Member 2 review Member 3.
3. Member 3 review Member 4.
4. Member 4 review Member 5.
5. Member 5 review Member 6.
6. Member 6 review Member 1.

Vì vậy, chiều review là Member 1 → Member 2 → Member 3 → Member 4 → Member 5 → Member 6 → Member 1.
