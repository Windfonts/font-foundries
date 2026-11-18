# font-foundries

字体厂商档案，管理 Windfonts 字库中所有字体厂商/设计师的信息。

## 目录结构

```
foundries/
  {slug}/
    profile.json       # 厂商档案
    logo.png           # 厂商 Logo（可选）
schemas/
  foundry-profile.schema.json
index.json             # 所有厂商索引
```

## profile.json 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| slug | string | 唯一标识（kebab-case，如 `alibaba-design`） |
| name | string | 厂商名称（中文） |
| nameEn | string | 厂商名称（英文） |
| type | string | 类型：company / studio / individual |
| country | string | 国家/地区 |
| website | string | 官网 |
| licensePolicyUrl | string | 授权政策页面 |
| contactEmail | string | 联系邮箱 |
| description | string | 简介 |
| fonts | string[] | 旗下字体（normalized_name 列表） |
| defaultLicenseType | string | 默认授权类型 |
| logoUrl | string | Logo 地址 |
| established | string | 成立年份 |

## 已收录厂商（部分，slug 以 `foundries/*/profile.json` 实际为准）

| 厂商 | slug | 类型 |
|------|------|------|
| 阿里巴巴设计 | alibaba-design | company |
| 汉仪字库 | hanyi | company |
| 方正字库 | founder | company |
| 站酷 | zcool | company |
| 谷歌+奥多比（Noto CJK） | google-adobe | company |
| 霞鹜 | lxgw | individual |

共 77 家 profile。`fonts[]` 里存的是 font-licenses 的 `normalizedName`；2026-10-07 迁移后部分条目仍写旧 CamelCase，属已知口径漂移（审计 #13）。

## 关联仓库

- `fonts-vault` → 字体库 `fonts` 表（`foundry` 字段关联厂商 slug）
- `font-licenses` → 各厂商字体的授权信息
