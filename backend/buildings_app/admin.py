from django.contrib import admin

from .models import Building, BuildingNews, ElevatorReport


class BuildingNewsInline(admin.TabularInline):
    model = BuildingNews
    extra = 0
    readonly_fields = (
        "title",
        "url",
        "source",
        "published_date",
        "relevance_score",
        "created_at",
    )
    can_delete = True


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ("bin", "address", "borough", "last_news_refresh", "created_at")
    search_fields = ("bin", "address")
    list_filter = ("borough",)
    inlines = [BuildingNewsInline]


@admin.register(ElevatorReport)
class ElevatorReportAdmin(admin.ModelAdmin):
    list_display = ("building", "user", "status", "is_official", "reported_at")
    list_filter = ("status", "is_official", "reported_at")
    search_fields = ("building__address", "building__bin")


@admin.register(BuildingNews)
class BuildingNewsAdmin(admin.ModelAdmin):
    list_display = ("title", "building", "source", "relevance_score", "published_date")
    list_filter = ("source", "relevance_score")
    search_fields = ("title", "building__address", "summary")
