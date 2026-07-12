#!/usr/bin/env python3
"""
Research Workflow Orchestrator for ea-new
Helps reduce manual friction while preserving the gated rigor.

Usage examples:
  python research.py status
  python research.py prepare-prompt G1
  python research.py new-card
  python research.py confirm-card
  python research.py new-prereg
  python research.py confirm-prereg
  python research.py open-holdout   # for G7

The script never bypasses human sign-off for gates that require it.
"""

import argparse
import datetime
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

# ============== CONFIG ==============
REPO_ROOT = Path(__file__).resolve().parent
RESEARCH = REPO_ROOT / "research"
CARDS = RESEARCH / "cards"
PREREG = RESEARCH / "prereg"
PROMPTS = RESEARCH / "prompts"
RESULTS = RESEARCH / "results"
AUDITS = RESEARCH / "audits"
DECISION_LOG = RESEARCH / "decision_log.md"
CONSTRAINTS = RESEARCH / "constraints.yaml"
AI_CONSTITUTION = RESEARCH / "AI_CONSTITUTION.md"

G1_PROMPT = PROMPTS / "G1_research_card.md"
G2_PROMPT = PROMPTS / "G2_preregister.md"

TODAY = datetime.date.today().strftime("%Y%m%d")

# ============== HELPERS ==============
def ensure_dirs():
    for d in [CARDS, PREREG, RESULTS, AUDITS]:
        d.mkdir(parents=True, exist_ok=True)

def get_next_id(folder: Path, prefix: str = "") -> str:
    """Find next ### for today, e.g. 20260712-002"""
    pattern = re.compile(rf"{TODAY}-(\d{{3}})")
    max_num = 0
    for f in folder.glob(f"{TODAY}-*.md"):
        m = pattern.search(f.name)
        if m:
            max_num = max(max_num, int(m.group(1)))
    return f"{TODAY}-{max_num + 1:03d}"

def read_text(p: Path) -> str:
    if not p.exists():
        return f"[FILE NOT FOUND: {p}]"
    return p.read_text(encoding="utf-8")

def write_text(p: Path, content: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"✅ Created: {p.relative_to(REPO_ROOT)}")

def open_in_editor(path: Path):
    """Try to open file in editor (cross-platform best effort)"""
    editors = ["code", "code-insiders", "subl", "atom", "vim", "nvim", "nano"]
    for ed in editors:
        try:
            subprocess.run([ed, str(path)], check=False)
            return
        except FileNotFoundError:
            continue
    # Fallbacks
    if sys.platform == "win32":
        os.startfile(str(path))
    elif sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=False)
    else:
        print(f"📝 Please open manually: {path}")
        print("   (or set your EDITOR env var)")

def update_decision_log(action: str, details: str = ""):
    """Append a simple entry to decision_log.md"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"\n- [{timestamp}] {action}"
    if details:
        entry += f" — {details}"
    with open(DECISION_LOG, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"📝 Updated decision_log.md: {action}")

def check_constraints_locked() -> bool:
    content = read_text(CONSTRAINTS)
    return "status: LOCKED" in content

def parse_rubric_score(card_path: Path) -> Optional[int]:
    """Extract Total score from rubric table"""
    content = read_text(card_path)
    match = re.search(r"\*\*Total\*\*\s*\|\s*(\d+)/12", content)
    if match:
        return int(match.group(1))
    # fallback
    match2 = re.search(r"Total.*?(\d+)\s*/\s*12", content, re.IGNORECASE)
    return int(match2.group(1)) if match2 else None

def parse_decision(card_path: Path) -> Optional[str]:
    content = read_text(card_path)
    match = re.search(r"\*\*Decision:\*\*\s*(PASS|KILL|REWORK)", content, re.IGNORECASE)
    return match.group(1).upper() if match else None

# ============== COMMANDS ==============
def cmd_status():
    print("=== RESEARCH WORKFLOW STATUS ===\n")
    print(f"Today ID base: {TODAY}")
    print(f"Constraints locked? {'✅ YES' if check_constraints_locked() else '❌ NO (G0 required)'}")
    
    # Latest card
    latest_card = None
    for f in sorted(CARDS.glob("*.md"), reverse=True):
        if f.name != "_TEMPLATE.md":
            latest_card = f
            break
    if latest_card:
        score = parse_rubric_score(latest_card)
        decision = parse_decision(latest_card)
        print(f"\nLatest Research Card: {latest_card.name}")
        print(f"  Score: {score}/12" if score else "  Score: not found")
        print(f"  Decision: {decision}" if decision else "  Decision: not signed yet")
    
    # Latest prereg
    latest_prereg = None
    for f in sorted(PREREG.glob("*.md"), reverse=True):
        if f.name != "_TEMPLATE.md":
            latest_prereg = f
            break
    if latest_prereg:
        content = read_text(latest_prereg)
        locked = "status: LOCKED" in content.lower() or "LOCKED" in content
        print(f"\nLatest Prereg: {latest_prereg.name}  {'🔒 LOCKED' if locked else '✏️ DRAFT'}")

    print("\nNext suggested action:")
    if not check_constraints_locked():
        print("  → G0: Lock constraints.yaml (edit status: LOCKED)")
    elif not latest_card or not parse_decision(latest_card):
        print("  → G1: python research.py new-card   (then confirm-card after signing)")
    elif parse_decision(latest_card) == "PASS" and not latest_prereg:
        print("  → G2: python research.py new-prereg")
    else:
        print("  → Continue with G3+ (data audit, spec, mechanism test...)")
        print("     See flow.md and research/README.md for details.")

def cmd_prepare_prompt(gate: str):
    """Print full context the user should paste into AI for that gate"""
    ensure_dirs()
    if gate.upper() == "G1":
        print("=" * 60)
        print("COPY EVERYTHING BELOW AND PASTE INTO YOUR AI CHAT FOR G1")
        print("=" * 60 + "\n")
        print(read_text(AI_CONSTITUTION))
        print("\n" + "=" * 40 + " CONSTRAINTS (do not change) " + "=" * 40 + "\n")
        print(read_text(CONSTRAINTS))
        print("\n" + "=" * 40 + " G1 PROMPT " + "=" * 40 + "\n")
        print(read_text(G1_PROMPT))
        print("\n" + "=" * 60)
        print("After AI replies, paste the output into the new card file created by 'new-card'")
        print("=" * 60)
    elif gate.upper() == "G2":
        print("For G2, first make sure you have a PASS card. Then run 'new-prereg'.")
        print("The prereg prompt will be injected into the created file.")
    else:
        print("Supported: G1, G2")

def cmd_new_card():
    ensure_dirs()
    if not check_constraints_locked():
        print("❌ G0 not done. Please lock constraints.yaml first (status: LOCKED)")
        return

    card_id = get_next_id(CARDS)
    card_path = CARDS / f"{card_id}.md"

    # Build content from template + helpful header
    template = read_text(CARDS / "_TEMPLATE.md")
    header = f"""# RESEARCH CARD — ID: {card_id}

**Status**: DRAFT → Fill rubric & sign after AI generates content  
**Created by script**: {datetime.datetime.now().isoformat(timespec='minutes')}

> **Hướng dẫn nhanh**:
> 1. Dùng lệnh `python research.py prepare-prompt G1` để lấy full context paste vào AI
> 2. Paste kết quả AI vào phần dưới (thay thế nội dung placeholder)
> 3. Điền rubric ở cuối → **Decision: PASS** (nếu ≥10/12) hoặc KILL
> 4. Chạy `python research.py confirm-card` để ghi nhận

---
"""

    # Keep the template structure but update ID
    content = template.replace("YYYYMMDD-###", card_id)
    content = header + "\n" + content.split("---", 1)[1] if "---" in content else header + content

    write_text(card_path, content)
    print(f"\n📄 Card created: {card_path.name}")
    print("   → Now run: python research.py prepare-prompt G1")
    print("   → Paste into AI, then edit this file with the result + sign rubric")
    open_in_editor(card_path)

def cmd_confirm_card():
    ensure_dirs()
    # Find latest card for today
    candidates = sorted([f for f in CARDS.glob(f"{TODAY}-*.md") if f.name != "_TEMPLATE.md"], reverse=True)
    if not candidates:
        print("❌ No card found for today. Run 'new-card' first.")
        return

    card_path = candidates[0]
    score = parse_rubric_score(card_path)
    decision = parse_decision(card_path)

    if score is None or decision is None:
        print(f"❌ Card {card_path.name} is not fully signed yet.")
        print("   Please fill the rubric table and add **Decision:** + **Signed:** lines.")
        open_in_editor(card_path)
        return

    if decision == "PASS" and score >= 10:
        print(f"✅ Card {card_path.name} PASSED with {score}/12")
        update_decision_log(f"G1 PASS {card_path.name}", f"Score {score}/12")
        print("\nNext: python research.py new-prereg   (after reviewing the card)")
    elif decision == "KILL":
        print(f"🛑 Card {card_path.name} was KILLED (score {score}/12)")
        update_decision_log(f"G1 KILL {card_path.name}", f"Score {score}/12")
    else:
        print(f"⚠️  Card {card_path.name}: Decision={decision}, Score={score}/12")
        print("   Only PASS with ≥10/12 is accepted to proceed.")

def cmd_new_prereg():
    ensure_dirs()
    # Find latest PASS card
    candidates = sorted([f for f in CARDS.glob("*.md") if f.name != "_TEMPLATE.md"], reverse=True)
    if not candidates:
        print("❌ No Research Card found. Do G1 first.")
        return

    latest_card = candidates[0]
    decision = parse_decision(latest_card)
    if decision != "PASS":
        print(f"❌ Latest card {latest_card.name} is not PASS yet. Confirm it first.")
        return

    prereg_id = get_next_id(PREREG)
    prereg_path = PREREG / f"{prereg_id}.md"

    template = read_text(PREREG / "_TEMPLATE.md")
    header = f"""# PREREGISTRATION — ID: {prereg_id}

**Card ID**: {latest_card.name}  
**Status**: DRAFT → Sign & lock after filling  
**Created**: {datetime.datetime.now().isoformat(timespec='minutes')}

> Sau khi điền xong → thêm dòng **Signed** + **status: LOCKED** ở cuối  
> Sau đó chạy `python research.py confirm-prereg`

---
"""

    content = template.replace("YYYYMMDD-###", prereg_id)
    content = header + content.split("---", 1)[1] if "---" in content else header + content

    # Inject reference to the card
    content = content.replace("Card ID | |", f"Card ID | {latest_card.name} |")

    write_text(prereg_path, content)
    print(f"\n📄 Prereg created: {prereg_path.name}")
    print("   → Fill the sections (especially Primary metric, kill floors, variants, mechanism test)")
    print("   → At the bottom, add your signature and change status to LOCKED")
    open_in_editor(prereg_path)

def cmd_confirm_prereg():
    ensure_dirs()
    candidates = sorted([f for f in PREREG.glob(f"{TODAY}-*.md") if f.name != "_TEMPLATE.md"], reverse=True)
    if not candidates:
        print("❌ No prereg file for today.")
        return

    prereg_path = candidates[0]
    content = read_text(prereg_path)

    has_signature = "Signed:" in content and "LOCKED" in content.upper()
    if not has_signature:
        print(f"❌ Prereg {prereg_path.name} not yet signed/locked.")
        print("   Please add signature line and set status: LOCKED at the end.")
        open_in_editor(prereg_path)
        return

    print(f"✅ Prereg {prereg_path.name} LOCKED & signed.")
    update_decision_log(f"G2 LOCKED {prereg_path.name}")
    print("\nGood! Now proceed to G3 (Data Audit) → G4 (Spec) → G5 (Mechanism Test)")
    print("See flow.md for the remaining gates.")

def cmd_open_holdout():
    """G7 helper: remind + show how to unlock holdout"""
    print("G7 — Blind OOS (Holdout)")
    print("1. Make sure G6 (Robustness) has fully PASSED.")
    print("2. Edit constraints.yaml and set:")
    print("      holdout_final:
        opened: true")
    print("3. Sign the change (add comment + date).")
    print("4. Run the OOS test **only once** on the sealed period.")
    print("5. If it fails kill floors → KILL the family.")
    update_decision_log("G7 Holdout opened (manual)")

def main():
    parser = argparse.ArgumentParser(
        description="Research gated workflow helper for ea-new (keeps rigor, reduces copy-paste pain)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="Show current progress and next step")

    p_prompt = sub.add_parser("prepare-prompt", help="Print full context to paste into AI for a gate")
    p_prompt.add_argument("gate", choices=["G1", "G2"], help="Which gate prompt to prepare")

    sub.add_parser("new-card", help="Create today's Research Card file (G1) with template + instructions")
    sub.add_parser("confirm-card", help="Validate rubric + decision on latest card, update log if PASS")

    sub.add_parser("new-prereg", help="Create Preregistration file (G2) linked to latest PASS card")
    sub.add_parser("confirm-prereg", help="Validate signature + LOCKED status on latest prereg")

    sub.add_parser("open-holdout", help="Helper for G7 (unlock sealed holdout)")

    args = parser.parse_args()

    if args.cmd == "status":
        cmd_status()
    elif args.cmd == "prepare-prompt":
        cmd_prepare_prompt(args.gate)
    elif args.cmd == "new-card":
        cmd_new_card()
    elif args.cmd == "confirm-card":
        cmd_confirm_card()
    elif args.cmd == "new-prereg":
        cmd_new_prereg()
    elif args.cmd == "confirm-prereg":
        cmd_confirm_prereg()
    elif args.cmd == "open-holdout":
        cmd_open_holdout()

if __name__ == "__main__":
    main()
