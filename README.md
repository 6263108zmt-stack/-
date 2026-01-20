# 粤业悦菁才（FastAPI + SQLite + 纯前端）

功能：
- **政策库**：搜索/筛选/跳转原文（首启动会自动抓取官方/半官方门户索引，生成 50+ 条政策链接；无网则用本地种子数据）
- **基地库**：地图展示基地，点击可查看入驻条件/联系方式/官网链接（首启动会自动抓取“基地导览”页面生成 20+ 条）
- **AI 助手**：根据填写的信息与需求，推荐**创业/就业基地 + 匹配政策**（规则 + 关键词检索；可选接入 OpenAI 生成更自然答复）
- **专家联系**：专家列表 + 咨询表单（可落库；配置 SMTP 可邮件转发）
- **后台管理**：可增删改政策/基地/专家；可手动“刷新抓取”

## 运行（Python 3.8+）

```bash
cd gba_youth_portal
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# 至少把 ADMIN_TOKEN 改掉

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- 用户端：`http://127.0.0.1:8000/`
- 后台：`http://127.0.0.1:8000/admin.html`（输入 ADMIN_TOKEN）

## 数据抓取

首启动会尝试抓取并入库（后台也可“刷新抓取”）：
- **政策汇编索引**：解析出大量政策链接
- **基地导览**：解析基地名称/城市/地址/联系方式等（坐标默认用城市中心点，后台可手动修正）

无网时会加载 `data/seed_*.json` 的种子数据。
