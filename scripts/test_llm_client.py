from dotenv import load_dotenv

from chanta_core.llm import LLMClient


def main() -> None:
    load_dotenv()

    llm = LLMClient()

    response = llm.chat(
        system_message="You are ChantaCore's local LLM connection test.",
        user_message="Say hello in one short sentence.",
    )

    print(response)


if __name__ == "__main__":
    main()