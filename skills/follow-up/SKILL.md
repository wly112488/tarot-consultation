---
name: tarot-follow-up
description: Use when a tarot client requests deeper explanation, supplementary cards, a new question, or a continuation after discussing the reading.
---

# FOLLOW_UP — Clarify, supplement, or start a new round

**Prerequisite:** 继承全部历史记录，特别是已锁定牌面和原始解读。

## Route by intent

- **现有牌义、牌间关系或现实解释的追问**：先用已抽的牌回答；若客户提供的内容与原解释冲突，回读 `skills/feedback/SKILL.md`。无需新抽牌时不要为了流程完整而补抽。
- **补牌请求**：明确补牌将回答什么新增问题、对应哪个补充牌位；先得到客户同意并固定位置与方向规则，再转 `skills/draw/SKILL.md`；旧牌面和原始解释保持锁定，新补牌单独追加，不能重新解释成原本抽到的牌。若同一轮使用无放回牌组，新牌也不能重复。
- **新的独立问题**：`round += 1`，保留旧轮次，重新在 `skills/question/SKILL.md` 明确新问题；新轮次独立决定牌阵和抽牌，但绝不把旧结果清零。
- **需要复述已有结果**：只基于先前记录简明回应，不重新制造另一套初始解读。
- **要求结束**：转 CLOSING。

不要频繁邀请补牌，也不将客户质疑视为必须重新抽牌的理由。

## Next

依据以上意图，**实际读取** `skills/feedback/SKILL.md`、`skills/question/SKILL.md`、`skills/draw/SKILL.md` 或 `skills/closing/SKILL.md`。单纯解释旧牌则继续本阶段。
