# Tarot Consultation Skills

面向**单个 ChatGPT 会话**的模块化塔罗咨询提示词。入口为 [`SKILL.md`](SKILL.md)，各阶段的 `SKILL.md` 根据客户回答按需读取，保留同一会话的牌阵、牌面、初次解读与反馈记录。

## 使用

在已连接、可读取本仓库的 ChatGPT 会话中输入：

> 请读取 GitHub 仓库 `wly112488/tarot-consultation` 的 `main` 分支根目录 `SKILL.md`，按其规则主持一场完整的塔罗咨询。在同一个会话中，根据阶段切换条件按需读取下一个 Skill，保持已确认的客户问题、牌阵、牌面和解释记录，不展示内部路由。

## 结构

- `SKILL.md`：唯一入口，负责分阶段调用
- `skills/opening/`：开场与主题选择
- `skills/question/`：明确咨询问题
- `skills/spread/`：选牌阵、锁定牌位
- `skills/draw/`：选抽牌方式、记录牌面
- `skills/interpret/`：牌义、牌间关系与初步解读
- `skills/feedback/`：处理客户反馈、现实事实与解释冲突
- `skills/follow-up/`：澄清、补牌、新问题
- `skills/closing/`：结束咨询
- `references/session-contract.md`：跨阶段状态与判断约束
- `references/spread-catalog.md`：主题、牌阵与牌位目录
- `references/deck.md`：完整 78 张韦特系塔罗牌名称索引
- `evals/scenarios.md`：流程与冲突的验收场景

## 运行边界

GitHub 中的 Markdown 是**按需读取的指令文件**，不会自行执行或自动注入更高优先级提示词。ChatGPT 必须具备实际的 GitHub 读取工具，并遵守入口 Skill 的阶段路由要求。若工具不可用或读取失败，应明确说明；不应假称已自动加载。

抽牌可使用可用的随机工具、明确标注为模拟抽牌，或解读客户自行抽取的实体牌；不能把不可验证的抽牌声称为可审计的随机结果。塔罗解读用于象征性探索，不是可验证的超自然事实预测。
