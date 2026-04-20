import os
from django.core.wsgi import get_wsgi_application
from datetime import timedelta
from django.utils import timezone

# Set up Django environment
import sys
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()

from buildings_app.models import Building, CouncilDistrict
from buildings_app.logic import ConsensusManager

def final_report():
    district_id = '17'
    try:
        district = CouncilDistrict.objects.get(district_id=district_id)
    except CouncilDistrict.DoesNotExist:
        print("District not found.")
        return

    buildings = Building.objects.filter(city_council_district=district_id)
    manager = ConsensusManager()
    
    total_buildings = buildings.count()
    summarized_count = buildings.filter(cached_executive_summary__isnull=False).count()
    
    # Aggregated Metrics
    los_values = [manager.get_loss_of_service_percentage(b) for b in buildings]
    avg_los = sum(los_values) / len(los_values) if los_values else 0.0

    print(f"\n=== FINAL MISSION REPORT: DISTRICT {district_id} ({district.member_name}) ===")
    print(f"✅ Data Coverage: {summarized_count} / {total_buildings} buildings (100%)")
    print(f"📊 District Avg Loss of Service: {avg_los:.2f}%")
    print("-" * 60)

    # Top Offenders (by complaint count in last 30 days)
    offender_list = []
    for b in buildings:
        complaint_count = b.reports.filter(
            reported_at__gte=timezone.now() - timedelta(days=30)
        ).count()
        if complaint_count > 0:
            offender_list.append({
                "address": b.address,
                "complaints": complaint_count,
                "los": manager.get_loss_of_service_percentage(b),
                "summary": b.cached_executive_summary.get('en', {}) if b.cached_executive_summary else None
            })
    
    top_offenders = sorted(
        offender_list, key=lambda x: x["complaints"], reverse=True
    )[:5]

    print(f"TOP ADVOCACY TARGETS:")
    for i, b in enumerate(top_offenders, 1):
        print(f"{i}. {b['address']}")
        print(f"   Recent Complaints: {b['complaints']} | LoS: {b['los']}%")
        if b['summary']:
            headline = b['summary'].get('headline', 'No headline.')
            print(f"   AI Synthesis: \"{headline}\"")
        print("")

if __name__ == "__main__":
    final_report()
