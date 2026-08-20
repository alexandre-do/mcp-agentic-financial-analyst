def print_chat_msg(msgs: list[str]):
    for msg in msgs:
        if hasattr(msg, "pretty_print"):
            msg.pretty_print()
        else:
            print(f"{msg.type}: {msg.content}")
