import pytest
from interview.profiles.models import UserProfile

# Create your tests here.

@pytest.fixture
def user(db):
    return UserProfile.objects.create_user(
        email="test@example.com",
        password="securepassword123",
        first_name="Jane",
        last_name="Doe",
    )


# --- Challenge 4: Profile Model ---

@pytest.mark.django_db
def test_user_profile_created_with_email(user):
    assert user.email == "test@example.com"


@pytest.mark.django_db
def test_user_profile_username_field_is_email(user):
    assert UserProfile.USERNAME_FIELD == "email"


@pytest.mark.django_db
def test_get_full_name(user):
    assert user.get_full_name() == "Jane Doe"


@pytest.mark.django_db
def test_get_username_returns_email(user):
    assert user.get_username() == "test@example.com"


@pytest.mark.django_db
def test_is_authenticated_is_true(user):
    assert user.is_authenticated is True


@pytest.mark.django_db
def test_is_active_default_true(user):
    assert user.is_active is True


@pytest.mark.django_db
def test_is_staff_default_false(user):
    assert user.is_staff is False


@pytest.mark.django_db
def test_is_admin_default_false(user):
    assert user.is_admin is False


@pytest.mark.django_db
def test_create_superuser(db):
    superuser = UserProfile.objects.create_superuser(
        email="super@example.com",
        password="superpassword123",
    )
    assert superuser.is_staff is True
    assert superuser.is_superuser is True
    assert superuser.is_admin is True


@pytest.mark.django_db
def test_str_returns_email(user):
    assert str(user) == "test@example.com"


@pytest.mark.django_db
def test_password_is_hashed(user):
    assert user.password != "securepassword123"
    assert user.check_password("securepassword123") is True
