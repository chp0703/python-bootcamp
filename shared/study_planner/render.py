from shared.contract import Block


def render(blocks: list[Block]) -> str:
    """Convert allocated study blocks into readable text."""
    if not blocks:
        return "No study blocks allocated."

    lines = ["STUDY PLAN"]
    total_hours = 0.0

    for index, block in enumerate(blocks, start=1):
        title = block.task.title
        hours = block.hours

        lines.append(f"{index}. {title} - {hours:.1f} h")
        total_hours += hours

    lines.append("")
    lines.append(f"Total: {total_hours:.1f} h")

    return "\n".join(lines)
