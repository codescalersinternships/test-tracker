from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path("auth/", include("test_tracker.routs.auth")),
                path("dashboard/", include("test_tracker.routs.dashboard")),
                path("requirements/", include("test_tracker.routs.requirement")),
                path("members/", include("test_tracker.routs.member")),
                path("project/", include("test_tracker.routs.project")),
                path("test_plan/", include("test_tracker.routs.test_plan")),
                path("test_suites/", include("test_tracker.routs.test_suites")),
                path("test_cases/", include("test_tracker.routs.test_cases")),
                path("test_runs/", include("test_tracker.routs.test_runs")),
            ]
        ),
    ),
]


if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="Api Documentation",
            default_version="v1",
        ),
        public=False,
    )

    urlpatterns = (
        [
            # URLs specific only to django-debug-toolbar:
            path("__debug__/", include(debug_toolbar.urls)),
            # Swagger
            path(
                "swagger/",
                schema_view.with_ui("swagger", cache_timeout=0),
                name="schema-swagger-ui",
            ),
            path(
                "redoc/",
                schema_view.with_ui("redoc", cache_timeout=0),
                name="schema-redoc",
            ),
            # noqa: DJ05
        ]
        + urlpatterns
        + static(  # type: ignore
            # Serving media files in development only:
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT,
        )
    )
