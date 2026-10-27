# AI Pose Gallery · 中文版

> 1439 组 AI 生成人像姿势参考图，日文数据完整汉化，附可直接部署的静态画廊。

![画廊预览](docs/preview.jpg)

**在线演示：** 部署到 Cloudflare Pages 后替换此处地址
**原始站点：** <https://ai-pose-gallery.pages.dev/>
**原作者：** <https://x.com/giaaibusi>
**GitHub：** <https://github.com/anhao/ai-pose-gallery-zh>

---

## 这是什么

原站 [ai-pose-gallery](https://ai-pose-gallery.pages.dev/) 是一套面向 AI 绘画 / 3D / 摄影参考的姿势图库，元数据全部为日文，且不提供批量素材下载。本仓库做了三件事：

1. **全量镜像** —— 1439 条记录对应的 1439 张缩略图（JPG 300×400）与 1439 张原图（PNG 900×1200）全部落地，共 2878 个文件 / 659.5 MB。
2. **完整汉化** —— 日文字段逐条译为中文，覆盖 4 个体系、26 个分类、288 个姿势名、5 个视角，零遗漏。
3. **可用的前端** —— 一个零依赖的单页画廊，支持分类筛选、关键词搜索、大图灯箱与键盘翻页。

## 数据规模

| 体系 | 条数 |
| --- | ---: |
| 全身单人・标准系 | 365 |
| 全身单人・性感系 | 399 |
| 上半身单人 | 400 |
| 双人缠绵 | 275 |
| **合计** | **1439** |

每条记录对应 5 个视角中的若干个：正面 / 斜侧 / 侧面 / 俯视 / 仰视。

## 目录结构

```
.
├── index.html              # 单页画廊（零依赖，直接打开即可）
├── data/
│   ├── pose.json           # 原始日文数据（1439 条，未改动）
│   ├── pose-zh.json        # 中文数据（前端实际读取，含检索字段）
│   ├── meta.json           # 原始体系分类
│   ├── meta-zh.json        # 中文体系分类
│   └── translations.csv    # 日⇄中对照表（323 条，便于校对）
├── thumbs/                 # 缩略图 1439 张 JPG 300×400（22 MB）
├── img/                    # 原图 1439 张 PNG 900×1200（637 MB）
├── scripts/
│   ├── download.py         # 并发下载器（48 线程 / 断点续传 / 自动重试）
│   ├── i18n.py             # 日译中词典（唯一值去重后的 323 条译文）
│   ├── apply_translation.py# 回填译文，生成中文数据
│   └── verify.py           # 校验文件完整性（存在性 / 大小 / 图片头）
├── _headers                # Cloudflare Pages 缓存策略
├── LICENSE
└── README.md
```

## 数据结构

`data/pose-zh.json` 字段说明：

| 字段 | 原日文字段 | 示例 | 说明 |
| --- | --- | --- | --- |
| `id` | — | `full_sexy_P001_front` | 唯一标识 |
| `体系` | `系統` | 全身单人・性感系 | 4 大类 |
| `姿势编号` | `ポーズ番号` | `P001` | 80 组编号 |
| `分类` | `分類` | 站姿 | 26 类动作 |
| `姿势名称` | `ポーズ名` | S形站姿・胯部侧顶 | 288 种描述 |
| `角度` | `アングル` | 正面 | 5 种视角 |
| `缩略图` | `サムネ` | `thumbs/…jpg` | 相对路径 |
| `原图` | `原寸` | `img/…png` | 相对路径 |
| `检索` | — | 拼接串 | 供前端模糊搜索 |

原始日文数据 `data/pose.json` 保持原样，字段名与站点接口一致，便于对照或回灌。

## 本地预览

画廊通过 `fetch` 读取 JSON，需要 HTTP 环境（直接双击 `index.html` 会被 CORS 拦截）：

```bash
python3 -m http.server 8000
# 打开 http://127.0.0.1:8000
```

功能：体系分类页签、视角下拉筛选、关键词搜索（姿势名 / 分类 / 编号）、懒加载分页（每页 120）、点击看原图、`←/→` 翻页、`Esc` 关闭。

## 脚本用法

```bash
# 重新拉取全部图片（已存在的文件自动跳过，可反复执行）
python3 scripts/download.py
WORKERS=64 python3 scripts/download.py   # 调整并发

# 修改 scripts/i18n.py 中的译文后，重新生成中文数据
python3 scripts/apply_translation.py

# 校验 2878 个文件是否完整
python3 scripts/verify.py
```

## 部署到 Cloudflare Pages

仓库为纯静态站点，无框架、无依赖。

**方式一：GitHub 自动部署（推荐）**

1. 登录 Cloudflare Dashboard → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
2. 选择本仓库 → 生产分支 `main`
3. 构建设置照抄：

   | 字段 | 值 |
   | --- | --- |
   | Framework preset | `None` |
   | Build command | `bash scripts/build.sh` |
   | Build output directory | `dist` |

4. **Save and Deploy**，约 2–5 分钟得到 `https://<project>.pages.dev`
5. 之后每次 `git push` 自动重新发布

> ⚠️ **不要**把 Build output directory 直接填 `/`。仓库根目录含 `.git`（数百 MB），
> Cloudflare 会把它当静态资源扫描，pack 文件超过 25 MiB 单文件限制会导致构建失败。
> `scripts/build.sh` 只拷贝 `index.html`、`_headers`、`data/`、`thumbs/`、`img/` 到 `dist/`。
> 若确实想用根目录，仓库已附 `.assetsignore` 兜底排除非站点文件。

> 站点限制：单文件 ≤ 25 MiB、每次部署 ≤ 20,000 个文件。本仓库最大文件 917 KB、共 2883 个文件，均在限制内。

**方式二：命令行直传**

```bash
bash scripts/build.sh
npx wrangler pages deploy dist --project-name ai-pose-gallery-zh
```

`_headers` 已为 `img/`、`thumbs/` 配置一年期强缓存，图片不会重复回源。

## 内容提示

图库包含成人向姿势参考（部分分类名称涉及性行为术语），仅供艺术创作、动作参考与前端技术学习使用。请勿用于违法用途。未成年人请勿访问。

## 版权与致谢

- **图片与原始数据的著作权归原作者所有**：<https://x.com/giaaibusi>，原始站点 <https://ai-pose-gallery.pages.dev/>
- 本仓库仅为个人学习、汉化与静态站点实践存档，**不对图片主张任何权利**，也不构成对原作品的商业使用授权
- 若原作者认为本仓库侵犯其权益，请通过 Issue 联系，将立即删除相关内容
- `scripts/` 与 `index.html` 的代码以 MIT 协议开源（见 [LICENSE](LICENSE)），该协议**不覆盖** `img/`、`thumbs/` 与 `data/` 中的图片和原始数据
