"""
Generates the extended corporate policy library (66 policies) as markdown files in data/policies/.

The policies are generic templates modelled on what large enterprises typically publish (HR, ethics,
legal & compliance, IT security, finance, health & safety, sustainability and customer policies).
They are written for the fictional company "Acme Enterprise" and should be reviewed by Legal / HR
before real-world use.

Usage:
    python3 data/seed_policies_extended.py
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from policy_library.hr import HR_POLICIES
from policy_library.legal import LEGAL_POLICIES
from policy_library.it_security import IT_POLICIES
from policy_library.operations import FINANCE_POLICIES, EHS_POLICIES, CUSTOMER_POLICIES

POL_DIR = os.path.join(BASE_DIR, "policies")
DEFAULT_ROLES = ["employee", "manager", "hr", "legal", "admin"]

ALL_EXTENDED_POLICIES = (
    HR_POLICIES + LEGAL_POLICIES + IT_POLICIES + FINANCE_POLICIES + EHS_POLICIES + CUSTOMER_POLICIES
)


def render(policy: dict) -> str:
    roles = policy.get("roles") or DEFAULT_ROLES
    lines = [
        f"# {policy['title']}",
        f"Document ID: {policy['id']}",
        f"Version: {policy['ver']}",
        f"Last Updated: {policy['date']}",
        f"Department: {policy['dept']}",
        f"Owner: {policy['owner']}",
        f"Access Roles: {', '.join(roles)}",
        "",
    ]
    for section_title, body in policy["sections"]:
        lines.append(f"## {section_title}")
        lines.append(body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def generate_extended_policies() -> int:
    os.makedirs(POL_DIR, exist_ok=True)
    seen_ids, seen_files = set(), set()
    for policy in ALL_EXTENDED_POLICIES:
        assert policy["id"] not in seen_ids, f"Duplicate policy id {policy['id']}"
        assert policy["file"] not in seen_files, f"Duplicate file name {policy['file']}"
        seen_ids.add(policy["id"])
        seen_files.add(policy["file"])
        with open(os.path.join(POL_DIR, f"{policy['file']}.md"), "w", encoding="utf-8") as fh:
            fh.write(render(policy))
    print(f"Generated {len(ALL_EXTENDED_POLICIES)} extended policy documents in {POL_DIR}")
    return len(ALL_EXTENDED_POLICIES)


if __name__ == "__main__":
    generate_extended_policies()
