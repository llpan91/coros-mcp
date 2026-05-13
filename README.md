# coros-mcp

COROS (高驰) 手表数据 MCP Server —— 让 Claude 直接读取和分析你的运动、睡眠、健康数据。

Fork 自 [cygnusb/coros-mcp](https://github.com/cygnusb/coros-mcp)，新增了睡眠时间戳解析等功能。

## 能做什么

在 Claude Code 中直接用自然语言提问：

- "分析一下我最近两个月的跑步数据"
- "最近一周睡眠质量怎么样"
- "我的 HRV 和静息心率趋势"
- "对比最近三次跑步的配速和心率"
- "帮我创建一个间歇训练计划"

## 快速安装

### 1. 安装 uv + 克隆代码

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

git clone https://github.com/llpan91/coros-mcp.git ~/coros-mcp
cd ~/coros-mcp
uv python install 3.12
uv venv --python 3.12
uv pip install -e .
```

### 2. 配置高驰账号

```bash
cat > ~/coros-mcp/.env << 'EOF'
COROS_EMAIL=你的邮箱
COROS_PASSWORD=你的密码
COROS_REGION=cn
EOF
```

> Region 选择：国内用 `cn`，欧洲 `eu`，美国 `us`，亚洲 `asia`

### 3. 注册到 Claude Code

```bash
claude mcp add coros-mcp -s user -- uv --directory ~/coros-mcp run coros-mcp serve
```

完成。打开 Claude Code 直接问即可。

## 可用工具

### 数据查询

| 工具 | 功能 |
|------|------|
| `get_daily_metrics` | 每日健康指标：HRV、静息心率、训练负荷、VO2max 等 |
| `get_sleep_data` | 睡眠分期（深睡/浅睡/REM/清醒）、入睡和醒来时间、睡眠心率 |
| `list_activities` | 活动列表：跑步、骑行、游泳等，含心率/配速/功率等摘要 |
| `get_activity_detail` | 单次活动详情：分圈数据、心率区间、功率区间 |

### 训练管理

| 工具 | 功能 |
|------|------|
| `list_workouts` | 已保存的训练计划 |
| `create_workout` | 创建结构化训练（支持间歇/重复组） |
| `delete_workout` | 删除训练计划 |
| `schedule_workout` | 将训练安排到日历 |
| `list_planned_activities` | 查看训练日历 |
| `remove_scheduled_workout` | 移除已安排的训练 |
| `create_strength_workout` | 创建力量训练（组数/次数/时间） |
| `list_exercises` | 浏览高驰运动库 |

### 认证管理

| 工具 | 功能 |
|------|------|
| `authenticate_coros` | Web API 登录 |
| `authenticate_coros_mobile` | Mobile API 登录（睡眠数据需要） |
| `check_coros_auth` | 检查认证状态 |

## 相比上游的改动

- **睡眠时间戳**：`SleepRecord` 新增 `sleep_start` / `sleep_end` 字段，记录入睡和醒来的 Unix 时间戳
- 通过解码 Mobile API 返回的 `sleepList` 二进制数据（`dataType=13`）提取时间信息

详见 [CHANGELOG.md](CHANGELOG.md)。

## CLI 命令

```bash
coros-mcp serve          # 启动 MCP Server（Claude Code 自动调用）
coros-mcp auth           # 交互式登录（Web + Mobile）
coros-mcp auth-web       # 仅 Web API 登录
coros-mcp auth-mobile    # 仅 Mobile API 登录（睡眠数据）
coros-mcp auth-status    # 查看认证状态
coros-mcp auth-clear     # 清除已保存的 token
coros-mcp sync           # 同步历史数据到本地 SQLite 缓存
coros-mcp cache-status   # 查看本地缓存状态
```

## 注意事项

- 基于高驰**非官方** API，可能随时失效
- Token 24 小时过期，配置 `.env` 后会自动重新登录
- Mobile API 登录会踢掉手机 App 的登录态（使用 `auth-web` 可避免，Mobile token 会在首次请求睡眠数据时自动获取）
- 卡路里单位：API 返回的是 cal（物理卡），需除以 1000 得到 kcal

## 依赖

- Python >= 3.11
- [fastmcp](https://github.com/jlowin/fastmcp) / [httpx](https://www.python-httpx.org/) / [pydantic](https://docs.pydantic.dev/) / [pycryptodome](https://pycryptodome.readthedocs.io/) / [keyring](https://github.com/jaraco/keyring) / [python-dotenv](https://github.com/theskumar/python-dotenv)
