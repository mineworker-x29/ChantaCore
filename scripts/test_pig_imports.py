from chanta_core.pig.service import PIGService


def main() -> None:
    service = PIGService()
    result = service.analyze_recent(limit=20)
    print(result)


if __name__ == "__main__":
    main()
