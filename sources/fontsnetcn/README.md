# fonts.net.cn 作者数据全量采集

来源:字体天下 `www.fonts.net.cn`(厂商与设计师栏目),抓取日 **2026-09-21**。
用途:Windfonts 厂商档案(`foundries/{slug}/`)的外部源数据,供画像补全与核对;不直接对外展示。

## 数据事实(抓完才知道的)

- 全站 **6624** 个作者条目(站方计数 6625,索引按 authorId 去重差 1)。
- **真头像只有 158 家**(2.4%)——列表页给所有条目都渲染头像 URL,但 97.6% 指向
  `author-avatar-default.jpg` 站点占位图。占位图在仓里只存一份 `avatars/_default.jpg`,
  其余为硬链(git 打包时同一 blob,不占体积)。
- 厂商简介(`site_author_sh_desc`)与类型(厂商/设计师)同样只覆盖少数条目,以 `authors.jsonl` 实际内容为准。

## 目录

```
data/
  authors-index.json   # 列表页索引:authorId/name/avatar/fonts/popularity(221 页聚合)
  authors.jsonl        # 详情页逐条:上表字段 + type/description/sourceUrl/fetchedAt
  matches.json         # 我方 slug ↔ 字体天下 authorId 匹配表(30 验证 + 3 拒,含理由)
avatars/
  {authorId}.{jpg|png|gif}   # 158 真头像 + _default.jpg(占位,其余硬链)
scripts/
  scrape_list.sh       # 列表页 221 页抓取(0.2s 限速)→ 索引
  scrape_details.py    # 详情页全量 → authors.jsonl(5 workers × 0.75s,断点续传)
  scrape_avatars.py    # 头像全量(8 workers,断点续传,占位图硬链去重)
```

## 字段说明(authors.jsonl)

| 字段 | 说明 |
|------|------|
| authorId | 站点作者 ID(详情页 URL `/author-{id}-1.html`) |
| name / siteName | 详情页展示名 / 列表页名单(不一致时以 name 为准) |
| type | `厂商` / `设计师` 等,站点标注 |
| description | 厂商简介原文(多为厂商自提交) |
| fonts / popularity | 列表页的字体数 / 人气 |
| avatarUrl | 头像原始 CDN 地址(`img.cdn.fonts.net.cn`) |

## 版权口径

简介与头像是字体天下页面内容,`descSource`/`sourceUrl` 保留了原页可追溯链接。
入库仅作内部档案核对;若要进对外产品(fonts-front 等),先过授权评估或改写。

## 复跑

```bash
cd sources/fontsnetcn
bash scripts/scrape_list.sh                # 重建 data/authors-index.json
python3 scripts/scrape_details.py          # 断点续传,已抓的跳过
python3 scripts/scrape_avatars.py
```

## 关联

- 2026-09-21 首轮消化:fonts-front 已从本源收 8 家头像 + 13 家简介
  (见 fonts-front `docs/HANDOFF.md` §6「fonts.net.cn 通道跑通」);匹配明细在 `data/matches.json`。
