try:
    import email_validator
    print(f"email_validator version: {email_validator.__version__}")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
