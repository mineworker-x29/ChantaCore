from dotenv import load_dotenv
import sys

from chanta_core.llm import LLMClient


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    load_dotenv()

    llm = LLMClient()

    response = llm.chat(
        system_message="You are ChantaCore's local LLM connection test.",
        user_message="Say hello in one short sentence.",
    )

    print(response)


if __name__ == "__main__":
    main()
