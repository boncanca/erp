import pytest
from django.test import override_settings

from apps.users.models import User
from core.identity.models import ExternalIdentity, LoginAudit
from core.identity.providers.base import ProviderRegistry


@pytest.mark.django_db
def test_external_identity_can_be_linked():
    user = User.objects.create_user(email="identity@example.com", password="safe-pass-123")

    external = ExternalIdentity.objects.create(
        user=user,
        provider="keycloak",
        external_id="external-123",
    )

    assert external.user_id == user.id
    assert external.provider == "keycloak"


@pytest.mark.django_db
def test_login_audit_record_can_be_created():
    user = User.objects.create_user(email="audit@example.com", password="safe-pass-123")

    audit = LoginAudit.objects.create(
        user=user,
        attempted_email=user.email,
        result="success",
    )

    assert audit.result == "success"
    assert audit.attempted_email == user.email


@override_settings(AUTH_ENABLE_OAUTH2_PROVIDER=False)
def test_oauth2_provider_disabled_by_default():
    registry = ProviderRegistry()
    assert registry.get("oauth2") is None


@override_settings(AUTH_ENABLE_OAUTH2_PROVIDER=True)
def test_oauth2_provider_enabled_with_feature_flag():
    registry = ProviderRegistry()
    assert registry.get("oauth2") is not None
