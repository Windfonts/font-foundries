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
| english_name | string | 厂商名称（英文） |
| type | string | 类型：company / studio / individual |
| country | string | 国家/地区 |
| website | string | 官网 |
| license_policy_url | string | 授权政策页面 |
| contact_email | string | 联系邮箱 |
| social_links | object | 社交链接（weibo/twitter/github） |
| description | string | 简介 |
| fonts | string[] | 旗下字体（normalized_name 列表） |
| default_license_type | string | 默认授权类型 |

## 已收录厂商（部分）

| 厂商 | slug | 类型 |
|------|------|------|
| 阿里巴巴设计 | alibaba-design | company |
| 阿里妈妈 | alimama | company |
| 方正字库 | founder-type | company |
| 汉仪字库 | hanyi | company |
| 造字工房 | makefont | studio |
| 站酷 | zcool | company |
| 思源字体（Adobe/Google） | source-han | company |

## 关联仓库

- `font-metadata` → 字体元数据（通过 foundry 字段关联）
- `font-licenses` → 各厂商字体的授权信息
