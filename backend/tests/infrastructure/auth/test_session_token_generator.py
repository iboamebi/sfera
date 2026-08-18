from app.infrastructure.auth.session_token_generator import (
    SecureSessionTokenGenerator,
)


def test_generate_returns_unique_url_safe_tokens() -> None:
    generator = SecureSessionTokenGenerator()

    first = generator.generate()
    second = generator.generate()

    assert first != second
    assert len(first) >= 40
    assert all(
        character.isalnum() or character in "-_"
        for character in first
    )
