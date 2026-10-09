---
name: tarot-follow-up
description: Use when a tarot client requests deeper explanation, supplementary cards, a new question, or a continuation after discussing the reading.
---

# FOLLOW_UP — Clarify, supplement, or start a new round

**Prerequisite:** 继承全部历史记录，特别是已锁定牌面和原始解读。

## Route by intent

- **原问题的深入方向或现有牌义、牌间关系、现实解释的追问**：客户在 FEEDBACK 选定方向后，优先依据原牌阵、固定牌位及牌间关系直接回答；不要求先补充现实背景，也不另开轮次。若新事实与原解释冲突，回读 `skills/feedback/SKILL.md`。无需新抽牌时不要为了流程完整而补抽。
- **补牌请求或现有牌阵不足以回答深入问题**：说明补牌将回答什么新增问题、对应哪个补充牌位；先得到客户同意并固定位置与方向规则，再转 `skills/draw/SKILL.md`；旧牌面和原始解释保持锁定，新补牌单独追加，不能重新解释成原本抽到的牌。数字抽牌同一轮继续使用先前 `prepare` 生成的同一状态文件，运行 `skills/draw/scripts/tarot_shuffle.py reveal` 追加未选过的位置；禁止重洗、重复位置或覆盖原状态。
- **新的独立问题**：`round += 1`，保留旧轮次，重新在 `skills/question/SKILL.md` 明确新问题；新轮次独立决定牌阵和抽牌，使用新状态文件执行新的 `prepare`，但绝不把旧结果清零。
- **需要复述已有结果**：只基于先前记录简明回应，不重新制造另一套初始解读。
- **要求结束**：转 CLOSING。

一次深入方向回答完成后等待客户下一步输入，不自动再次邀请选择方向、开启新轮或进入 CLOSING；客户继续提问时再依其意图处理。不要频繁邀请补牌，也不将客户质疑视为必须重新抽牌的理由。

## Next

依据以上意图，**实际读取** `skills/feedback/SKILL.md`、`skills/question/SKILL.md`、`skills/draw/SKILL.md` 或 `skills/closing/SKILL.md`。单纯解释旧牌则继续本阶段。
