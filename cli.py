"""
Grathon CLI - برای استفاده از Grathon به‌عنوان command-line tool
"""

import sys

def main():
    """Entry point برای grathon-cli"""
    print("🤖 Grathon CLI")
    print(f"Version: 0.1.0")
    print(f"Python: {sys.version.split()[0]}")

    if len(sys.argv) < 2:
        print("\nدستورات:")
        print("  grathon-cli version   - نسخه‌ی Grathon")
        print("  grathon-cli info      - اطلاعات Grathon")
        return 0

    command = sys.argv[1]

    if command == "version":
        print("Grathon 0.1.0")
    elif command == "info":
        print("Grathon - High-level TDLib wrapper for Telegram bots")
        print("\nDocumentation: https://github.com/yourusername/grathon")
        print("\nUsage:")
        print("  from grathon import GrathonBot")
    else:
        print(f"❌ دستور نامشخص: {command}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
