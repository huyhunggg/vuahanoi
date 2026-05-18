# VN Stock Picker - Vnstock API Key

Project dùng GitHub Pages + GitHub Actions + VNSTOCK_API_KEY.

## Cách cài

1. Upload tất cả file trong zip ra ngoài cùng repo.
2. Vào `Settings → Secrets and variables → Actions → New repository secret`.
3. Tạo secret:

```txt
Name: VNSTOCK_API_KEY
Secret: dán API Key Vnstock của bạn
```

4. Vào `Settings → Pages`:
   - Source: Deploy from a branch
   - Branch: main
   - Folder: /root

5. Vào `Actions → Update stock data → Run workflow`.

## File chính

```txt
index.html
data.json
update_data.py
requirements.txt
.github/workflows/update-data.yml
.nojekyll
```

## Thêm mã

Mở `update_data.py`, sửa `WATCHLIST`, `NAMES`, `SECTORS`.

## Ghi chú

Nếu Vnstock API lỗi, `data.json` vẫn được tạo bằng fallback sample đủ mã. Mở `data.json → meta.errors` để xem lỗi chi tiết.
